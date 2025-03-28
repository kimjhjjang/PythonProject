import logging
import pymysql

from pymysql.cursors import DictCursor
from src.util import read_config_yaml


class Mysql(object):

    client = None
    database = None

    def __init__(self):

        config = read_config_yaml()
        host = config.get('mysql.host')
        port = config.get('mysql.port')
        user = config.get('mysql.user')
        password = config.get('mysql.password')
        db = config.get('mysql.db')
        charset = config.get('mysql.charset')

        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset=charset)


    def queries(self, sql):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                return cursor.fetchall()  # 모든 결과를 가져옴

        except pymysql.err.OperationalError as e:
            logging.fatal(e)

        return None


    def query(self, sql):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                return cursor.fetchone()  # 0, 1개의 결과를 가져옴

        except pymysql.err.OperationalError as e:
            logging.fatal(e)

        return None


    def gets(self, sql):
        res = self.queries(sql)
        if res is None:
            return []
        return res


    def get(self, sql):
        res = self.query(sql)
        if res is None:
            return {}
        return res

