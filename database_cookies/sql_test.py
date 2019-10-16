# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SURL = "mysql+pymysql://cic_admin:TaBoq,,1234@192.168.1.170:3306/hsz_system?charset=utf8&autocommit=true"
SURL = "mysql+pymysql://root:root@localhost:3306/hsz_system?charset=utf8&autocommit=true"
engine = create_engine(SURL)  # 定义引擎
Base = declarative_base()
session = sessionmaker(engine)()


class HSZCOMPANY(Base):
    __tablename__ = 'hszcompany'
    id = Column(Integer, primary_key=True)
    userId = Column(String(40))
    userName = Column(String(20))
    zjxxName = Column(String(20))
    autowork = Column(String(20))
    ztId = Column(String(50))
    id_num = Column(String(50))
    headers = Column(String(1000))
    usereventually = Column(String(20))
    endkjqj = Column(String(20))
    eventuallykjqj = Column(String(20))
    startkjqj = Column(String(20))
    content = Column(String(1000))
    eventually_work = Column(String(20))

Base.metadata.create_all(engine)

