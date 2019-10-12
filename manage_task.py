# -*- coding: utf-8 -*-
import datetime

from huey import SqliteHuey

from database.sql_test import session, HSZCOMPANY
from downloader import Downloader
down = Downloader()
huey = SqliteHuey(filename='./manage.db')



# 除非大于本月或者不是才能入这里，所以当为本月的时候说明全部都采集完毕
@huey.task(retries=1)
def start_spider(userId):
    result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId,
                                              HSZCOMPANY.eventuallykjqj != 0).all()
    headers = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId, HSZCOMPANY.headers != 0).first().headers
    for zt in result:
        url = 'https://sap.kungeek.com/portal/ftsp/portal/khxx.do?handleCustomer'
        data = {'ztZtxxId': zt.ztId, 'khxxId': zt.id_num}
        account_date = down.visit(url=url, response_container=['json', 'utf-8'], method='post', data=data,
                                  headers=eval(headers))
        if account_date.get('data', None):
            fwqxz = account_date['data']['fwqxz']
            startkjqj = account_date['data']['qyQj']
            eventally = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId,
                                                         HSZCOMPANY.ztId == zt.ztId,
                                                         HSZCOMPANY.eventuallykjqj != 0).first()
            if eventally:
                if eventally.eventuallykjqj < eventally and eventally > '2000':
                    startkjqj = eventally.eventuallykjqj
                    account_date_poll(zt, headers, fwqxz, startkjqj, first=0)
                else:
                    return '*********轮训成功**********'
            else:
                startkjqj = startkjqj
                account_date_poll(zt, headers, fwqxz, startkjqj, first=1)


@huey.task(retries=1)
def rubbish_data(**kwargs):
    '''记录垃圾数据,有待下次重新做任务'''
    print(dict(kwargs), '我是垃圾')


def account_date_poll(zt, headers, fwqxz, startkjqj, first):
    '''账期轮训逻辑'''
    url = 'https://sap.kungeek.com/portal/ftsp/portal/balance.do?getYebWangLaiMx&funcCode=ftsp_zhangbu_balance'
    data = {'ztZtxxId': zt.ztId, 'startKjQj': startkjqj, 'endKjQj': startkjqj, 'cxwbkm': '0'}
    if startkjqj < fwqxz and first == 0:
        if startkjqj == '201912':
            kjqj = '202001'
        elif startkjqj == '202012':
            kjqj = '202101'
        elif startkjqj == '201812':
            kjqj = '201901'
        elif startkjqj == '201712':
            kjqj = '201801'
        elif startkjqj == '201612':
            kjqj = '201701'
        elif startkjqj == '201512':
            kjqj = '201601'
        elif startkjqj == '201412':
            kjqj = '201501'
        elif startkjqj == '201312':
            kjqj = '201401'
        elif startkjqj == '201212':
            kjqj = '201301'
        elif startkjqj == '201112':
            kjqj = '201201'
        else:
            kjqj = eval('{}+1'.format(startkjqj))
    else:
        kjqj = startkjqj
    data.update({'startKjQj': kjqj, 'endKjQj': kjqj})
    single_account_date = down.visit(url=url, response_container=['json', 'utf-8'], method='post', data=data,
                                     headers=headers)
    if single_account_date.get('data', 'None'):
        total = single_account_date['total']
        datas = single_account_date['data'].append(total)
        for i in datas:
            result = HSZCOMPANY(
                userId=zt.userId, userName=zt.userName, zjxxName=zt.zjxxName,
                autowork=0, ztId=zt.ztId, id_num=zt.id_num, headers=0, endkjqj=0, eventuallykjqj=0,
                startkjqj=startkjqj, content=str(i), eventually_work=0)
            session.add(result)
            session.commit()
            session.close()
        if kjqj < fwqxz:
            session.execute(
                'update {} set eventuallykjqj="{}" endkjqj="{}" where userId = "{}" and eventuallykjqj!=0 and ztId="{}"'.format(
                    'hszcompany', kjqj, fwqxz, zt.userId, zt.ztId))
            return account_date_poll(zt, headers, fwqxz, kjqj, first=0)
        else:
            date = datetime.datetime.now().strftime('%Y%m')
            session.execute(
                'update {} set eventuallykjqj="{}" endkjqj="{}"eventually_work="{}" where userId = "{}" and eventuallykjqj!=0 and ztId="{}"'.format(
                    'hszcompany', kjqj, fwqxz, date, zt.userId, zt.ztId))
            eventually_works = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == zt.userId,
                                                                HSZCOMPANY.ztId == zt.ztId,
                                                                HSZCOMPANY.eventuallykjqj != 0).all()
            for eventually_work in eventually_works:
                if eventually_work.eventually < date:
                    return
            session.execute(
                'update {} set state="{}" autowork="accomplish" where userId = "{}" and state!=0'.format(
                    'hszcompany', str(date) + '|完成', zt.userId))
            return "轮训成功"
    else:
        datetimenowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rubbish = {'userId': zt.userId, 'headers': headers, 'url': url, 'function': 'account_date_poll',
                   'time': datetimenowTime, 'webname': '慧算账', 'errMsg': single_account_date['errMsg'],
                   'account_time': kjqj, 'ztZtxxId': zt.ztId}
        rubbish_data(rubbish)
