# coding: utf-8

# 月线向下一笔 周线向下一笔 最后一个分型是底分型 底分型距离当下只有1颗K线
import talib as ta
import numpy as np
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
from model.result import Result

stocks2 = bi(-1, '3_1', 'direction') == -1
stocks3 = bi(-1, '4_1', 'direction') == -1
stocks4 = fractal(-1, '3_1', 'fractal_flag') == -1

stocks5 = fractal(-1, '3_1', 'eigen_chan_kline_index')
stocks6 = chan_k(-1, '3_1', 'index') - stocks5 <= 1

print stocks2 & stocks3 & stocks4 & stocks6
