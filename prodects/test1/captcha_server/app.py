# -*- coding: utf-8 -*-
from flask import Flask
from captcha_server.ext.cache import cache
from captcha_server.rpc.captcha import captcha_rpc, jsonrpc


def create_app():
    app = Flask("captcha_rpc_server")
    app.config.from_envvar('APP_CONFIG_FILE')

    # jsonrpc
    jsonrpc.init_app(app)
    jsonrpc.register_blueprint(captcha_rpc)

    # redis cache
    cache.init_app(app)

    return app
