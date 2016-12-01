import pymongo
from database import client
from mod_base.cache import Cache
from model.chan import ChanKline, Trend, Centre, Fractal, Kline
from model.result import Result

all_stocks = {i['windCode'] for i in client.wind.wind_code.find()}
all_stocks = {'600000.SH', '603009.SH', '002751.SZ', '600006.SH', '300055.SZ', '600054.SH'}

cache = Cache()
limit = 15


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
        cur = client.chan.trend.find(condition).sort('index', pymongo.DESCENDING).limit(limit)
        ret[wind_code] = [Fractal(e) for e in cur]
    return ret


@cache.memoize(timeout=30)
def get_centre(ktype, level):
    ret = {}
    for wind_code in all_stocks:
        condition = {'windCode': wind_code, 'ktype': ktype, 'level': level}
        cur = client.chan.trend.find(condition).sort('index', pymongo.DESCENDING).limit(limit)
        ret[wind_code] = [Centre(e) for e in cur]
    return ret


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
