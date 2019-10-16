from database.sql_test import session, HSZCOMPANY
userId='4E06FEE71A5E4AA393F509DB16BC8A32'
xxx="""id=G1390017670417621815307832600000&ztZtxxId=G1390017666642739215307832600000&ztKjkmId=G1390017670417621815307832600000&qcYe=-790.24&qmYe=2123.45&jfLj=1919.59&dfLj=4833.28&qcYeYb=0.0&qmYeYb=0.0&jfLjYb=0.0&dfLjYb=0.0&kjQj=201806&yeFx=0&currentYe=0.0&kmMc=%E5%BA%94%E4%BA%A4%E7%A8%8E%E8%B4%B9&kmDm=2221&wldwLx=0&yearJfLj=25249.57&yearDfLj=4833.28&yearJfLjYb=0.0&yearDfLjYb=0.0&generateFlag=0&showFlag=1&sortKey=0&level=1&jfQc=0.0&dfQc=-790.24&jfQcYb=0.0&dfQcYb=0.0&jfQm=0.0&dfQm=2123.45&jfQmYb=0.0&dfQmYb=0.0"""
from urllib import parse
yyy=dict(parse.parse_qsl(xxx))
print(yyy)





# ztId='G1390017666642739215307832600000'
# date='201910'
# eventually_works = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId,
#                                                                 HSZCOMPANY.ztId == ztId,
#                                                                 HSZCOMPANY.eventuallykjqj != 0).all()
# for eventually_work in eventually_works:
#     print(eventually_work.eventually_work,date)
#     if eventually_work.eventually_work == date:
#         session.execute(
#     'update {} set state="{}" , autowork="accomplish" where userId = "{}" and autowork!=0'.format(
#         'hszcompany', date, userId))
#     else:
#         print(eventually_work.userId
# )

# for i in range(10):
#     result = HSZCOMPANY(
#         userId=userId, userName='小王', zjxxName='悲哀', autowork=1,
#         ztId=0, id_num=0, headers=1, state=1, endkjqj=0, eventuallykjqj=0, startkjqj=0, content=0, eventually_work=0)
#     session.add(result)
# session.commit()
# session.close()