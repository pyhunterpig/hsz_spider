from database.sql_test import session, HSZCOMPANY
from urllib import parse

import datetime
userId="4E06FEE71A5E4AA393F509DB16BC8A32"

result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId,
                                              HSZCOMPANY.usereventually != 0).first()
autowork = result.autowork

# autowork='accomplish'
print(result.userId,result.usereventually,result.autowork)
if autowork != 'taskfailed' and autowork != 'taskworking' and autowork == 'accpmplish' and result.usereventually != datetime.datetime.now().strftime('%Y%m'):
    autowork='accomplish'

    session.execute(
        'update {} set autowork="{}" where userId = "{}" and usereventually!=0'.format('hszcompany', autowork, userId))
    session.close()


    print('taskworking')






# result = session.query(HSZCOMPANY).filter_by(userId=userId).first()
# print(result.headers)
#
# headers = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId, HSZCOMPANY.headers.like('%{0}%'.format("sap"))).first().headers
# headers=dict(parse.parse_qsl(headers))
# print(headers)
# import requests

# headers={'Host': 'sap.kungeek.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) yct/1.0.3 Chrome/73.0.3683.121 Electron/5.0.6 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://sap.kungeek.com/portal/ftsp/portal/home.do?main&useridx=4E06FEE71A5E4AA393F509DB16BC8A32', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN', 'Cookie': 'URI=/portal/ftsp/portal/qyzHome.do; route=209e6eabe3215c79720fe09de423df3f; JSESSIONID=2CD0B2F5BA6D0972BF8B4E92A20798A5','X-CSRF-TOKEN': 'f72831cd-a1e8-4a53-aee0-0907415f13e9'}


payload={'ztZtxxId': 'G1390017666642739215307832600000', 'khxxId': '54FFD672883A4C758E50229972C83496'}
x=requests.post(url='https://sap.kungeek.com/portal/ftsp/portal/khxx.do?handleCustomer',data=payload,verify=False,headers=headers)
print(x.json())
