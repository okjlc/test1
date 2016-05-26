# -*- coding: utf-8 -*-
from redis_shard.shard import RedisShardAPI


class Cached:
    _cache = ''

    def init_app(self, app):
        servers = app.config.get("REDIS_SHARD_URL")
        client = RedisShardAPI(servers, hash_method='md5')
        self._cache = client
        return client

    def set(self, key, value, expire=300):
        """
        Captcha expire time: 300s
        """
        return self._cache.setex(key, value, expire)

    def get(self, key, expire=300):
        return self._cache.get(key)




    def clear(self):
            self._cache.clear()

cache = Cached()
