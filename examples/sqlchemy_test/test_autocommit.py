
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column, String, DateTime, Text, create_engine, Integer
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def get_global_session_without_pool(url):
    engine = create_engine(url, poolclass=NullPool)
    session = sessionmaker(bind=engine)
    return session()


class Alert(Base):
    __tablename__ = 'alert'
    id = Column(Integer, primary_key=True)
    update_time = Column(Integer)

    def __init__(self, id, update_time):
        self.id = id
        self.update_time = update_time


class AlertHandler:

    def __init__(self, db_user, db_pass, db_host, db_name):
        self.db_setting = "mysql+pymysql://{user}:{pw}@{host}/{db}?autocommit=true".format(
            user=db_user, pw=db_pass, host=db_host, db=db_name
        )
        self.db_session = get_global_session_without_pool(self.db_setting)

    def _get_update_time_from_db(self, ids):
        return self.db_session.query(
            Alert.id, Alert.update_time
        ).filter(Alert.id.in_(ids)).all()


class AlertHandlerV2:

    def __init__(self, db_user, db_pass, db_host, db_name):
        self.db_setting = "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
            user=db_user, pw=db_pass, host=db_host, db=db_name
        )
        self.db_session = get_global_session_without_pool(self.db_setting)

    def _get_update_time_from_db(self, ids):
        return self.db_session.query(
            Alert.id, Alert.update_time
        ).filter(Alert.id.in_(ids)).all()


def unit_test():
    '''Unit test for this module.'''
    handler = AlertHandler(
        'root', 'Trend#1..',
        '10.206.67.81', 'alert_opt'
    )
    ids = [1, 2, 400]
    result = handler._get_update_time_from_db(ids)
    print result


if __name__ == '__main__':
    unit_test()
