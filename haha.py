from database_cookies.sql_test import session, HSZCOMPANY
from urllib import parse
from urllib.request import urlopen
from urllib import request

# headers={'Host': 'sap.kungeek.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) yct/1.0.3 Chrome/73.0.3683.121 Electron/5.0.6 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://sap.kungeek.com/portal/ftsp/portal/home.do?main&useridx=4E06FEE71A5E4AA393F509DB16BC8A32', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN', 'Cookie': 'URI=/portal/ftsp/portal/form.do; route=65b0be2280cd89589218aa98bdebc22e; JSESSIONID=D1D791AFC3F86122C59018D9A16F7E10'}
# dict1 = {'pid': 1375, 'type': 'cpu', 'resource': 2048}
#
#
# data = parse.urlencode(headers)
# print(type(data))
# print(data)
# userId="4E06FEE71A5E4AA393F509DB16BC8A32"
# res = dict(parse.parse_qsl(data))
# print(res)
# headers=3
#
# session.execute('update {} set headers="{}" where userId = "{}" and state!=0'.format('hszcompany',data,userId))
#
# session.close()

userId='4E06FEE71A5E4AA393F509DB16BC8A32'
print(userId)
result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId,
                                              HSZCOMPANY.eventuallykjqj != 0).all()
headers = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId, HSZCOMPANY.headers == 0).first()
print(headers.headers)