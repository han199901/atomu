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
    "_token"
]

prefix = "http://help.hanblog.fun/api"
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
    return requests.post(prefix + endpoint, json=body, headers=headers).json()

def api(endpoint, body):
    print(f"> {endpoint}: {body}")
    resp = _api(endpoint, body)
    print(resp)

    return resp

def api_async(endpoint, body, callback):
    def on_done(resp, error):
        callback(resp, error)

    @async_function(on_done=on_done)
    def call_api(endpoint, body):
        return api(endpoint, body)

    call_api(endpoint, body)
