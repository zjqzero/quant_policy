# coding:utf-8
import talib as ta
import numpy as np
from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, history, std, mean
from model.result import Result

all_stocks = {'600000.SH', '603009.SH', '002751.SZ', '600006.SH', '300055.SZ', '600054.SH'}

from database import client


a = [e for e in client.chan.chankline.find()]

print len(a)