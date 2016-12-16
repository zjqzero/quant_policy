# coding:utf-8
import talib as ta
import numpy as np
import time
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
from model.result import Result
from _query import get_original_k_by_index

t1 = time.time()

# 大级别分型突破策略，连续4个中继分型

stocks_0 = fractal(-1, '4_1', 'fractal_flag') == 1
stocks_0 = fractal(-2, '4_1', 'fractal_flag', stocks_0) == -1
stocks_0 = fractal(-3, '4_1', 'fractal_flag', stocks_0) == 1
stocks_0 = fractal(-4, '4_1', 'fractal_flag', stocks_0) == -1

stocks_1_1 = fractal(-1, '4_1', 'eigen_chan_kline_index', stocks_0)
stocks_1_2 = fractal(-2, '4_1', 'eigen_chan_kline_index', stocks_1_1)
stocks_1_3 = fractal(-3, '4_1', 'eigen_chan_kline_index', stocks_1_2)
stocks_1_4 = fractal(-4, '4_1', 'eigen_chan_kline_index', stocks_1_3)

# stocks_2_1 = get_original_k_by_index(stocks_1_1, '4_1', 'low')
# stocks_2_2 = get_original_k_by_index(stocks_1_2, '4_1', 'high')
# stocks_2_3 = get_original_k_by_index(stocks_1_3, '4_1', 'low')
# stocks_2_4 = get_original_k_by_index(stocks_1_4, '4_1', 'high')

# stocks_3_1 = original_k(-1, '4_1', 'index', stocks_0)
# stocks_4 = stocks_3_1 - stocks_1_4 - 1

ret = {}
for k, v in stocks_1_4.items:
    max_index = chan_k(-1, '4_1', 'index', [k]).values
    close_price = []
    for i in range(max_index - v - 1):
        close_price.append(get_original_k_by_index(Result({k: v + i}), '4_1', 'close').values)
    max_close = max(close_price)
    ret[k] = max_close

stocks_5 = Result(ret)
stocks_5 = stocks_5 / float(10000)

# print stocks_5
# print '################'

stocks_6 = original_k(-2, '2_1', 'close') < stocks_5
stocks_7 = original_k(-1, '2_1', 'close') > stocks_5

print stocks_6 & stocks_7
# print stocks_7

print time.time() - t1
