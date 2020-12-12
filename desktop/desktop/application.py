#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib, Gdk

import os

from .api import api
from .window_login import LoginWindow
from .misc import dark_mode_switch, dark_mode_init
from .config import *

class Application(Gtk.Application):
    def __init__(self, data_dir):
        self.data_dir = data_dir

        import random
        Gtk.Application.__init__(self, application_id="com.atomu.client.desktop._" + str(random.randint(0, 10000)))
        self.res = "/com/atomu/client/desktop"

        config_load()

        Gtk.Settings.get_default().set_property("gtk-decoration-layout", "close,minimize,maximize:menu")

        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_resource(self.res + "/main.css")
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        dark_mode_init(self.res)
        dark_mode_switch(False)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        LoginWindow(self)

    def do_activate(self):
        window = self.get_active_window()
        if window:
            window.present()

    def run(self):
        Gtk.Application.run(self)
        config_save()
