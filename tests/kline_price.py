# coding:utf-8

# 最后一笔向下，最后一颗k线形成底分型，最后一颗K线收盘价大于前5颗的价格
import talib as ta
import numpy as np
import time
# from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
from _query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre
from model.result import Result

t1 = time.time()
stocks1 = bi(-1, '2_1', 'direction') == -1
stocks2 = bi(-1, '2_1', 'chankline_index_list', stocks1)
stocks2_1 = bi(-1, '2_1', 'end_chan_k', stocks2)

stock3 = chan_k(-1, '2_1', 'index') - stocks2_1 <= 1
stock5 = chan_k(-3, '2_1', 'inclusive') == 0

stocks_9_0 = original_k(-1, '2_1', 'close', stock5)
stocks_9_1 = original_k(-2, '2_1', 'close', stock5)
stocks_9_2 = original_k(-3, '2_1', 'close', stock5)
stocks_9_3 = original_k(-4, '2_1', 'close', stock5)
stocks_9_4 = original_k(-5, '2_1', 'close', stock5)
stocks_9_5 = original_k(-6, '2_1', 'close', stock5)

stocks_10 = ((((stocks_9_0 > stocks_9_1) > stocks_9_2) > stocks_9_3) > stocks_9_4) > stocks_9_5

print stocks_10
print time.time() - t1
