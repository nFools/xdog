import os

import redis

import app_properties

REDIS_HOST = os.getenv('REDIS_HOST', app_properties.redis.host)
REDIS_PROT = os.getenv('REDIS_PROT', app_properties.redis.port)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PROT)
