#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib, Gdk
import locale

import os

from .api import api
from .window_login import LoginWindow
from .misc import dark_mode_switch
from .config import *

class Application(Gtk.Application):
    def __init__(self):
        self.data_dir = os.path.dirname(__file__)
        locale.bindtextdomain("atomudesktop", f"{self.data_dir}/mo")
        locale.textdomain("atomudesktop")

        Gtk.Application.__init__(self, application_id="com.atomu.client.desktop")
        self.res = "/com/atomu/client/desktop"

        res = Gio.Resource.load(self.data_dir + "/client.gresource")
        Gio.Resource._register(res)

        config_load()

        dark_mode_switch(False)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        w = LoginWindow(self)

    def do_activate(self):
        window = self.get_active_window()
        if window:
            window.present()

    def run(self):
        Gtk.Application.run(self)
        config_save()
