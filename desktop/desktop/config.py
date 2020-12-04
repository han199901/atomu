#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pathlib

_fn = None
_need_save = False

config_dir = None

config = dict()

__all__ = [
    "config_get",
    "config_set",
    "config_save",
    "config_load",
    "get_config_dir"
]

def config_load():
    global _fn
    global config_dir

    if os.name == "nt":
        if "APPDATA" in os.environ:
            config_dir = os.path.join(os.environ["APPDATA"], "atomu")
        else:
            config_dir = os.path.join(os.path.expanduser("~"), ".atomu")
    else:
        if 'XDG_CONFIG_HOME' in os.environ:
            config_dir = os.path.join(os.environ['XDG_CONFIG_HOME'], "atomu")
        else:
            config_dir = os.path.join(os.environ['HOME'], '.config', "atomu")

    print(f"conf dir: {config_dir}")
    if not os.path.exists(config_dir):
        pathlib.Path(config_dir).mkdir(parents=True, exist_ok=True)

    _fn = os.path.join(config_dir, "desktop.conf")
    if os.path.exists(_fn):
        with open(_fn) as f:
            config.update(json.load(f))

def config_save():
    global _fn
    global _need_save

    if _need_save and _fn is not None:
        print(f"save config: {_fn}")
        with open(_fn, "w") as f:
            json.dump(config, f)

def config_get(name, defvalue):
    if name not in config:
        return defvalue
    return config[name]

def config_set(name, value):
    global _need_save
    _need_save = True
    config[name] = value

def get_config_dir():
    return config_dir

