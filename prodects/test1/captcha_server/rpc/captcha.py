# -*- coding: utf-8 -*-
import uuid
import cPickle
from flask_jsonrpc import JSONRPC
from flask import Blueprint
from captcha_server.ext.captcha import create_captcha
from captcha_server.utils.words import lower_noblank
from captcha_server.ext.cache import cache
from flask import jsonify
from captcha_server.ext.middleware import check_request


captcha_rpc = Blueprint('catpcha_rpc', __name__)
jsonrpc = JSONRPC(None, '/v1/rpc/captcha', enable_web_browsable_api=True)


@jsonrpc.method('Captcha.example')
def example():
    return u'Welcome to Acttao Captcha Server!'


@jsonrpc.method('Captcha.create')
#@check_request()
def create(chars=None):
    img, body, chars = create_captcha(chars)
    uid = unicode(uuid.uuid4())
    cache.set(uid, cPickle.dumps({chars: body}))
    return jsonify(dict(code=10000, uid=uid, img=body))


@jsonrpc.method('Captcha.check')
@check_request()
def check(uid, key):
    _cached = cache.get(uid)
    if _cached:
        img_dict = cPickle.loads(_cached)
        img_key = img_dict.keys()[0]
        if lower_noblank(key) == lower_noblank(img_key):
            return jsonify(dict(code=10000, msg=u'校验成功!'))
        else:
            return jsonify(dict(code=10001, msg=u'校验失败!'))
    return jsonify(dict(code=40001, msg=u'验证码不存在，请重试！'))
