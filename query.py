# coding:utf-8
import pymongo
import numpy as np
import talib as ta
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


# def history(wind_code, ktype, key, start=0, end=None):
#     collection = client.chan.chankline
#     condition = {'windCode': wind_code, 'ktype': ktype}
#     if not end:
#         end = collection.find(condition).count()
#     else:
#         end = collection.find(condition).count() + end
#     condition.update({'index': {'$gte': start}})
#     cur = collection.find(condition).sort('index', pymongo.ASCENDING).limit(end - start)
#     return np.array([getattr(ChanKline(e), 'kline')[key] for e in cur])


def history(wind_codes, ktype, key, start=0, end=None):
    if isinstance(wind_codes, (str, unicode)):
        wind_codes = [wind_codes]
    collection = client.chan.chankline
    ret = {}
    for wind_code in wind_codes:
        condition = {'windCode': wind_code, 'ktype': ktype}
        if not end:
            end = collection.find(condition).count()
        else:
            end = collection.find(condition).count() + end
        condition.update({'index': {'$gte': end - start}})
        cur = collection.find(condition).sort('index', pymongo.ASCENDING).limit(start)
        ret[wind_code] = np.array([getattr(ChanKline(e), 'kline')[key] for e in cur])
    return Result(ret)


def std(stocks, time_period):
    return Result({k: ta.STDDEV(v, timeperiod=time_period) for k, v in stocks.items})


def mean(stocks, time_period):
    return Result({k: ta.MA(v, timeperiod=time_period) for k, v in stocks.items})
