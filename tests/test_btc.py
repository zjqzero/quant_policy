# coding:utf-8
from datetime import datetime

from database import client
from infrastructure.btc_query import SingleQuery

btc_query = SingleQuery(client, 'btc_chan', 'OKCOIN.SH')

print btc_query.bi(-1, '1_1').start_time

date = datetime.strptime('2017-01-10 13:50:00', '%Y-%m-%d %H:%M:%S')
print btc_query.bi_from('1_1', date)

# if stocks1:
#     stocks2 = bi(-1, '1_1', 'direction', stocks1) == 1
#     if stocks2 and state == 1:
#         state = 0
#         print 'sell'
#     stocks3 = bi(-1, '1_1', 'direction', stocks1) == -1
#     if stocks3 and state == 0:
#         state = 1
#         print 'buy'
