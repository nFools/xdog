import yaml
from loguru import logger


class Xdog2:
    interval = 60
    servers = {}

    class Redis:
        host = 'localhost'
        port = 6379

        def update(self, redis_property: dict):
            self.host = redis_property['host'] if redis_property.get('host') else self.host
            self.port = redis_property['port'] if redis_property.get('port') else self.port


interval = Xdog2.interval
servers = Xdog2.servers
redis = Xdog2.Redis()


def load():
    with open('app.yaml', 'r', encoding='utf-8') as yf:
        yml = yaml.load(yf, Loader=yaml.FullLoader)
        xdog2 = yml.get('xdog2')
        servers.update(xdog2['servers'])
        redis.update(xdog2['redis'])
    logger.info(f'load config [{xdog2}]')


def reload():
    load()


load()
