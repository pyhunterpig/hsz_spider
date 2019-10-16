from manage_task import start_spider
start_spider(userId='4E06FEE71A5E4AA393F509DB16BC8A32')

import datetime

# date = datetime.datetime.now().strftime('%Y%m')
# print(type(date))
# from database.sql_test import session, HSZCOMPANY
# kjqj,fwqxz,userId,ztId=("201806","201908","4E06FEE71A5E4AA393F509DB16BC8A32", "G1390017666642739215307832600000")
# # session.execute(
# #                 'update {} set eventuallykjqj="{}" and endkjqj="{}" where userId = "{}" and eventuallykjqj!=0 and ztId="{}"'.format(
# #                     'hszcompany', kjqj, fwqxz, userId, ztId))
# session.execute(
#                 'update {} set eventuallykjqj="{}" , endkjqj="{}" where userId = "{}" and eventuallykjqj!=0 and ztId="{}"'.format(
#                     'hszcompany', kjqj, fwqxz, userId, ztId))









from urllib import parse

# x={'id': 'G1390017670417614715307832600000', 'ztZtxxId': 'G1390017666642739215307832600000', 'ztKjkmId': 'G1390017670417614715307832600000', 'qcYe': 192473.11, 'qmYe': 191202.51, 'jfLj': 0.0, 'dfLj': 1270.6, 'qcYeYb': 0.0, 'qmYeYb': 0.0, 'jfLjYb': 0.0, 'dfLjYb': 0.0, 'kjQj': '201806', 'yeFx': '1', 'currentYe': 0.0, 'kmMc': '库存现金', 'kmDm': '1001', 'wldwLx': '0', 'yearJfLj': 30191.3, 'yearDfLj': 1270.6, 'yearJfLjYb': 0.0, 'yearDfLjYb': 0.0, 'generateFlag': 0, 'showFlag': 1, 'sortKey': 0, 'level': 1, 'jfQc': 192473.11, 'dfQc': 0.0, 'jfQcYb': 0.0, 'dfQcYb': 0.0, 'jfQm': 191202.51, 'dfQm': 0.0, 'jfQmYb': 0.0, 'dfQmYb': 0.0}
# z=parse.urlencode(x)
# print(z)
# m=dict(parse.parse_qsl(z))
# print(m)
# if m==x:
#     print(1)