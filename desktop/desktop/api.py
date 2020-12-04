#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk

import requests

from .asynchelper import async_function

__all__ = [
    "CNetworkError",
    "CSystemError",
    "finish",
    "api_async",
    "api",
    "_token",
    "set_code",
    "reload_token",
    "reload_token_async"
]

prefix = "http://help.hanblog.fun/api"
_uid = None
_code = None
_token = None

class CNetworkError(Exception):
    def __init__(self):
        super().__init__(self)

class CSystemError(Exception):
    def __init__(self, code):
        super().__init__(self)
        self.code = code

def finish(r, e):
    try:
        assert r is not None
        assert "code" in r
        assert "result" in r
    except:
        raise CNetworkError()

    if r["code"] != 0:
        raise CSystemError(r["code"])

    return r["result"]

def _api(endpoint, body):
    headers = {
        "User-agent": "AtomuClientDesktop/0.1.0 CPython/unknown requests/unknown",
        "Accept": "application/json"
    }
    if _token:
        headers["Authorization"] = f"bearer {_token}"
    print(f"> {endpoint}: {body}")
    resp = requests.post(prefix + endpoint, json=body, headers=headers).json()
    print(resp)
    return resp

def api(endpoint, body):
    resp = _api(endpoint, body)
    if "code" in resp and resp["code"] == 5:
        _token = reload_token() #FIXME
        resp = _api(endpoint, body)

    return resp

def api_async(endpoint, body, callback):
    def on_done(resp, error):
        callback(resp, error)

    @async_function(on_done=on_done)
    def call_api(endpoint, body):
        return api(endpoint, body)

    call_api(endpoint, body)

def set_code(uid, code):
    global _uid, _code

    _uid = uid
    _code = code

def reload_token():
    resp = api("/login/token", {
        "uid": _uid,
        "auth": _code
    })
    assert "code" in resp
    assert resp["code"] == 0
    return resp["result"]["token"]

def reload_token_async(callback):
    global _token

    def on_done(r, e):
        try:
            result = finish(r, e)
            _token = result["token"]
            API._token = _token
        except:
            pass
        callback(r, e)

    api_async("/login/token", {
        "uid": _uid,
        "auth": _code
    }, on_done)
