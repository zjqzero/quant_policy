import sys
import pickle
import hashlib
import base64
import inspect
import functools
import uuid
import string
from time import time

text_type = str
string_types = (str,)
integer_types = (int,)


def iteritems(d, *args, **kwargs):
    return iter(d.items(*args, **kwargs))


def to_native(x, charset=sys.getdefaultencoding(), errors='strict'):
    if x is None or isinstance(x, str):
        return x
    return x.decode(charset, errors)


def _items(mappingorseq):
    """Wrapper for efficient iteration over mappings represented by dicts
    or sequences::

        >>> for k, v in _items((i, i*i) for i in xrange(5)):
        ...    assert k*k == v

        >>> for k, v in _items(dict((i, i*i) for i in xrange(5))):
        ...    assert k*k == v

    """
    if hasattr(mappingorseq, 'items'):
        return iteritems(mappingorseq)
    return mappingorseq


class BaseCache(object):
    """Baseclass for the cache systems.  All the cache systems implement this
    API or a superset of it.

    :param default_timeout: the default timeout (in seconds) that is used if no
                            timeout is specified on :meth:`set`. A timeout of 0
                            indicates that the cache never expires.
    """

    def __init__(self, default_timeout=300):
        self.default_timeout = default_timeout

    def get(self, key):
        """Look up key in the cache and return the value for it.

        :param key: the key to be looked up.
        :returns: The value if it exists and is readable, else ``None``.
        """
        return None

    def delete(self, key):
        """Delete `key` from the cache.

        :param key: the key to delete.
        :returns: Whether the key existed and has been deleted.
        :rtype: boolean
        """
        return True

    def get_many(self, *keys):
        """Returns a list of values for the given keys.
        For each key a item in the list is created::

            foo, bar = cache.get_many("foo", "bar")

        Has the same error handling as :meth:`get`.

        :param keys: The function accepts multiple keys as positional
                     arguments.
        """
        return map(self.get, keys)

    def get_dict(self, *keys):
        """Like :meth:`get_many` but return a dict::

            d = cache.get_dict("foo", "bar")
            foo = d["foo"]
            bar = d["bar"]

        :param keys: The function accepts multiple keys as positional
                     arguments.
        """
        return dict(zip(keys, self.get_many(*keys)))

    def set(self, key, value, timeout=None):
        """Add a new key/value to the cache (overwrites value, if key already
        exists in the cache).

        :param key: the key to set
        :param value: the value for the key
        :param timeout: the cache timeout for the key (if not specified,
                        it uses the default timeout). A timeout of 0 idicates
                        that the cache never expires.
        :returns: ``True`` if key has been updated, ``False`` for backend
                  errors. Pickling errors, however, will raise a subclass of
                  ``pickle.PickleError``.
        :rtype: boolean
        """
        return True

    def add(self, key, value, timeout=None):
        """Works like :meth:`set` but does not overwrite the values of already
        existing keys.

        :param key: the key to set
        :param value: the value for the key
        :param timeout: the cache timeout for the key or the default
                        timeout if not specified. A timeout of 0 indicates
                        that the cache never expires.
        :returns: Same as :meth:`set`, but also ``False`` for already
                  existing keys.
        :rtype: boolean
        """
        return True

    def set_many(self, mapping, timeout=None):
        """Sets multiple keys and values from a mapping.

        :param mapping: a mapping with the keys/values to set.
        :param timeout: the cache timeout for the key (if not specified,
                        it uses the default timeout). A timeout of 0
                        indicates tht the cache never expires.
        :returns: Whether all given keys have been set.
        :rtype: boolean
        """
        rv = True
        for key, value in _items(mapping):
            if not self.set(key, value, timeout):
                rv = False
        return rv

    def delete_many(self, *keys):
        """Deletes multiple keys at once.

        :param keys: The function accepts multiple keys as positional
                     arguments.
        :returns: Whether all given keys have been deleted.
        :rtype: boolean
        """
        return all(self.delete(key) for key in keys)

    def has(self, key):
        """Checks if a key exists in the cache without returning it. This is a
        cheap operation that bypasses loading the actual data on the backend.

        This method is optional and may not be implemented on all caches.

        :param key: the key to check
        """
        raise NotImplementedError(
            '%s doesn\'t have an efficient implementation of `has`. That '
            'means it is impossible to check whether a key exists without '
            'fully loading the key\'s data. Consider using `self.get` '
            'explicitly if you don\'t care about performance.'
        )

    def clear(self):
        """Clears the cache.  Keep in mind that not all caches support
        completely clearing the cache.
        :returns: Whether the cache has been cleared.
        :rtype: boolean
        """
        return True

    def inc(self, key, delta=1):
        """Increments the value of a key by `delta`.  If the key does
        not yet exist it is initialized with `delta`.

        For supporting caches this is an atomic operation.

        :param key: the key to increment.
        :param delta: the delta to add.
        :returns: The new value or ``None`` for backend errors.
        """
        value = (self.get(key) or 0) + delta
        return value if self.set(key, value) else None

    def dec(self, key, delta=1):
        """Decrements the value of a key by `delta`.  If the key does
        not yet exist it is initialized with `-delta`.

        For supporting caches this is an atomic operation.

        :param key: the key to increment.
        :param delta: the delta to subtract.
        :returns: The new value or `None` for backend errors.
        """
        value = (self.get(key) or 0) - delta
        return value if self.set(key, value) else None


class SimpleCache(BaseCache):
    """Simple memory cache for single process environments.  This class exists
    mainly for the development server and is not 100% thread safe.  It tries
    to use as many atomic operations as possible and no locks for simplicity
    but it could happen under heavy load that keys are added multiple times.

    :param threshold: the maximum number of items the cache stores before
                      it starts deleting some.
    :param default_timeout: the default timeout that is used if no timeout is
                            specified on :meth:`~BaseCache.set`. A timeout of
                            0 indicates that the cache never expires.
    """

    def __init__(self, threshold=500, default_timeout=300):
        BaseCache.__init__(self, default_timeout)
        self._cache = {}
        self.clear = self._cache.clear
        self._threshold = threshold

    def _prune(self):
        if len(self._cache) > self._threshold:
            now = time()
            toremove = []
            for idx, (key, (expires, _)) in enumerate(self._cache.items()):
                if (expires != 0 and expires <= now) or idx % 3 == 0:
                    toremove.append(key)
            for key in toremove:
                self._cache.pop(key, None)

    def _get_expiration(self, timeout):
        if timeout is None:
            timeout = self.default_timeout
        if timeout > 0:
            timeout = time() + timeout
        return timeout

    def get(self, key):
        try:
            expires, value = self._cache[key]
            if expires == 0 or expires > time():
                return pickle.loads(value)
        except (KeyError, pickle.PickleError):
            return None

    def set(self, key, value, timeout=None):
        expires = self._get_expiration(timeout)
        self._prune()
        self._cache[key] = (expires, pickle.dumps(value,
                                                  pickle.HIGHEST_PROTOCOL))
        return True

    def add(self, key, value, timeout=None):
        expires = self._get_expiration(timeout)
        self._prune()
        item = (expires, pickle.dumps(value,
                                      pickle.HIGHEST_PROTOCOL))
        if key in self._cache:
            return False
        self._cache.setdefault(key, item)
        return True

    def delete(self, key):
        return self._cache.pop(key, None) is not None

    def has(self, key):
        try:
            expires, value = self._cache[key]
            return expires == 0 or expires > time()
        except KeyError:
            return False


valid_chars = set(string.ascii_letters + string.digits + '_.')
delchars = ''.join(c for c in map(chr, range(256)) if c not in valid_chars)
null_control = (None, delchars)


def function_namespace(f, args=None):
    """
    Attempts to returns unique namespace for function
    """
    m_args = inspect.getargspec(f)[0]
    instance_token = None

    instance_self = getattr(f, '__self__', None)

    if instance_self \
            and not inspect.isclass(instance_self):
        instance_token = repr(f.__self__)
    elif m_args \
            and m_args[0] == 'self' \
            and args:
        instance_token = repr(args[0])

    module = f.__module__

    if hasattr(f, '__qualname__'):
        name = f.__qualname__
    else:
        klass = getattr(f, '__self__', None)

        if klass \
                and not inspect.isclass(klass):
            klass = klass.__class__

        if not klass:
            klass = getattr(f, 'im_class', None)

        if not klass:
            if m_args and args:
                if m_args[0] == 'self':
                    klass = args[0].__class__
                elif m_args[0] == 'cls':
                    klass = args[0]

        if klass:
            name = klass.__name__ + '.' + f.__name__
        else:
            name = f.__name__

    ns = '.'.join((module, name))
    ns = ns.translate(*null_control)

    if instance_token:
        ins = '.'.join((module, name, instance_token))
        ins = ins.translate(*null_control)
    else:
        ins = None

    return ns, ins


class Cache(object):
    """
    This class is used to control the cache objects.
    """

    def __init__(self):
        self.cache = SimpleCache()

    def get(self, *args, **kwargs):
        return self.cache.get(*args, **kwargs)

    def set(self, *args, **kwargs):
        self.cache.set(*args, **kwargs)

    def add(self, *args, **kwargs):
        self.cache.add(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.cache.delete(*args, **kwargs)

    def delete_many(self, *args):
        self.cache.delete_many(*args)

    def clear(self):
        self.cache.clear()

    def get_many(self, *args):
        return self.cache.get_many(*args)

    def set_many(self, *args, **kwargs):
        self.cache.set_many(*args, **kwargs)

    def _memvname(self, funcname):
        return funcname + '_memver'

    def _memoize_make_version_hash(self):
        return base64.b64encode(uuid.uuid4().bytes)[:6].decode('utf-8')

    def _memoize_version(self, f, args=None,
                         reset=False, delete=False, timeout=None):
        """
        Updates the hash version associated with a memoized function or method.
        """
        fname, instance_fname = function_namespace(f, args=args)
        version_key = self._memvname(fname)
        fetch_keys = [version_key]

        if instance_fname:
            instance_version_key = self._memvname(instance_fname)
            fetch_keys.append(instance_version_key)

        # Only delete the per-instance version key or per-function version
        # key but not both.
        if delete:
            self.cache.delete_many(fetch_keys[-1])
            return fname, None

        version_data_list = list(self.cache.get_many(*fetch_keys))
        dirty = False

        if version_data_list[0] is None:
            version_data_list[0] = self._memoize_make_version_hash()
            dirty = True

        if instance_fname and version_data_list[1] is None:
            version_data_list[1] = self._memoize_make_version_hash()
            dirty = True

        # Only reset the per-instance version or the per-function version
        # but not both.
        if reset:
            fetch_keys = fetch_keys[-1:]
            version_data_list = [self._memoize_make_version_hash()]
            dirty = True

        if dirty:
            self.cache.set_many(dict(zip(fetch_keys, version_data_list)),
                                timeout=timeout)

        return fname, ''.join(version_data_list)

    def _memoize_make_cache_key(self, make_name=None, timeout=None):
        """
        Function used to create the cache_key for memoized functions.
        """

        def make_cache_key(f, *args, **kwargs):
            _timeout = getattr(timeout, 'cache_timeout', timeout)
            fname, version_data = self._memoize_version(f, args=args,
                                                        timeout=_timeout)

            #: this should have to be after version_data, so that it
            #: does not break the delete_memoized functionality.
            if callable(make_name):
                altfname = make_name(fname)
            else:
                altfname = fname

            if callable(f):
                keyargs, keykwargs = self._memoize_kwargs_to_args(f,
                                                                  *args,
                                                                  **kwargs)
            else:
                keyargs, keykwargs = args, kwargs

            try:
                updated = "{0}{1}{2}".format(altfname, keyargs, keykwargs)
            except AttributeError:
                updated = "%s%s%s" % (altfname, keyargs, keykwargs)

            cache_key = hashlib.md5()
            cache_key.update(updated.encode('utf-8'))
            cache_key = base64.b64encode(cache_key.digest())[:16]
            cache_key = cache_key.decode('utf-8')
            cache_key += version_data

            return cache_key

        return make_cache_key

    def _memoize_kwargs_to_args(self, f, *args, **kwargs):
        #: Inspect the arguments to the function
        #: This allows the memoization to be the same
        #: whether the function was called with
        #: 1, b=2 is equivilant to a=1, b=2, etc.
        new_args = []
        arg_num = 0
        argspec = inspect.getargspec(f)

        args_len = len(argspec.args)
        for i in range(args_len):
            if i == 0 and argspec.args[i] in ('self', 'cls'):
                #: use the repr of the class instance
                #: this supports instance methods for
                #: the memoized functions, giving more
                #: flexibility to developers
                arg = repr(args[0])
                arg_num += 1
            elif argspec.args[i] in kwargs:
                arg = kwargs[argspec.args[i]]
            elif arg_num < len(args):
                arg = args[arg_num]
                arg_num += 1
            elif abs(i - args_len) <= len(argspec.defaults):
                arg = argspec.defaults[i - args_len]
                arg_num += 1
            else:
                arg = None
                arg_num += 1

            #: Attempt to convert all arguments to a
            #: hash/id or a representation?
            #: Not sure if this is necessary, since
            #: using objects as keys gets tricky quickly.
            # if hasattr(arg, '__class__'):
            #     try:
            #         arg = hash(arg)
            #     except:
            #         arg = repr(arg)

            #: Or what about a special __cacherepr__ function
            #: on an object, this allows objects to act normal
            #: upon inspection, yet they can define a representation
            #: that can be used to make the object unique in the
            #: cache key. Given that a case comes across that
            #: an object "must" be used as a cache key
            # if hasattr(arg, '__cacherepr__'):
            #     arg = arg.__cacherepr__

            new_args.append(arg)

        return tuple(new_args), {}

    def memoize(self, timeout=None, make_name=None, unless=None):
        """
        Use this to cache the result of a function, taking its arguments into
        account in the cache key.

        Information on
        `Memoization <http://en.wikipedia.org/wiki/Memoization>`_.

        Example::

            @cache.memoize(timeout=50)
            def big_foo(a, b):
                return a + b + random.randrange(0, 1000)

        .. code-block:: pycon

        .. versionadded:: 0.4
            The returned decorated function now has three function attributes
            assigned to it.

                **uncached**
                    The original undecorated function. readable only

                **cache_timeout**
                    The cache timeout value for this function. For a custom value
                    to take affect, this must be set before the function is called.

                    readable and writable

                **make_cache_key**
                    A function used in generating the cache_key used.

                    readable and writable


        :param timeout: Default None. If set to an integer, will cache for that
                        amount of time. Unit of time is in seconds.
        :param make_name: Default None. If set this is a function that accepts
                          a single argument, the function name, and returns a
                          new string to be used as the function name. If not set
                          then the function name is used.
        :param unless: Default None. Cache will *always* execute the caching
                       facilities unelss this callable is true.
                       This will bypass the caching entirely.

        .. versionadded:: 0.5
            params ``make_name``, ``unless``
        """

        def memoize(f):
            @functools.wraps(f)
            def decorated_function(*args, **kwargs):
                #: bypass cache
                if callable(unless) and unless() is True:
                    return f(*args, **kwargs)

                try:
                    cache_key = decorated_function.make_cache_key(f, *args, **kwargs)
                    rv = self.cache.get(cache_key)
                except Exception:
                    print("Exception possibly due to cache backend.")
                    return f(*args, **kwargs)

                if rv is None:
                    rv = f(*args, **kwargs)
                    try:
                        self.cache.set(cache_key, rv,
                                       timeout=decorated_function.cache_timeout)
                    except Exception:
                        print("Exception possibly due to cache backend.")
                return rv

            decorated_function.uncached = f
            decorated_function.cache_timeout = timeout
            decorated_function.make_cache_key = self._memoize_make_cache_key(
                make_name, decorated_function)
            decorated_function.delete_memoized = lambda: self.delete_memoized(f)

            return decorated_function

        return memoize

    def delete_memoized(self, f, *args, **kwargs):
        """
        Deletes the specified functions caches, based by given parameters.
        If parameters are given, only the functions that were memoized with them
        will be erased. Otherwise all versions of the caches will be forgotten.

        Example::

            @cache.memoize(50)
            def random_func():
                return random.randrange(1, 50)

            @cache.memoize()
            def param_func(a, b):
                return a+b+random.randrange(1, 50)

        .. code-block:: pycon

        Delete memoized is also smart about instance methods vs class methods.

        When passing a instancemethod, it will only clear the cache related
        to that instance of that object. (object uniqueness can be overridden
            by defining the __repr__ method, such as user id).

        When passing a classmethod, it will clear all caches related across
        all instances of that class.

        Example::

            class Adder(object):
                @cache.memoize()
                def add(self, b):
                    return b + random.random()

        .. code-block:: pycon

        :param fname: Name of the memoized function, or a reference to the function.
        :param \*args: A list of positional parameters used with memoized function.
        :param \**kwargs: A dict of named parameters used with memoized function.

        .. note::

            Flask-Cache uses inspect to order kwargs into positional args when
            the function is memoized. If you pass a function reference into ``fname``
            instead of the function name, Flask-Cache will be able to place
            the args/kwargs in the proper order, and delete the positional cache.

            However, if ``delete_memoized`` is just called with the name of the
            function, be sure to pass in potential arguments in the same order
            as defined in your function as args only, otherwise Flask-Cache
            will not be able to compute the same cache key.

        .. note::

            Flask-Cache maintains an internal random version hash for the function.
            Using delete_memoized will only swap out the version hash, causing
            the memoize function to recompute results and put them into another key.

            This leaves any computed caches for this memoized function within the
            caching backend.

            It is recommended to use a very high timeout with memoize if using
            this function, so that when the version has is swapped, the old cached
            results would eventually be reclaimed by the caching backend.
        """
        if not callable(f):
            raise DeprecationWarning("Deleting messages by relative name is no longer"
                                     " reliable, please switch to a function reference")

        try:
            if not args and not kwargs:
                self._memoize_version(f, reset=True)
            else:
                cache_key = f.make_cache_key(f.uncached, *args, **kwargs)
                self.cache.delete(cache_key)
        except Exception:
            print("Exception possibly due to cache backend.")

    def delete_memoized_verhash(self, f, *args):
        """
        Delete the version hash associated with the function.

        ..warning::

            Performing this operation could leave keys behind that have
            been created with this version hash. It is up to the application
            to make sure that all keys that may have been created with this
            version hash at least have timeouts so they will not sit orphaned
            in the cache backend.
        """
        if not callable(f):
            raise DeprecationWarning("Deleting messages by relative name is no longer"
                                     " reliable, please use a function reference")

        try:
            self._memoize_version(f, delete=True)
        except Exception:
            print("Exception possibly due to cache backend.")
