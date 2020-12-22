#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Soup', '2.4')
from gi.repository import Gtk, Gio, GLib, Gdk
import locale
import gettext

import ctypes
import os

def init():
    data_dir = os.path.dirname(__file__)

    if os.name == "nt":
        libintl = ctypes.cdll.LoadLibrary("libintl-8.dll")
        libintl.bindtextdomain.restype = ctypes.c_char_p
        libintl.bind_textdomain_codeset.restype = ctypes.c_char_p
        libintl.textdomain.restype = ctypes.c_char_p
        print(libintl.bindtextdomain("atomudesktop".encode(), f"{data_dir}/mo".encode()))
        print(libintl.bind_textdomain_codeset("atomudesktop".encode(), "UTF-8".encode()))
        print(libintl.textdomain("atomudesktop".encode()))

        vlc_path = os.path.join(os.path.dirname(__file__), "vlc")
        os.environ['PYTHON_VLC_MODULE_PATH'] = vlc_path
        os.environ['PYTHON_VLC_LIB_PATH'] = os.path.join(vlc_path, "libvlc.dll")
        os.add_dll_directory(vlc_path)

        if os.getenv('LANG') is None:
            lang, enc = locale.getdefaultlocale()
            os.environ['LANG'] = lang
    else:
        locale.bindtextdomain("atomudesktop", f"{data_dir}/mo")
        locale.textdomain("atomudesktop")

    gettext.bindtextdomain("atomudesktop", f"{data_dir}/mo")
    gettext.textdomain("atomudesktop")

    res = Gio.Resource.load(data_dir + "/client.gresource")
    Gio.Resource._register(res)

    from .application import Application
    Application(data_dir).run()
