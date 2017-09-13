# coding: utf-8

# 长笔， 最后一个level_1中枢

import talib as ta
import numpy as np
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean, \
    CHAN_MAPPING
from model.result import Result

stocks1 = bi(-1, '3_1', 'direction') == -1
stocks2 = bi(-1, '3_1', 'count_kline', stocks1) >= 20
stocks3 = bi(-1, '3_1', 'count_kline', stocks2) <= 25

stocks4 = centre(-1, '1_1', 'direction', '1', stocks3) == -1

print stocks4
