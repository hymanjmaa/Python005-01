#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2020/12/9 23:03
"""
from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy import create_engine, Table, Float, Column, Integer, SmallInteger, DateTime, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime
from datetime import datetime


Base = declarative_base()
db_url = "mysql+pymysql://root:hymanjma@localhost/testdb?charset=utf8mb4"
engine = create_engine(db_url, echo=True, encoding="utf-8")
SessionClass = sessionmaker(bind=engine)
session = SessionClass()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(128))
    age = Column(SmallInteger)
    birth_day = Column(DateTime)
    gender = Column(SmallInteger)
    academic = Column(String(16))
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    def __repr__(self):
        return "User(user_id='{self.user_id}', " \
            "user_name={self.user_name})".format(self=self)


class TransferUser(Base):
    __tablename__ = 'transfer_user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(64))


class TransferUserAsset(Base):
    __tablename__ = 'transfer_user_asset'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    asset = Column(Float)


class TransferHistory(Base):
    __tablename__ = 'transfer_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_user_id = Column(Integer)
    to_user_id = Column(Integer)
    transfer_amount = Column(Float)
    transfer_time = Column(DateTime)


def homework_2():
    user_a = User(user_name='马云', age=56, birth_day=datetime.strptime('1964-09-10', '%Y-%m-%d'),
                  gender=1, academic='本科', create_time=datetime.utcnow(),
                  update_time=datetime.utcnow())
    session.add(user_a)

    user_b = User(user_name='马化腾', age=49, birth_day=datetime.strptime('1971-10-29', '%Y-%m-%d'),
                  gender=1, academic='本科', create_time=datetime.utcnow(),
                  update_time=datetime.utcnow())
    session.add(user_b)

    user_c = User(user_name='马明哲', age=65, birth_day=datetime.strptime('1955-12-01', '%Y-%m-%d'),
                  gender=1, academic='博士', create_time=datetime.utcnow(),
                  update_time=datetime.utcnow())
    session.add(user_c)

    session.commit()

    session.query(User).filter(User.user_name == '马云').first()
    session.query(User).order_by(User.age.desc()).all()


def homework_6(from_user_name, to_user_name, transfer_amount):
    if from_user_name == to_user_name:
        return '不能给自己转账'

    from_user_asset = session.query(TransferUserAsset).filter(
        TransferUserAsset.user_id == TransferUser.user_id,
        TransferUser.user_name == from_user_name).first()
    if from_user_asset is None:
        return '转账用户不存在，请检查'

    if from_user_asset.asset < transfer_amount:
        return '可用余额不足，转账失败'

    to_user_assert_info = session.query(TransferUser, TransferUserAsset).filter(
        TransferUser.user_name == to_user_name).outerjoin(TransferUserAsset,
                                                          TransferUserAsset.user_id == TransferUser.user_id).first()
    if to_user_assert_info is None:
        return '目标用户不存在，请检查'

    to_transfer_user, to_user_assert = to_user_assert_info[0], to_user_assert_info[1]
    if to_user_assert is None:
        to_user_assert = TransferUserAsset(user_id=to_transfer_user.user_id,
                                           asset=0)
        session.add(to_user_assert)
        session.commit()

    try:
        from_user_asset.asset = from_user_asset.asset - transfer_amount
        # import time
        # time.sleep(15)
        to_user_assert.asset += transfer_amount
        transfer_history = TransferHistory(from_user_id=from_user_asset.user_id,
                                           to_user_id=to_user_assert.user_id,
                                           transfer_amount=transfer_amount,
                                           transfer_time=datetime.utcnow())
        session.add(transfer_history)
        session.commit()
    except Exception as e:
        # import traceback
        # traceback.print_exc()
        session.rollback()
        return '转账失败'
    return '转账成功'


def init_transfer_data():
    transfer_u1 = TransferUser(user_id=1, user_name='张三')
    transfer_u2 = TransferUser(user_id=2, user_name='李四')
    session.add(transfer_u1)
    session.add(transfer_u2)

    tua = TransferUserAsset(user_id=1, asset=98)
    session.add(tua)

    session.commit()


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    # homework_2()
    # init_transfer_data()
    print(homework_6('李四', '张三', 100))
