import json
import time
from urllib.request import urlopen

from loguru import logger

import app_properties
from dbutils import redis_client


def add_unit(value):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1
    return f"{value:.2f} {units[unit_index]}"


def process_stats(stats):
    rows = []
    for type_key, type_value in stats.items():
        for tag_key, tag_value in type_value.items():
            rows.append({'type': type_key, 'tag': tag_key, 'downlink': add_unit(tag_value['downlink']),
                         'uplink': add_unit(tag_value['uplink'])})
    return rows


def fetch_metrics(server_id):
    pipe = redis_client.pipeline()
    try:
        logger.debug(f'[{server_id}] fetch stats')
        server = list(app_properties.servers.items())[server_id]
        j_data = json.loads(
            urlopen(f'{"http://" if server[1].get("insecure") is True else "https://"}{server[0]}/debug/vars').read())
        j_data['stats'] = process_stats(j_data.pop('stats'))
        pipe.multi()
        pipe.set(f'{server_id}:cmdline', json.dumps(j_data['cmdline']))
        pipe.set(f'{server_id}:memstats', json.dumps(j_data['memstats']))
        pipe.set(f'{server_id}:observatory', json.dumps(j_data['observatory']))
        pipe.set(f'{server_id}:stats', json.dumps(j_data['stats']))
        pipe.set(f'{server_id}:time', time.time())
        pipe.execute()
        return j_data
    except Exception as e:
        pipe.reset()
        logger.error(e)
        # traceback.print_exc()
    finally:
        pipe.close()
    return None


def get_metric(server_id: int, key: str):
    try:
        update_time = redis_client.get(f'{server_id}:time')
        if update_time:
            if time.time() - float(update_time.decode('utf-8')) < app_properties.interval:
                logger.debug(f'[{server_id}] valid cache')
                data = redis_client.get(f'{server_id}:{key}')
                if data:
                    logger.debug(f'[{server_id}] shot cache')
                    return json.loads(data)
    except Exception as e:
        # traceback.print_exc()
        logger.error(e)
        # dfs.append(failed_data)
    return fetch_metrics(server_id).get(key)
