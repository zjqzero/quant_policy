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
    c1_amount = history(wind_code, '1_1', 'close', amount)
    c2_amount = history(wind_code, '1_1', 'close', amount, end=-1)
    c_ratio = c1_amount / c2_amount
    s = std(c_ratio, time_period=amount)
    m = mean(c_ratio, time_period=amount)
    result = c_ratio > m + s * 3
    for k, v in result.items:
        if v[-1]:
            ret[k] = v

c_result = Result(ret)
ret = {}
for wind_code, amount in stock4.items:
    volume_amount = history(wind_code, '1_1', 'volume', amount)
    s = std(volume_amount, time_period=amount)
    m = mean(volume_amount, time_period=amount)
    result = volume_amount > m + s * 3
    for k, v in result.items:
        if v[-1]:
            ret[k] = v
v_result = Result(ret)

print c_result & v_result
