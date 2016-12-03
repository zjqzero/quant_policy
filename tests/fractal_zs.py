# coding:utf-8
import talib as ta
import numpy as np
import time
# from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
from _query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, get_original_k_by_index

# 月线级别，最后一个底分型；最后4个分型形成 低-1>低-3 高-2>高-4 结构，且当前K线距离最后分型的特征K线<=1
stocks0 = fractal(-1, '4_1', 'fractal_flag') == -1
stocks1 = fractal(-1, '4_1', 'eigen_chan_kline_index', stocks0)
stocks2 = fractal(-2, '4_1', 'eigen_chan_kline_index', stocks1)
stocks3 = fractal(-3, '4_1', 'eigen_chan_kline_index', stocks2)
stocks4 = fractal(-4, '4_1', 'eigen_chan_kline_index', stocks3)

stocks1_1 = get_original_k_by_index(stocks1, '4_1', 'low')
stocks2_1 = get_original_k_by_index(stocks2, '4_1', 'high')
stocks3_1 = get_original_k_by_index(stocks3, '4_1', 'low')
stocks4_1 = get_original_k_by_index(stocks4, '4_1', 'high')

stocks5 = chan_k(-1, '4_1', 'index') - stocks1 <= 1

print (stocks4_1 < stocks2_1) & (stocks3_1 < stocks1_1) & stocks5 & stocks0


# 获取特定K线需要提供函数
