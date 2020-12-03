#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk

from .api import *
from . import api as API

_uid = None
_code = None
_token = None


def set_code(uid, code):
    global _uid, _code

    _uid = uid
    _code = code

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
