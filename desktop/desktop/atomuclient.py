#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib, Gdk
import locale
import gettext

import ctypes
import os

def init():
    data_dir = os.path.dirname(__file__)
    gettext.bindtextdomain("atomudesktop", f"{data_dir}/mo")
    gettext.textdomain("atomudesktop")

    if os.name == "nt":
        libintl = ctypes.cdll.LoadLibrary("libintl-8.dll")
        libintl.bindtextdomain.restype = ctypes.c_char_p
        libintl.bind_textdomain_codeset.restype = ctypes.c_char_p
        libintl.textdomain.restype = ctypes.c_char_p
        print(libintl.bindtextdomain("atomudesktop".encode(), f"{data_dir}/mo".encode()))
        print(libintl.bind_textdomain_codeset("atomudesktop".encode(), "UTF-8".encode()))
        print(libintl.textdomain("atomudesktop".encode()))
    else:
        locale.bindtextdomain("atomudesktop", f"{data_dir}/mo")
        locale.textdomain("atomudesktop")

    res = Gio.Resource.load(data_dir + "/client.gresource")
    Gio.Resource._register(res)

    from .application import Application
    Application(data_dir).run()
