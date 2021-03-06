# coding:utf-8
import talib as ta
import numpy as np
import time
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
# from _query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, get_original_k_by_index

t1 = time.time()
# 月线级别，最后一个底分型；最后4个分型形成 低-1>低-3 高-2>高-4 结构，且当前K线距离最后分型的特征dK线<=1
# stocks_1 = centre(-1, '2_1', 'direction') == -1
stocks_2 = level2(-1, '1_1', 'direction') == -1
stocks_3 = level2(-1, '1_1', 'end_time', stocks_2)

stocks_4_1 = centre(-1, '1_1', 'direction', '2', stocks_3) == -1
stocks_4_2 = centre(-2, '1_1', 'direction', '2', stocks_4_1) == 1

stocks_5_1 = (centre(-1, '1_1', 'zg', '2', stocks_4_2) + centre(-1, '1_1', 'zd', '2', stocks_4_2)) / 2
stocks_5_2 = (centre(-2, '1_1', 'zg', '2', stocks_4_2) + centre(-2, '1_1', 'zd', '2', stocks_4_2)) / 2
stocks_6 = stocks_5_1 > stocks_5_2

stocks_7_1 = centre(-1, '1_1', 'gg', '2', stocks_4_2)

stocks_8_1 = original_k(-1, '2_1', 'close', stocks_6) > stocks_7_1
stocks_8_2 = original_k(-2, '2_1', 'close', stocks_6) < stocks_7_1

print stocks_8_1 & stocks_8_2

print time.time() - t1
# 获取特定K线需要提供函数

# Result 对象对datetime的dump出问题