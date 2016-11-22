# coding:utf-8
import json
import operator

OP_DICT = {
    '==': operator.eq,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}


class Result(object):
    def __init__(self, data):
        self.data = data

    def compare(self, other, op):
        if isinstance(other, (int, float, enumerate)):
            return Result({k: v for k, v in self.data.items() if OP_DICT[op](v, other)})
        elif isinstance(other, Result):
            result = {k1: v1 for k1, v1 in self.items for k2, v2 in other.items if k1 == k2 and OP_DICT[op](v1, v2)}
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
        return json.dumps(self.data, indent=4)

    @property
    def wind_codes(self):
        return self.data.keys()

    @property
    def items(self):
        return self.data.items()
