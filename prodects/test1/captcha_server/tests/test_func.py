# -*- coding: utf-8 -*-
import requests
import pytest


url = "http://localhost:5000/v1/rpc/captcha"


def test_create():
    p_params = {"jsonrpc": "2.0", "method": "Captcha.create",
                "params": {'chars': '1234'}, "id": "1"}
    headers = {'Content-Type': "application/json"}
    r = requests.post(url, json=p_params, headers=headers)

    assert r.status_code == requests.codes.ok
    uid = r.json()['uid']
    return r.json(), uid


def test_check():
    data, uid = test_create()
    p_params = {"jsonrpc": "2.0",
                "method": "Captcha.check",
                "params": {"uid": uid,
                           "key": '1234'},
                "id": "1"}
    headers = {'Content-Type': "application/json"}
    r = requests.post(url, json=p_params, headers=headers)

    assert r.status_code == requests.codes.ok
    return r.json()

if __name__ == "__main__":
    pytest.main()
