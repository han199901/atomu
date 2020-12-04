#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk

from .api import *
from .window import Window
from .asynchelper import async_function
from .misc import dark_mode_switch

class MainWindow(Window):
    def __init__(self, app):
        super().__init__(app, "main")
        self.window.set_application(app)
        self.window.show_all()

    def on_dark_switch_button_clicked(self, button):
        dark_mode_switch(True)
