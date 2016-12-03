# coding:utf-8
import operator
import numpy as np
import json

np.seterr(invalid='ignore')

OP_DICT = {
    '==': operator.eq,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '/': operator.div,
    '*': operator.mul,
    '-': operator.sub,
    '+': operator.add
}


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


class Result(object):
    def __init__(self, data):
        self.data = data

    def compare(self, other, op):
        if not self.data:
            return self
        if isinstance(other, (int, float, enumerate)):
            return Result({k: v for k, v in self.data.items() if OP_DICT[op](v, other)})
        elif isinstance(self.data.values()[0], np.ndarray):
            result = {k1: OP_DICT[op](v1, v2) for k1, v1 in self.items for k2, v2 in other.items if k1 == k2}
            return Result(result)
        elif isinstance(other, Result):
            result = {k1: v1 for k1, v1 in self.items for k2, v2 in other.items if k1 == k2 and OP_DICT[op](v1, v2)}
            return Result(result)
        else:
            raise ValueError(u'比较的对象不是数字或Result对象')

    def operate(self, other, op):
        if isinstance(other, (int, float, enumerate)):
            return Result({k: OP_DICT[op](v, other) for k, v in self.data.items()})
        elif isinstance(other, Result):
            result = {k1: OP_DICT[op](v1, v2) for k1, v1 in self.items for k2, v2 in other.items if k1 == k2}
            return Result(result)
        else:
            raise ValueError(u'比较的对象不是数字或Result对象')

    def __eq__(self, other):
        return self.compare(other, '==')

    def __gt__(self, other):
        return self.compare(other, '>')

    def __ge__(self, other):
        return self.compare(other, '>=')

    def __lt__(self, other):
        return self.compare(other, '<')

    def __le__(self, other):
        return self.compare(other, '<=')

    def __div__(self, other):
        return self.operate(other, '/')

    def __mul__(self, other):
        return self.operate(other, '*')

    def __sub__(self, other):
        return self.operate(other, '-')

    def __add__(self, other):
        return self.operate(other, '+')

    def __and__(self, other):
        if isinstance(other, Result):
            intersection_keys = set(self.wind_codes) & set(other.wind_codes)
            return Result({k: self.data[k] for k in intersection_keys})
        else:
            raise ValueError(u'与的对象不是Result对象')

    def __or__(self, other):
        if isinstance(other, Result):
            union_dict = self.data.copy()
            union_dict.update(other.data)
            return Result(union_dict)
        else:
            raise ValueError(u'或的对象不是Result对象')

    def __str__(self):
        return json.dumps(self.data, indent=4, cls=MyEncoder)

    def __iter__(self):
        return iter(self.wind_codes)

    @property
    def wind_codes(self):
        return self.data.keys()

    @property
    def items(self):
        return self.data.items()

    @property
    def values(self):
        """计算均值时，只能一个一个计算"""
        return self.data.values()[0]
