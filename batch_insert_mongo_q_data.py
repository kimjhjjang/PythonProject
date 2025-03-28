import json

from src.database import Redis
from src.client import DataMocker

redis_client = Redis()
list_key = 'CM_Q_MONGO_DB_TEST'

redis_client.delete_list_all(list_key)

# 데이터가 섞여서 내려갈 수 있도록 수정 (insert 후에 랜덤으로 update 데이터도 생성 되도록 수정)
#for index, mongo_data in enumerate(MessageHub.gen_mongo_q_data(50000)):
#    print('{} DATA (FOR INSERT/UPDATE) INSERTED TO REDIS'.format(index + 1))
#    redis_client.list_push_right(list_key, json.dumps(mongo_data))

for index, mongo_data in enumerate(DataMocker.gen_mongo_q_insert_data(10000)):
    print('{} DATA (FOR INSERT) INSERTED TO REDIS'.format(index+1))
    redis_client.list_push_right(list_key, json.dumps(mongo_data))

#for index, mongo_data in enumerate(MessageHub.gen_mongo_q_update_data(50000)):
#    print('{} DATA (FOR UPDATE) INSERTED TO REDIS'.format(index+1))
#    redis_client.list_push_right(list_key, json.dumps(mongo_data))
