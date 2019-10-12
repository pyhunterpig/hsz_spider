# -*- coding:utf-8 -*
import datetime

from flask import Flask, request
from flask_cors import *

from database.sql_test import session, HSZCOMPANY
from manage_task import start_spider

# REDIS_GZ = RedisDB()
app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

global null

null = ''


@app.route('/task_state', methods=['POST'])
def getjg():
    user_info = dict(request.args)
    result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId==user_info['userId'],HSZCOMPANY.state!=0).first()
    if result.autowork == 'unable':
        return 'task_failed'
    elif result.autowork == 'able':
        return 'task_working'
    elif result.autowork == 'accomplish':
        return 'task_accomplish'
    else:
        start_spider(userId=user_info['userId'], cookies=result.headers)
        try:
            session.execute(
                'update {} set autowork="able" where userId = "{}"'.format(
                    'hszcompany', user_info['userId']))
        except Exception as e:
            session.rollback()
            session.close()
        else:
            return 'task_working'


@app.route('/distribute', methods=['POST'])
def getgz():
    userinfo = dict(request.args)
    result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userinfo['userId'],
                                              HSZCOMPANY.state.like('%{0}%'.format("完成"))).first()
    if result:
        datetimenowTime = datetime.datetime.now().strftime('%Y%m')
        state = result.state
        date = state.split('|')[0]
        if date == datetimenowTime:
            return 'next month'
    else:
        for i in range(2):
            if i == 0:
                result = HSZCOMPANY(
                    userId=userinfo['userId'], userName=userinfo['userName'], zjxxName=userinfo['zjxxName'], autowork=1,
                    ztId=0, id_num=0, headers=1, state=1,  endkqj=0,eventuallykjqj=0,startkjqj=0,content=0,eventually_work=0)
            elif i == 1:
                result = HSZCOMPANY(
                    userId=userinfo['userId'], userName=userinfo['userName'], zjxxName=userinfo['zjxxName'], autowork=0,
                    ztId=userinfo['ztid'], id_num=userinfo['id'], headers=0, state=0, endkqj=1,eventuallykjqj=1,startkjqj=0,content=0,eventually_work=1)
        session.add(result)
        session.commit()
        session.close()
        return 'tasking'


# @app.route('/getgzrender', methods=['GET'])
# def getgzrender():
#     x = str(datetime.datetime.now().strftime('%Y%m%d'))
#     result = session.query(YCTGZACCOUNT).filter(YCTGZACCOUNT.time_scope != x).all()
#     for i in result:
#         for n in range(3):
#             try:
#                 session.execute(
#                     'update {} set time_scope={} , complete_state="未完成" , unlock_state="未锁定" where account = "{}"'.format(
#                         'yctaccount', x,
#                         i.account))
#                 session.close()
#                 break
#             except:
#                 session.rollback()
#                 session.close()
#                 if i == 2:
#                     return '后台错误,请联系后台'
#     for i in range(3):
#         try:
#             result = session.query(YCTGZACCOUNT).filter_by(complete_state='未完成').first()
#             session.close()
#             break
#         except:
#             session.rollback()
#             session.close()
#             if i == 2:
#                 return '后台错误,请联系后台'
#     lists = []
#     if result:
#         if result.unlock_state == '未锁定':
#             # print(result.account)
#             # print(result.unlock_state)
#             for n in range(3):
#                 try:
#                     session.execute(
#                         'update {} set unlock_state="锁定" where account = "{}"'.format(
#                             'yctaccount', result.account))
#                     session.close()
#                     break
#                 except:
#                     session.rollback()
#                     session.close()
#                     if n == 2:
#                         return '后台错误,请联系后台'
#         for i in range(3):
#             try:
#                 result = session.query(YCTGZACCOUNT).filter_by(complete_state='未完成').all()
#                 session.close()
#                 break
#             except:
#                 session.rollback()
#                 session.close()
#                 if i == 2:
#                     return '后台错误,请联系后台'
#         for x, y in enumerate(result):
#             dicts = {}
#             dicts['account'] = y.account
#             dicts['password'] = y.password
#             dicts['complete_state'] = y.complete_state
#             dicts['id'] = x
#             dicts['time_scope'] = y.time_scope
#             dicts['unlock'] = y.unlock_state
#             lists.append(dicts)
#         res = {'code': 0, 'data': lists, 'count': len(lists)}
#         return json.dumps(res)
#     else:
#         return '1'
#
#
# @app.route('/getrecord', methods=['POST'])
# def getrecord():
#     account = request.form.get('account')
#     username = request.form.get('username')
#     result = ''
#     for i in range(3):
#         try:
#             result = session.query(YCTGZACCOUNT).filter(YCTGZACCOUNT.account == account).first()
#             session.close()
#             if not result:
#                 return '账号错误'
#             if result.unlock_state == '未锁定':
#                 return '请填写锁定账号'
#         except:
#             session.rollback()
#             session.close()
#             if i == 2:
#                 return '后台错误,请联系后台'
#         else:
#             if result.complete_state == '完成':
#                 return '请不要重复提交'
#             else:
#                 break
#     man = ''
#     for i in range(3):
#         try:
#             man = session.query(YCTGZWORKERMAN).filter(YCTGZWORKERMAN.username == username).first()
#             session.close()
#             if not man:
#                 return '工作人员错误'
#             break
#         except:
#             session.rollback()
#             session.close()
#             if i == 2:
#                 return '后台错误,请联系后台'
#     if result and man:
#
#         for z in range(3):
#             try:
#                 session.execute(
#                     'update {} set complete_state="完成",unlock_state="未锁定" where account = "{}"'.format('yctaccount',
#                                                                                                        result.account))
#                 session.close()
#                 break
#             except Exception as e:
#                 session.rollback()
#                 session.close()
#                 if z == 2:
#                     return '后台错误,请联系后台,1'
#         x = str(datetime.datetime.now().strftime('%Y%m%d'))
#         for z in range(3):
#             try:
#                 result = YCTGZRECORDER(username=username, account=account, time_scope=x, complete_state='完成')
#                 session.add(result)
#                 session.commit()
#                 session.close()
#                 break
#             except:
#                 session.rollback()
#                 session.close()
#                 if z == 2:
#                     return '后台错误,请联系后台,2'
#         return '1'
#     elif not result:
#         return '后台没有账号信息，请正确填写'
#     elif not man:
#         return '后台没有完成人信息,请联系后台验证'
#
#
# @app.route('/getpage', methods=['POST'])
# def getres():
#     # print('getpage, 14 row')
#     # 好的情况下返回的网址
#     '''从redis中获取当前页和所谓的总页数'''
#     result = REDIS_GZ.hget('specify_account_yctAppNo_page')
#     # 有可能换成cookies的方式
#     if result['getpage'] == result['total']:
#         data = {'page': 1}
#         # print(data, '21 row')
#         return json.dumps(data)
#     else:
#         data = {'page': 0}
#         # print(data, '24 row')
#         return json.dumps(data)
#
#
# @app.route('/geturls', methods=['GET', 'POST'])
# def geturls():
#     # print(request.cookies, '32 low')
#     tbcg = request.cookies.get('task', '')
#     if tbcg:
#         # print('redirect to gettbcg 33 row')
#         return redirect(url_for('gettbcg'))
#     specify_account_yctAppNo = REDIS_GZ.hget('specify_account_yctAppNo')
#     if specify_account_yctAppNo:
#         for yctAppNo in specify_account_yctAppNo:
#             if '退回修改' in specify_account_yctAppNo[yctAppNo]:
#                 url = 'http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/print?yctAppNo={}'.format(yctAppNo)
#                 data = {'urls': url, 'task': 'thxg'}
#                 # print(data, '41 row')
#                 return json.dumps(data)
#             elif '填报成功' in specify_account_yctAppNo[yctAppNo]:
#                 # print(yctAppNo, 'yctappno')
#                 # 前端能在页面判断是否有填报成功
#                 url = 'http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/print?yctAppNo={}'.format(yctAppNo)
#                 data = json.dumps({'urls': url, 'task': 'tbcg'})
#                 resp = make_response(data)
#                 resp.set_cookie('task', 'tbcg')
#                 return resp
#                 # return json.dumps(data)
#     else:
#         data = {'urls': '', 'task': 'end'}
#         REDIS_GZ.hset('specify_account_yctAppNo_page', {'getpage': '-1', 'total': '-2'})
#         return json.dumps(data)
#
#
# @app.route('/gettbcg', methods=['GET'])
# def gettbcg():
#     # print('gettbcg 57 low')
#     specify_account_yctAppNo = REDIS_GZ.hget('specify_account_yctAppNo')
#     for yctAppNo in specify_account_yctAppNo:
#         results = REDIS_GZ.hget('specify_account_tbcg_' + yctAppNo)
#         # print(results, 'DDDDDDDDDDDDDDD')
#         if not results:
#             REDIS_GZ.hdel('specify_account_yctAppNo', yctAppNo)
#             resp = make_response(redirect(url_for('geturls')))
#             resp.set_cookie('task', '')
#             return resp
#         for result in results:
#             if len(result) > 15:
#                 id_, app_no = result.split('^')
#                 url = 'http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/content_special?id=-{}&p=1&app_no={}&papers={}&yctAppNo={}'.format(
#                     id_, app_no, result,
#                     yctAppNo)
#                 data = json.dumps({'urls': url, 'num': results.__len__()})
#                 if results.__len__() == 1:
#                     resp = make_response(data)
#                     resp.set_cookie('task', '')
#                 else:
#                     resp = make_response(data)
#                     resp.set_cookie('task', 'tbcg_source')
#                 return resp
#             else:
#                 url = 'http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/content?id=-{}&appendixStatus=&isPrint=1&p=1&papers={}&yctAppNo={}'.format(
#                     result, result, yctAppNo)
#                 data = json.dumps({'urls': url, 'num': results.__len__()})
#                 if results.__len__() == 1:
#                     resp = make_response(data)
#                     resp.set_cookie('task', '')
#                 else:
#                     resp = make_response(data)
#                     resp.set_cookie('task', 'tbcg_source')
#                 # print(data, '77 row')
#                 return resp


# /.virtualenvs/py3_flask
app.run(port=5060, debug=True, host='127.0.0.1')
