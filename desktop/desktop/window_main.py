#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk

import sys
import traceback

from .api import *
from .window import Window
from .asynchelper import async_function
from .misc import dark_mode_switch
from .config import *

MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
        <item>
            <attribute name="label">About</attribute>
            <attribute name="action">app.about</attribute>
        </item>
        <item>
            <attribute name="label">Logout</attribute>
            <attribute name="action">app.logout</attribute>
        </item>
    </section>
  </menu>
</interface>
"""

class MainWindow(Window):
    def __init__(self, app):
        super().__init__(app, "main")

        self.window.set_application(app)

        self.builder.add_from_string(MENU_XML)

        menu = self.builder.get_object("app-menu")
        button = self.get("menu_button")
        popover = Gtk.Popover.new_from_model(button, menu)
        button.set_popover(popover)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        app.add_action(action)

        action = Gio.SimpleAction.new("logout", None)
        action.connect("activate", self.on_logout)
        app.add_action(action)

        self.window.show_all()

    def on_about(self, action, param):
        pass

    def on_logout(self, action, param):
        def on_done(r, e):
            try:
                result = finish(r, e)
                config_set("user_auth_uid", None)
                config_set("user_auth_code", None)
                self.window.close()
            except CSystemError as e:
                config_set("user_auth_uid", None)
                config_set("user_auth_code", None)
                self.window.close()
            except CNetworkError:
                traceback.print_exc()
                self.info("Network error, please check your network connection.")

        api_async("/user/logout", {
            "code": config_get("user_auth_code", None),
        }, on_done)


    def on_dark_switch_button_clicked(self, button):
        dark_mode_switch(True)
