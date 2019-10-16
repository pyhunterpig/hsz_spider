# -*- coding:utf-8 -*
import datetime
import time
from urllib import parse
from flask import Flask, request, jsonify
from flask_cors import *

from database.sql_test import session, HSZCOMPANY
from manage_task import start_spider

# REDIS_GZ = RedisDB()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

global null

null = ''

"""electron数据轮询"""


@app.route('/task_state', methods=['POST'])
def getjg():
    user_info = dict(request.args)
    result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == user_info['userid'],
                                              HSZCOMPANY.usereventually != 0).first()
    autowork = result.autowork
    if autowork != 'taskfailed' and autowork != 'taskworking' and autowork == 'accpmplish' and result.usereventually != datetime.datetime.now().strftime(
            '%Y%m'):
        start_spider(userId=user_info['userid'])
        session.execute(
            'update {} set autowork="taskworking" where userId = "{}" and usereventually!=0'.format(
                'hszcompany', user_info['userid']))
        return 'taskworking'
    else:
        return autowork


@app.route('/distribute', methods=['POST'])
def getgz():
    userinfo = dict(request.args)
    dict_forms = {}
    for k in dict(request.form):
        dict_forms = eval(k)
    for dict_form in dict_forms:
        result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userinfo['userId'],
                                                  HSZCOMPANY.usereventually != 0).first()
        if result:
            datetimenowTime = datetime.datetime.now().strftime('%Y%m')
            if result.usereventually == datetimenowTime:
                return 'nextmonth'
        else:
            result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userinfo['userId']
                                                      ).first()
            if result:
                continue
            else:
                for i in range(2):
                    if i == 0:
                        result = HSZCOMPANY(
                            userId=userinfo['userId'], userName=userinfo['userName'], zjxxName=userinfo['zjxxName'],
                            autowork=1,
                            ztId=0, id_num=0, headers=1, usereventually=1, endkjqj=0, eventuallykjqj=0, startkjqj=0,
                            content=0,
                            eventually_work=0)
                    elif i == 1:
                        result = HSZCOMPANY(
                            userId=userinfo['userId'], userName=userinfo['userName'], zjxxName=userinfo['zjxxName'],
                            autowork=0,
                            ztId=dict_form['ztId'], id_num=dict_form['id'], headers=0, usereventually=0, endkjqj=1,
                            eventuallykjqj=1, startkjqj=0, content=0, eventually_work=1)
                    session.add(result)
                    session.commit()
                session.close()
    return 'tasking'


"""api接口"""


@app.route('/getAllCustomers', methods=['POST'])
def getAllCustomers():
    resp = {
        "code": "",
        "userName": "",
        "userId": "",
        "data": [],
        "lang": "zh_CN",
        "msg": "",
        "localtime": ""
    }
    try:
        userId = dict(request.args)['userId']
        print(userId)
        result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId,
                                                  HSZCOMPANY.endkjqj != 0).all()
        infos = []
        for i in result:
            info = {}
            info['userId'] = i.userId
            info['ztId'] = i.ztId
            info['name'] = '上海商贸有限公司'
            info['endkjqj'] = i.endkjqj
            info['startkjqj'] = '201806'
            infos.append(info)
        resp['data'] = infos
        resp['code'] = "0"
        resp['msg'] = 'success'
        resp['localtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return jsonify(resp)
    except Exception as e:
        resp['code'] = -1
        resp['msg'] = "未知错误"
        return jsonify(resp)


@app.route('/queryYeb', methods=['POST'])
def queryYeb():
    resp = {
        "code": "",
        "companyName": "",
        "zztId": "",
        "data": [],
        "total": {},
        "lang": "zh_CN",
        "msg": ""
    }
    try:
        userId = dict(request.args)['userId']
        ztZtxxId = dict(request.args)['ztZtxxId']
        Kjqj = dict(request.args)['KjQj']
        result = session.query(HSZCOMPANY).filter(HSZCOMPANY.userId == userId,
                                                  HSZCOMPANY.ztId == ztZtxxId,
                                                  HSZCOMPANY.startkjqj == Kjqj).all()
        infos = []
        for i in result:
            info = {}
            info['userId'] = i.userId
            info['ztId'] = i.ztId
            info['content']=dict(parse.parse_qsl(i.content))
            infos.append(info)
            print(infos)
        resp['data'] = infos
        resp['code'] = "0"
        resp['msg'] = 'success'
        resp['companyName'] = '上海商贸有限公司'
        return jsonify(resp)
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "未知错误"
        return jsonify(resp)


app.run(port=5060, debug=True, host='127.0.0.1')
