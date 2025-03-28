import json

import redis

from src.util import read_config_yaml


class Redis(object):

    client = None

    def __init__(self):

        config = read_config_yaml()
        host = config.get('redis.host')
        port = config.get('redis.port')
        db = config.get('redis.db')

        if host is None or port is None or db is None:
            raise ValueError('redis host, port, db is not configured')

        if self.client is None:
            self.client = redis.Redis(host=host, port=port, db=db)

    def list_push_left(self, name, data):

        res = self.client.lpush(name, data)


    def list_push_right(self, name, data):

        res = self.client.rpush(name, data)


    def get_list_all(self, name):

        return self.client.lrange(name, 0, -1)


    def delete_list_all(self, name):

        res = self.client.delete(name)
        if res:
            print('{} DATA DELETED'.format(res))
        else:
            print('"{}" LIST HAS NO DATA')


    def list_pop_left(self, name):
        return self.client.lpop(name)


    def list_pop_left_all(self, name):

        while True:
            res = self.client.lpop(name)
            if res is None:
                break
            yield json.loads(res)


    def list_pop_left_all_batch(self, name, count):

        buffer = []

        while True:
            res = self.client.lpop(name)
            if res is None:
                break
            buffer.append(json.loads(res))

            if len(buffer) == count:
                yield buffer  # 리스트 반환
                buffer = []  # 리스트 초기화

        # 남아 있는 데이터 반환
        if buffer:
            yield buffer


    def hget_all(self, name):
        return self.client.hgetall(name)

    def hget(self, name, key):
        return self.client.hget(name, key)

    def get_string(self, name):
        return self.client.get(name)
