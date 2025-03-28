from src.util import *

from src.database import Mongo

client = Mongo()
client.set_database('cm')

for dt in gen_ymdh('2024-11-17', '2024-11-18'):
    collection_name = 'CM_MSG_INFO_{}'.format(dt)
    print(collection_name)
    client.create_collection(collection_name)
