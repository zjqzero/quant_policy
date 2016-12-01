import talib as ta
import numpy as np
import time
# from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
from _query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre
from model.result import Result

t1 = time.time()
stocks1 = bi(-1, '2_1', 'direction') == -1
stocks2 = bi(-1, '2_1', 'chankline_index_list')

ret = {}
for wind_code, v in stocks2.items:
    ret[wind_code] = v[-1]

last_index = Result(ret)

stock3 = chan_k(-1, '2_1', 'index') - last_index <= 1
stock5 = chan_k(-3, '2_1', 'inclusive') == 0

stock4 = original_k(-1, '2_1', 'close') / original_k(-1, '2_1', 'open') > 1.03

stock6 = original_k(-3, '2_1', 'open') / original_k(-3, '2_1', 'close') > 1

stock7 = stock4 > stock6

print stock4 & stock3 & stock5 & stock7

print time.time() - t1
