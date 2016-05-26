# -*- coding: utf-8 -*-
import requests
import pytest


url = "http://localhost:5000/v1/rpc/captcha"


def test_create():
    p_params = {"jsonrpc": "2.0", "method": "Captcha.create",
                "params": {}, "id": "1"}
    headers = {'Content-Type': "application/json"}
    r = requests.post(url, json=p_params, headers=headers)

    assert r.status_code == requests.codes.ok
    return r.json()


def test_check():
    p_params = {"jsonrpc": "2.0",
                "method": "Captcha.check",
                "params": {"uid": "26752493-a98b-4d7f-88d7-248b22a28fdb",
                           "key": '1234'},
                "id": "1"}
    headers = {'Content-Type': "application/json"}
    r = requests.post(url, json=p_params, headers=headers)

    assert r.status_code == requests.codes.ok
    return r.json()

if __name__ == "__main__":
    pytest.main()
