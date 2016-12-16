# coding:utf-8
import pymongo
import numpy as np
import talib as ta
from database import client
from model.chan import ChanKline, Trend, Centre, Fractal
from _query import get_original_k, get_chan_k, get_centre, get_fractal, get_trend
from model.result import Result

all_stocks = {i['windCode'] for i in client.wind.wind_code.find()}

CHAN_MAPPING = {
    'original_k': client.chan.chankline,
    'chan_k': client.chan.chankline,
    'trend': client.chan.trend,
    'fractal': client.chan.fractal,
    'centre': client.chan.centre
}

FUNC_MAPPING = {
    'original_k': get_original_k,
    'chan_k': get_chan_k,
    'trend': get_trend,
    'fractal': get_fractal,
    'centre': get_centre
}


def chan(chan_type, wind_code, ktype, abs_location, level=None, sort_key='index'):
    condition = {'windCode': wind_code, 'ktype': ktype}
    if level:
        condition.update(level=level)
    cur = CHAN_MAPPING[chan_type].find(condition).sort(sort_key, pymongo.DESCENDING).limit(abs_location)
    return [e for e in cur]


def original_k(location, ktype, key, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    for wind_code in stocks:
        chan_k_list = [ChanKline(e) for e in chan('original_k', wind_code, ktype, abs_location)]
        if not chan_k_list or len(chan_k_list) < abs_location:
            continue
        ret[wind_code] = getattr(chan_k_list[abs_location - 1], 'kline')[key]
    return Result(ret)


def chan_k(location, ktype, key, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    for wind_code in stocks:
        chan_k_list = [ChanKline(e) for e in chan('original_k', wind_code, ktype, abs_location)]
        if not chan_k_list or len(chan_k_list) < abs_location:
            continue
        ret[wind_code] = getattr(chan_k_list[abs_location - 1], key)
    return Result(ret)


def trend(location, ktype, key, level, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    for wind_code in stocks:
        trend_list = [Trend(e) for e in chan('trend', wind_code, ktype, abs_location, level)]
        if not trend_list or len(trend_list) < abs_location:
            continue
        ret[wind_code] = getattr(trend_list[abs_location - 1], key)
    return Result(ret)


def fractal(location, ktype, key, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    for wind_code in stocks:
        fractal_list = [Fractal(e) for e in chan('fractal', wind_code, ktype, abs_location)]
        if not fractal_list or len(fractal_list) < abs_location:
            continue
        ret[wind_code] = getattr(fractal_list[abs_location - 1], key)
    return Result(ret)


def centre(location, ktype, key, level, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    for wind_code in stocks:
        centre_list = [Centre(e) for e in chan('centre', wind_code, ktype, abs_location, level)]
        if not centre_list or len(centre_list) < abs_location:
            continue
        ret[wind_code] = getattr(centre_list[abs_location - 1], key)
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
    start = abs(start)
    ret = {}
    for wind_code in wind_codes:
        condition = {'windCode': wind_code, 'ktype': ktype}
        if not end:
            _end = collection.find(condition).count()
        else:
            _end = collection.find(condition).count() + end
        condition.update({'index': {'$gte': _end - start}})
        cur = collection.find(condition).sort('index', pymongo.ASCENDING).limit(start)
        ret[wind_code] = np.array([getattr(ChanKline(e), 'kline')[key] for e in cur])
    return Result(ret)


def std(stocks, time_period):
    return Result({k: ta.STDDEV(v, timeperiod=time_period) for k, v in stocks.items})


def mean(stocks, time_period):
    return Result({k: ta.MA(v, timeperiod=time_period) for k, v in stocks.items})
