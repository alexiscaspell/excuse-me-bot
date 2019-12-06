import redis
from config.configuration import CurrentConfig


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisLocalPool(metaclass=Singleton):

    def __init__(self, host=CurrentConfig.REDIS_HOST, port=int(CurrentConfig.REDIS_PORT), db=0,password=CurrentConfig.REDIS_PASSWD,redis_url:str=None):
        if redis_url:
            self.redisPool = redis.ConnectionPool.from_url(redis_url)
        else:
            self.redisPool = redis.ConnectionPool(host=host, port=port, db=db,password=password)

    def __getattr__(self, name):
        return self.redisPool.__getattribute__(name)

redis_local_pool = RedisLocalPool(redis_url=CurrentConfig.REDIS_URL).redisPool
