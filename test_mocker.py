import json

from src.client import DataMocker

mongo_data = DataMocker.build_mongo_q_random_data()
print(json.dumps(mongo_data, indent=2))
