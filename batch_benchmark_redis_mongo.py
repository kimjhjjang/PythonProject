import json

from src import util

from src.database import Mongo, Redis

from src.client.data_mocker import *

mongo_client = Mongo()
mongo_client.set_database('cm')

redis_client = Redis()

today = util.get_current_ymd('-')
tomorrow = util.get_elapsed_ymd(1, '-')

for dt in gen_ymdh(today, tomorrow):
    collection_name = 'CM_MSG_INFO_{}'.format(dt)
    mongo_client.create_collection(collection_name)

# {total_count}개의 데이터를 입력하는 데 걸리는 시간을 측정
# mock 데이터 생성 시간을 제외하고 순수하게 mongo db에 insert 되는 시간을 측정

total_count = 100000
batch_count = 100
list_key = 'CM_Q_MONGO_DB_TEST'

timer = Timer()

start_time = time.perf_counter()

for index, redis_data in enumerate(redis_client.list_pop_left_all_batch(list_key, 100)):

    collection_name = get_collection_name(redis_data[0])
    if collection_name is None:
        continue

    print('{} / {} DATA PROCESSING ({})'.format((index + 1) * batch_count, total_count, collection_name))

    work_data_list = [data['workData'] for data in redis_data if 'workData' in data]

    insert_count = mongo_client.insert(collection_name, work_data_list)
    timer.measure(insert_count, start_time, time.perf_counter())
    start_time = time.perf_counter()

print(timer)

exit()

for index, data in enumerate(redis_client.list_pop_left_all(list_key)):

    redis_data = json.loads(data)
    collection_name = get_collection_name(redis_data)
    if collection_name is None:
        continue

    print('{} / {} DATA PROCESSING ({})'.format(index + 1, total_count, collection_name))

    insert_count = mongo_client.insert(collection_name, redis_data['workData'])
    timer.measure(insert_count, start_time, time.perf_counter())
    start_time = time.perf_counter()


print(timer)
