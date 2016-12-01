# coding:utf-8
import talib as ta
import numpy as np
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
from model.result import Result

stocks1 = bi(-1, '2_1', 'direction') == -1
stocks2 = bi(-1, '2_1', 'chankline_index_list')
stocks3 = stocks2 & stocks1
ret = {}
for wind_code, amount in stocks3.items:
    ret[wind_code] = amount[-1]

# print chan_k(-1, '2_1', 'index')

stock4 = (chan_k(-1, '2_1', 'index') - Result(ret) + 1) * 240

ret = {}
for wind_code, amount in stock4.items:
    price_amount = history(wind_code, '1_1', 'close', amount)
    ma5 = mean(price_amount, time_period=5)
    ma8 = mean(price_amount, time_period=8)
    ma13 = mean(price_amount, time_period=13)
    ma21 = mean(price_amount, time_period=21)
    ma34 = mean(price_amount, time_period=34)
    ma55 = mean(price_amount, time_period=55)
    ma89 = mean(price_amount, time_period=89)
    ma144 = mean(price_amount, time_period=144)
    max_ma = max(ma5.values[-1], ma8.values[-1], ma13.values[-1], ma21.values[-1],
                 ma34.values[-1], ma55.values[-1], ma89.values[-1], ma144.values[-1])
    min_ma = min(ma5.values[-1], ma8.values[-1], ma13.values[-1], ma21.values[-1],
                 ma34.values[-1], ma55.values[-1], ma89.values[-1], ma144.values[-1])

    print wind_code, max_ma, min_ma


# 实现对result max min
