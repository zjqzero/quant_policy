# coding:utf-8
import talib as ta
import numpy as np
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
from model.result import Result

price_amount = history('002695.SZ', '2_1', 'close', 1000)
ma5 = mean(price_amount, time_period=5)
ma8 = mean(price_amount, time_period=8)
ma13 = mean(price_amount, time_period=13)
ma21 = mean(price_amount, time_period=21)
ma34 = mean(price_amount, time_period=34)
ma55 = mean(price_amount, time_period=55)
ma89 = mean(price_amount, time_period=89)
ma144 = mean(price_amount, time_period=144)
ma233 = mean(price_amount, time_period=233)

result = []
for i in range(230):
    j = -1 - i
    max_ma = max(ma5.values[j], ma8.values[j], ma13.values[j], ma21.values[j],
                 ma34.values[j], ma55.values[j], ma89.values[j], ma144.values[j],
                 ma233.values[j])
    min_ma = min(ma5.values[j], ma8.values[j], ma13.values[j], ma21.values[j],
                 ma34.values[j], ma55.values[j], ma89.values[j], ma144.values[j],
                 ma233.values[j])

    result.append(max_ma / min_ma)


result = result[66:]

_mean = sum(result) / len(result)
v = np.array(result)
print min(result)
print _mean
print ta.STDDEV(v, timeperiod=164)[-1]
# 实现对result max min
