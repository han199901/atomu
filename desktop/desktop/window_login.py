#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk
from locale import gettext as _

from .api import *
from .window import Window
from .asynchelper import async_function
from .misc import dark_mode_switch
from .config import *
from .window_main import MainWindow

class LoginWindow(Window):
    def __init__(self, app):
        super().__init__(app, "login")
        self.window.set_application(app)
        self.window.show_all()

        if config_get("user_auth_uid", None):
            set_code(config_get("user_auth_uid", None), config_get("user_auth_code", None))
            self.login()

    def login(self):
        button = self.get("login_button")

        def on_reload_token_done(r, e):
            button.set_sensitive(True)
            try:
                result = finish(r, e)
                MainWindow(self.app)
                self.window.close()
            except CSystemError as e:
                if e.code == 3:
                    config_set("user_auth_uid", None)
            except:
                pass #FIXME

        button.set_sensitive(False)
        reload_token_async(on_reload_token_done)

    def on_help_button_clicked(self, button):
        pass

    def on_dark_switch_button_clicked(self, button):
        dark_mode_switch(True)

    def on_login_clicked(self, button):
        username = self.get("username").get_text()
        password = self.get("password").get_text()

        def on_done(r, e):
            button.set_sensitive(True)
            try:
                result = finish(r, e)
                set_code(result["uid"], result["auth"])

                config_set("user_auth_uid", result["uid"])
                config_set("user_auth_code", result["auth"])

                self.login()
            except CSystemError as e:
                self.err(_("Login failed, please check your username and password."))
            except CNetworkError:
                self.info(_("Network error, please check your network connection."))

        button.set_sensitive(False)
        api_async("/login/login", {
            "name": username,
            "password": password
        }, on_done)
