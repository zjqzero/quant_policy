# coding:utf-8
import talib as ta
import numpy as np
import time
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
# from _query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, get_original_k_by_index

t1 = time.time()
# 月线级别，最后一个底分型；最后4个分型形成 低-1>低-3 高-2>高-4 结构，且当前K线距离最后分型的特征K线<=1
# stocks_1 = centre(-1, '2_1', 'direction') == -1
stocks_2 = level2(-1, '1_1', 'direction') == -1
stocks_3 = level2(-1, '1_1', 'end_time', stocks_2)

print stocks_3

print time.time() - t1
# 获取特定K线需要提供函数

# Result 对象对datetime的dump出问题