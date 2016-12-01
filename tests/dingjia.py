# coding:utf-8
# 定价权

import talib as ta
import numpy as np
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
from model.result import Result

# stock1 = original_k(-1, '2_1', 'open') == original_k(-1, '2_1', 'low')
#
# stock2 = original_k(-2, '2_1', 'open') == original_k(-2, '2_1', 'low')
#
stock3 = original_k(-1, '2_1', 'high') > original_k(-1, '2_1', 'low')

stock1 = original_k(-1, '2_1', 'low') == original_k(-2, '2_1', 'low')

stock2 = original_k(-2, '2_1', 'low') == original_k(-3, '2_1', 'low')

print stock1 & stock2 & stock3
