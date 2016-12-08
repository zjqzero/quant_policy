# coding:utf-8
# 最后一个level2向上中枢+最后一个level1向上中枢+最后一个level0向上中枢
# 最后一颗原K线收盘价除以最后一个level2中枢的GG >= 0.95
# 最后一颗原K线收盘价除以最后一个level2中枢的GG <= 1.05

import talib as ta
import numpy as np
import time
from datetime import datetime
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
# from _query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, get_original_k_by_index

t1 = time.time()

print 'START {}'.format(datetime.now())

# stocks_1_1 = level2(-1, '1_1', 'direction') == -1

stocks_2_1 = centre(-1, '1_1', 'direction', '2') == -1
stocks_2_2 = centre(-2, '1_1', 'direction', '2') == 1

stocks_3_1 = centre(-1, '1_1', 'direction', '1') == -1
stocks_3_2 = centre(-2, '1_1', 'direction', '1') == 1

stocks_4_1 = centre(-1, '1_1', 'direction', '0') == -1
stocks_4_2 = centre(-2, '1_1', 'direction', '0') == 1

stocks_5 = stocks_4_1 & stocks_4_2 & stocks_3_1 & stocks_3_2 & stocks_2_1 & stocks_2_2

stocks_6_1 = original_k(-1, '2_1', 'close', stocks_5)
stocks_6_2 = centre(-1, '1_1', 'gg', '2', stocks_5)

print (stocks_6_1 / stocks_6_2 > 0.92) & (stocks_6_1 / stocks_6_2 < 1.00)

print time.time() - t1
# 获取特定K线需要提供函数

# Result 对象对datetime的dump出问题