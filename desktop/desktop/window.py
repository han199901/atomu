#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk

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

class Window():
    def __init__(self, app, ui):
        self.app = app

        self.builder = Gtk.Builder()
        self.builder.add_from_resource(f"{app.res}/ui/{ui}.ui")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window")

    def get(self, id):
        return self.builder.get_object(id)

    def info(self, *args, **kwargs):
        _dialog(self.window, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, *args, **kwargs)
    def warn(self, *args, **kwargs):
        _dialog(self.window, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, *args, **kwargs)
    def err(self, *args, **kwargs):
        _dialog(self.window, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, *args, **kwargs)
    def ask(self, *args, **kwargs):
        return _dialog(self.window, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, *args, **kwargs)
