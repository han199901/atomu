#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk
from gettext import gettext as _

import sys

from .api import *
from .window import Window
from .asynchelper import async_function
from .misc import dark_mode_switch
from .config import *
from .dialog_create_meeting import CreateMeetingDialog

class MainWindow(Window):
    def __init__(self, app):
        super().__init__(app, "main")

        self.builder_add_file("main_menu")

        self.window.set_application(app)

        menu = self.get("app-menu")
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

    def on_create_meeting_clicked(self, button):
        CreateMeetingDialog(self.app, self.window)

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
                self.info(_("Network error, please check your network connection."))

        api_async("/user/logout", {
            "code": config_get("user_auth_code", None),
        }, on_done)


    def on_dark_switch_button_clicked(self, button):
        dark_mode_switch(True)
