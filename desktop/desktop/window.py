#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk
from gettext import gettext as _

from .api import *

def _dialog(tfor ,mtype, buttons, text, subtext = None, markup = False):
    dialog = Gtk.MessageDialog(
        transient_for=tfor,
        flags=0,
        message_type=mtype,
        buttons=buttons,
        text=text
    )

    if markup:
        dialog.set_markup(text)

    if subtext is not None:
        dialog.format_secondary_text(subtext)

    value = dialog.run()
    dialog.destroy()
    return value

errmap = {
    5: "FIXME", # never should be 5
    4: _("Login failed, please check your username and password."),
    6: _("Permision denied"),
    10: _("No such meeting"),
    11: _("Meeting datetime overlap"),
    13: _("Meeting is expired"),
    14: _("Meeting is not started"),
}

class Window():
    def __init__(self, app, ui):
        self.app = app

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain("atomudesktop")
        self.builder_add_file(ui)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window")

    def builder_add_file(self, fn):
        self.builder.add_from_resource(f"{self.app.res}/ui/{fn}.ui")

    def get(self, id):
        return self.builder.get_object(id)

    def defexphandler(self, e):
        if isinstance(e, CNetworkError):
            self.info(_("Network error, please check your network connection."))
        elif isinstance(e, CSystemError):
            msg = _("Unknown error")
            if e.code in errmap:
                msg = errmap[e.code]
            self.err(msg)

    def info(self, *args, **kwargs):
        _dialog(self.window, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, *args, **kwargs)
    def warn(self, *args, **kwargs):
        _dialog(self.window, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, *args, **kwargs)
    def err(self, *args, **kwargs):
        _dialog(self.window, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, *args, **kwargs)
    def ask(self, *args, **kwargs):
        return _dialog(self.window, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, *args, **kwargs)
