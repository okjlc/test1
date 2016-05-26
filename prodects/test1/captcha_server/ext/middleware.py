# -*- coding: utf-8 -*-
from datetime import datetime
from functools import wraps
from flask import request, jsonify, current_app
from redis_shard.shard import RedisShardAPI


def check_request(times=10):
    """
    if you per/second to much request, server will be refused.
    and 10s recovery.

    eg.
    @jsonrpc.method('Captcha.check')
    @check_request()
    def check(uid, key):
       ...
    """
    def check_request_cache(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            servers = current_app.config.get("REDIS_SHARD_URL")
            client = RedisShardAPI(servers, hash_method='md5')
            now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            ip = request.remote_addr
            key = "%s{%s}" % (ip, now)
            client.incr(key)
            if client.get(key):
                num = int(client.get(key))
            else:
                num = 0
            client.expire(key, 10)
            if num > times:
                return jsonify(dict(
                    code=40003,
                    msg='warning: Refused to too many requests !'))
            return f(*args, **kwargs)
        return decorator
    return check_request_cache
