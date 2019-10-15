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
    result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId==user_info['useridx'],HSZCOMPANY.state!=0).first()
    if result.autowork == 'unable':
        return 'task_failed'
    elif result.autowork == 'able':
        return 'task_working'
    elif result.autowork == 'accomplish':
        return 'task_accomplish'
    else:
        start_spider(userId=user_info['useridx'])
        try:
            session.execute(
                'update {} set autowork="able" where userId = "{}" and autowork!=0'.format(
                    'hszcompany', user_info['useridx']))
        except Exception as e:
            session.rollback()
            session.close()
        else:
            return 'task_working'


@app.route('/distribute', methods=['POST'])
def getgz():
    print(request.headers)
    userinfo = dict(request.args)
    print(userinfo)
    print(dict(request.form))
    dict_form={}
    for i in dict(request.form):
        dict_form=eval(i)[0]
    print(dict_form['id'])
    result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userinfo['userId'],
                                              HSZCOMPANY.state.like('%{0}%'.format("完成"))).first()
    if result:
        datetimenowTime = datetime.datetime.now().strftime('%Y%m')
        state = result.state
        date = state.split('|')[0]
        if date == datetimenowTime:
            return 'next month'
    result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userinfo['userId']
                                              ).first()
    if result:
        return 'tasking'
    else:
        for i in range(2):
            if i == 0:
                result = HSZCOMPANY(
                    userId=userinfo['userId'], userName=userinfo['userName'], zjxxName=userinfo['zjxxName'], autowork=1,
                    ztId=0, id_num=0, headers=1, state=1,  endkjqj=0,eventuallykjqj=0,startkjqj=0,content=0,eventually_work=0)
            elif i == 1:
                result = HSZCOMPANY(
                    userId=userinfo['userId'], userName=userinfo['userName'], zjxxName=userinfo['zjxxName'], autowork=0,
                    ztId=dict_form['ztId'], id_num=dict_form['id'], headers=0, state=0, endkjqj=1,eventuallykjqj=1,startkjqj=0,content=0,eventually_work=1)
            session.add(result)
            session.commit()
            session.close()
        return 'tasking'

app.run(port=5060, debug=True, host='127.0.0.1')
