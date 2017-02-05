# coding: utf-8
import numpy as np
import pymongo
import talib as ta

from database import client
from mod_base.cache import Cache
from model.chan import ChanKline, Trend, Centre, Fractal, Kline
from model.result import Result

all_stocks = {i['windCode'] for i in client.wind.wind_code.find()}

cache = Cache()
limit = 100


@cache.memoize(timeout=30)
def get_original_k(ktype):
    ret = {}
    for wind_code in all_stocks:
        condition = {'windCode': wind_code, 'ktype': ktype}
        cur = client.chan.chankline.find(condition).sort('index', pymongo.DESCENDING).limit(limit)
        ret[wind_code] = [Kline(e['kline']) for e in cur]
    return ret


@cache.memoize(timeout=30)
def get_chan_k(ktype):
    ret = {}
    for wind_code in all_stocks:
        condition = {'windCode': wind_code, 'ktype': ktype}
        cur = client.chan.chankline.find(condition).sort('index', pymongo.DESCENDING).limit(limit)
        ret[wind_code] = [ChanKline(e) for e in cur]
    return ret


@cache.memoize(timeout=30)
def get_trend(ktype, level):
    ret = {}
    for wind_code in all_stocks:
        condition = {'windCode': wind_code, 'ktype': ktype, 'level': level}
        cur = client.chan.trend.find(condition).sort('index', pymongo.DESCENDING).limit(limit)
        ret[wind_code] = [Trend(e) for e in cur]
    return ret


@cache.memoize(timeout=30)
def get_fractal(ktype):
    ret = {}
    for wind_code in all_stocks:
        condition = {'windCode': wind_code, 'ktype': ktype}
        cur = client.chan.fractal.find(condition).sort('index', pymongo.DESCENDING).limit(limit)
        ret[wind_code] = [Fractal(e) for e in cur]
    return ret


@cache.memoize(timeout=30)
def get_centre(ktype, level):
    ret = {}
    for wind_code in all_stocks:
        condition = {'windCode': wind_code, 'ktype': ktype, 'level': level}
        cur = client.chan.centre.find(condition).sort('index', pymongo.DESCENDING).limit(limit)
        ret[wind_code] = [Centre(e) for e in cur]
    return ret


# @cache.memoize(timeout=30)
# 不能使用cache，因为对象销毁重新分配的ID重复概率极大
def original_k_by_index(wind_codes, ktype, key):
    if isinstance(wind_codes, dict):
        wind_codes = Result(wind_codes)
    ret = {}
    for wind_code, value in wind_codes.items:
        condition = {'windCode': wind_code, 'ktype': ktype, 'index': value}
        result = list(client.chan.chankline.find(condition).limit(1))
        if len(result) == 1:
            ret[wind_code] = getattr(Kline(result[0]['kline']), key)
    return Result(ret)


def original_k(location, ktype, key, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    chan_k_dict = get_original_k(ktype)
    for wind_code in stocks:
        chan_k_list = chan_k_dict[wind_code]
        if not chan_k_list or len(chan_k_list) < abs_location:
            continue
        ret[wind_code] = getattr(chan_k_list[abs_location - 1], key)
    return Result(ret)


def chan_k(location, ktype, key, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    chan_k_dict = get_chan_k(ktype)
    for wind_code in stocks:
        chan_k_list = chan_k_dict[wind_code]
        if not chan_k_list or len(chan_k_list) < abs_location:
            continue
        ret[wind_code] = getattr(chan_k_list[abs_location - 1], key)
    return Result(ret)


def trend(location, ktype, key, level, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    trend_dict = get_trend(ktype, level)
    for wind_code in stocks:
        trend_list = trend_dict[wind_code]
        if not trend_list or len(trend_list) < abs_location:
            continue
        ret[wind_code] = getattr(trend_list[abs_location - 1], key)
    return Result(ret)


def fractal(location, ktype, key, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    fractal_dict = get_fractal(ktype)
    for wind_code in stocks:
        fractal_list = fractal_dict[wind_code]
        if not fractal_list or len(fractal_list) < abs_location:
            continue
        ret[wind_code] = getattr(fractal_list[abs_location - 1], key)
    return Result(ret)


def centre(location, ktype, key, level, stocks=None):
    stocks = stocks or all_stocks
    abs_location = abs(location)
    ret = {}
    centre_dict = get_centre(ktype, level)
    for wind_code in stocks:
        centre_list = centre_dict[wind_code]
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


def history(wind_codes, ktype, key, start=0, end=None):
    """
    :param wind_codes: 股票代码范围
    :param ktype: 级别 2_1表示日级别
    :param key: 取出的关键字
    :param start: index的起始，-1表示从右向左看第一颗缠k线
    :param end: index的结束，-1表示从右向左看第一颗缠k线
    :return:
    """
    if isinstance(wind_codes, (str, unicode)):
        wind_codes = [wind_codes]
    collection = client.chan.chankline
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


def history_by_date(wind_codes, ktype, key, start=0, end=None):
    """
    :param wind_codes: 股票代码范围
    :param ktype: 级别 2_1表示日级别
    :param key: 取出的关键字
    :param start: 起始的缠k线时间
    :param end: 结束的缠k线时间
    :return:
    """
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
