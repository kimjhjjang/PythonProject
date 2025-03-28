from src import util

from src.client.data_mocker import *

from src.util import *
from src.database import Mongo
from src.client import DataMocker

mongo_client = Mongo()
mongo_client.set_database('cm')

today = util.get_current_ymd('-')
tomorrow = util.get_elapsed_ymd(1, '-')

for dt in gen_ymdh(today, tomorrow):
    collection_name = 'CM_MSG_INFO_{}'.format(dt)
    mongo_client.create_collection(collection_name)

# {total_count}개의 데이터를 입력하는 데 걸리는 시간을 측정
# mock 데이터 생성 시간을 제외하고 순수하게 mongo db에 insert 되는 시간을 측정

total_count = 100000
batch_count = 100

timer = Timer()

for index, mongo_data in enumerate(DataMocker.gen_mongo_q_insert_data(total_count)):

    collection_name = get_collection_name(mongo_data)
    if collection_name is None:
        continue

    print('{} / {} DATA PROCESSING ({})'.format(index+1, total_count, collection_name))

    start_time = time.perf_counter()
    insert_count = mongo_client.insert(collection_name, mongo_data['workData'])
    timer.measure(insert_count, start_time, time.perf_counter())

result_insert_one = str(timer)

timer = Timer()

for index, mongo_data in enumerate(DataMocker.gen_mongo_q_insert_data_bulk(total_count, batch_count)):

    collection_name = get_collection_name(mongo_data[0])
    if collection_name is None:
        continue

    print('{} / {} DATA PROCESSING ({})'.format((index+1)*batch_count, total_count, collection_name))

    work_data_list = [data['workData'] for data in mongo_data if 'workData' in data]

    start_time = time.perf_counter()
    insert_count = mongo_client.insert(collection_name, work_data_list)
    timer.measure(insert_count, start_time, time.perf_counter())

result_insert_many = str(timer)

print(result_insert_one)
print(result_insert_many)
