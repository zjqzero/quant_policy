# coding:utf-8

# 最后一个分型是顶分型，距离当前大于10个k线
import talib as ta
import numpy as np
import time
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean

t1 = time.time()

stocks0 = fractal(-1, '2_1', 'fractal_flag') == 1
stocks1 = fractal(-1, '2_1', 'eigen_chan_kline_index', stocks0)

stocks2 = chan_k(-1, '2_1', 'index')

stocks3 = (stocks2 - stocks1) > 10

print stocks3

print time.time() - t1
# 获取特定K线需要提供函数
