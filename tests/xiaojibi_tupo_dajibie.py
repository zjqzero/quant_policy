# coding:utf-8
import talib as ta
import numpy as np
import time
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean

# from _query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, get_original_k_by_index

t1 = time.time()

# 小级别突破大级别中枢

stocks_1_1 = duan(-1, '1_1', 'direction') == -1

stocks_2_1 = duan(-1, '1_1', 'low', stocks_1_1)
stocks_2_2 = duan(-1, '1_1', 'high', stocks_1_1)
stocks_2_3 = duan(-3, '1_1', 'low', stocks_1_1)
stocks_2_4 = duan(-3, '1_1', 'high', stocks_1_1)
stocks_2_5 = duan(-4, '1_1', 'low', stocks_1_1)

stocks_3_1 = bi(-1, '2_1', 'direction', stocks_1_1) == -1
stocks_3_2 = bi(-1, '2_1', 'low', stocks_1_1)
stocks_3_3 = bi(-1, '1_1', 'low')

stocks_4_1 = stocks_2_1 > stocks_3_2
stocks_4_2 = stocks_2_3 > stocks_3_2
stocks_4_3 = stocks_2_5 == stocks_3_2
stocks_4_4 = stocks_2_1 == stocks_3_3

stocks_5 = stocks_4_1 & stocks_4_2 & stocks_4_3 & stocks_4_4


stocks_6 = original_k(-1, '1_1', 'close', stocks_5)

print (stocks_6 > stocks_2_2) > stocks_2_4

print time.time() - t1

