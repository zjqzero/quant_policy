# coding:utf-8

from query import chan_k, original_k, fractal, bi, duan, level1, level2, level3, centre, get_price

# all_stocks = {'600000.SH', '603009.SH', '002751.SZ', '600006.SH', '300055.SZ', '600054.SH'}

# print fractal(-1, '2_1', 'fractal_flag', stocks=all_stocks) < 0
# print centre(-1, '1_1', 'gg', '1')
# print original_k(-1, '2_1', 'close') > 50
# print original_k(-1, '2_1', 'volume')
# print original_k(-1, '2_1', 'amount')
# print chan_k(-1, '2_1', 'shaped_high')
# data = chan_k(-1, '2_1', 'direction')
# data2 = chan_k(-1, '2_1', 'inclusive')
# data3 = chan_k(-1, '2_1', 'has_gap')
# data4 = chan_k(-1, '2_1', 'chankline_flag')

# print [e for e in data if data[e] == -1]
# print [e for e in data2 if data2[e] == 1]

# print set([e for e in data2 if data2[e] == -1]) & set([e for e in data2 if data2[e] == -1])
# print [e for e in data4 if data4[e] == -3]
# data5 = bi(-1, '2_1', 'high')
# print data5
# print '######## END #########'



# FLAG_FRACTAL_TOP = 1
# FLAG_FRACTAL_BOTTOM = -1
# FLAG_BI_TOP = 2
# FLAG_BI_BOTTOM = -2
# FLAG_DUAN_TOP = 3
# FLAG_DUAN_BOTTOM = -3
# FLAG_TREND_1_TOP = 4
# FLAG_TREND_1_BOTTOM = -4
# FLAG_TREND_2_TOP = 5
# FLAG_TREND_2_BOTTOM = -5
# FLAG_TREND_3_TOP = 6
# FLAG_TREND_3_BOTTOM = -6
# FLAG_TREND_4_TOP = 7
# FLAG_TREND_4_BOTTOM = -7
# FLAG_TREND_5_TOP = 8
# FLAG_TREND_5_BOTTOM = -8
# FLAG_TREND_6_TOP = 9
# FLAG_TREND_6_BOTTOM = -9


# 过滤最后一笔，日级别，k线数量大于20
# print bi(0, '2_1', 'count_kline') > 20

# 过滤最后一段，日级别，比的数量=3
# print duan(0, '2_1', 'count_subtrend') == 3

# 过滤比趋势背离，日级别
# stock1 = bi(0, '2_1', 'ratio') < bi(-2, '2_1', 'ratio')
# stock2 = bi(0, '2_1', 'shaped_high') < bi(-2, '2_1', 'shaped_high')
# stock3 = bi(0, '2_1', 'shaped_low') < bi(-2, '2_1', 'shaped_low')
# stock4 = (bi(-2, '2_1', 'ratio') / bi(0, '2_1', 'ratio')) >= 1.3
# stock5 = bi(0, '2_1', 'direction') == -1
# stock6 = bi(0, '2_1', 'count_fractal') > bi(-2, '2_1', 'count_fractal')
#
# print stock6 & stock2 & stock3 & stock5

# 600000 13年8月1号的收盘价跟行情软件不一致

print get_price('600000.SH', '2_1', 'close', 733)
