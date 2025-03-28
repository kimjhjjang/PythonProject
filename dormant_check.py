import logging as log
import sys
import os

sys.path.append(r"C:\Users\admin\PycharmProjects\PythonProject\.venv\Lib\site-packages")

# path setting
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.client.schema_info_provider import SchemaInfoProvider
from src.database.redis import Redis

client = Redis()

# Configure logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create an instance of SchemaInfoProvider
provider = SchemaInfoProvider()

# Call the get_dormant_data function
dormant_data = provider.get_dormant_data()

# Log the results
log.info(f'Daily Data: {dormant_data}')

for item in dormant_data:
    try:
        # Combine KKO_CH_ID and TMPLT_CODE
        kko_ch_id = item.get('KKO_CH_ID')
        tmplt_code = item.get('TMPLT_CODE')
        hash_key = f"{kko_ch_id}@{tmplt_code}"

        # Log the generated HASH KEY
        log.info(f"Generated Redis Hash Key: {hash_key}")

        # Fetch data from Redis using the RedisClient's method
        redis_data = client.hget("CM_H_KKO_TMPLT_INFO_EXT",hash_key)

        # Log the retrieved Redis data
        if redis_data:
            log.info(f"Data found in Redis for {hash_key}: {redis_data}")

        else:
            log.warning(f"No data found in Redis for {hash_key}.")
    except Exception as e:
        log.error(f"Error while processing item {item}: {e}")

