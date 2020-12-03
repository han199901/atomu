#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import traceback
from gi.repository import GLib

__all__ = ['async_function']

def _async_call(f, args, kwargs, on_done):
    def run(data):
        f, args, kwargs, on_done = data
        error = None
        result = None
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            #e.traceback = traceback.format_exc()
            #error = 'Unhandled exception in asyn call:\n{}'.format(e.traceback)
            error = e
        if on_done:
            GLib.idle_add(lambda: on_done(result, error))

    data = f, args, kwargs, on_done
    thread = threading.Thread(target=run, args=(data,))
    thread.daemon = True
    thread.start()

def async_function(on_done):
    def wrapper(f):
        def run(*args, **kwargs):
            _async_call(f, args, kwargs, on_done)
        return run
    return wrapper
