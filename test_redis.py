import json
import logging

from src.database import Redis, Digger
from src.util.digger import decode_bytes
from src.util import setup_logging

setup_logging('test_redis')

client = Redis()

list_key = 'CM_Q_MONGO_DB_TEST2'

#database.list_push_right(list_key, 'new_data')  # 오른쪽에 데이터 추가
#database.list_push_left(list_key, 'another_item')  # 왼쪽에 데이터 추가

#database.list_pop_left(list_key)

# 리스트의 모든 값 가져오기
#print(database.get_list_all())

common_info = client.get_string('CM_S_COMMON')
digger = Digger(json.loads(common_info))

# 아쉬운 부분은 filter 후에 dig 시 filter
group_id = digger.dig('commonLst.[1]').filter('fieldId', 'mPushConnInfo').nth().dig('fieldValue').get('groupId')
logging.info(group_id)

conn_info = client.hget_all('CM_H_CH_CONNECTION_INFO')
digger = Digger(decode_bytes(conn_info))
#print(digger)

digger = digger.filter('useYn', 'Y').filter('delYn', 'N').filter('distributionChType', 'KKO').filter('chSupplyCode', 'LGCNS').nth()

digger.print()

svc_pwd = digger.dig('connInfo').print().get('svcPwd')

logging.info(svc_pwd)