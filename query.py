# coding:utf-8
import pymongo
from database import client
from model.chan import ChanKline, Trend, Centre, Fractal
from model.result import Result

all_stocks = {i['windCode'] for i in client.wind.wind_code.find()}

COLLECTION_MAPPING = {
    u'缠K线': 'chankline',
    u'趋势': 'trend',
    u'中枢': 'centre',
    u'分型': 'fractal'
}


def original_k(location, ktype, key, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    collection = client.chan.chankline
    for wind_code in stocks:
        condition = {'windCode': wind_code, 'ktype': ktype}
        cur = collection.find(condition).sort('index', pymongo.DESCENDING).limit(abs_location + 1)
        chan_k_list = [ChanKline(e) for e in cur]
        if not chan_k_list or len(chan_k_list) <= abs_location:
            continue
        ret[wind_code] = getattr(chan_k_list[abs_location], 'kline')[key]
    return Result(ret)


def chan_k(location, ktype, key, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    collection = client.chan.chankline
    for wind_code in stocks:
        condition = {'windCode': wind_code, 'ktype': ktype}
        cur = collection.find(condition).sort('index', pymongo.DESCENDING).limit(abs_location + 1)
        chan_k_list = [ChanKline(e) for e in cur]
        if not chan_k_list or len(chan_k_list) <= abs_location:
            continue
        ret[wind_code] = getattr(chan_k_list[abs_location], key)
    return Result(ret)


def trend(location, ktype, key, level, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    collection = client.chan.trend
    for wind_code in stocks:
        condition = {'windCode': wind_code, 'ktype': ktype, 'level': level}
        cur = collection.find(condition).sort('index', pymongo.DESCENDING).limit(abs_location + 1)
        bi_list = [Trend(e) for e in cur]
        if not bi_list or len(bi_list) <= abs_location:
            continue
        ret[wind_code] = getattr(bi_list[abs_location], key)
    return Result(ret)


def fractal(location, ktype, key, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    collection = client.chan.fractal
    for wind_code in stocks:
        condition = {'windCode': wind_code, 'ktype': ktype}
        cur = collection.find(condition).sort('index', pymongo.DESCENDING).limit(abs_location + 1)
        bi_list = [Fractal(e) for e in cur]
        if not bi_list or len(bi_list) <= abs_location:
            continue
        ret[wind_code] = getattr(bi_list[abs_location], key)
    return Result(ret)


def centre(location, ktype, key, level, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    collection = client.chan.centre
    for wind_code in stocks:
        condition = {'windCode': wind_code, 'ktype': ktype, 'level': level}
        cur = collection.find(condition).sort('index', pymongo.DESCENDING).limit(abs_location + 1)
        bi_list = [Centre(e) for e in cur]
        if not bi_list or len(bi_list) <= abs_location:
            continue
        ret[wind_code] = getattr(bi_list[abs_location], key)
    return Result(ret)


def bi(location, ktype, key, stocks=None):
    return trend(location, ktype, key, '-1', stocks)


def duan(location, ktype, key, stocks=None):
    return trend(location, ktype, key, '0', stocks)


def level1(location, ktype, key, stocks=None):
    return trend(location, ktype, key, '1', stocks)


def level2(location, ktype, key, stocks=None):
    return trend(location, ktype, key, '2', stocks)


def level3(location, ktype, key, stocks=None):
    return trend(location, ktype, key, '3', stocks)


def get_price(wind_code, ktype, key, n=15):
    collection = client.chan.chankline
    condition = {'windCode': wind_code, 'ktype': ktype}
    cur = collection.find(condition).sort('index', pymongo.ASCENDING).limit(n)
    return [getattr(ChanKline(e), 'kline').close for e in cur]
