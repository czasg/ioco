import re
import logging

from redis import StrictRedis
from random import choice

logger = logging.getLogger(__name__)


def check_proxy_ok(proxy):
    return re.match('\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:\d+$', proxy)


class Redis:
    def __init__(self, db, setting):
        self.db =  db
        self.pipe = db.pipeline()
        self.setting = setting
        self.score = setting.redis_score
        self.key = setting.redis_key
        self.min_score = setting.redis_min_score
        self.use_pipe = setting.redis_use_pipe

    @classmethod
    def from_setting(cls, setting):
        return cls(StrictRedis(**setting.get_redis_config()), setting)

    def add(self, proxy):
        if check_proxy_ok(proxy) and not self.db.zscore(self.key, proxy):
            logger.info('添加代理: %s' % proxy)
            if self.use_pipe:
                self.pipe.zadd(self.key, **{proxy: self.score})
            else:
                self.db.zadd(self.key, **{proxy: self.score})

    def random(self):
        try:
            return choice(self.db.zrangebyscore(self.key, 4, 100))
        except:
            logger.warning('代理池无可用代理')

    def decrease(self, proxy):
        score = self.db.zscore(self.key, proxy)
        if score and score > self.min_score:
            return self.db.zincrby(self.key, proxy, -1)
        else:
            return self.db.zrem(self.key, proxy)

    def exists(self, proxy): return self.db.zscore(self.key, proxy) is not None

    def count(self): return self.db.zcard(self.key)

    def all(self): return self.db.zrangebyscore(self.key, self.min_score, self.score)

    def batch(self, start, stop): return self.db.zrevrange(self.key, start, stop-1)

    def pipe_execute(self): return self.pipe.execute()


if __name__ == '__main__':
    from proxy_pool.setting import Setting as config
    redis = Redis.from_setting(config)
    # print(redis.random())
    # print(redis.count())
    # print(redis.all())

