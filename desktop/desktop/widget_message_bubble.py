#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk

@Gtk.Template(resource_path="/com/atomu/client/desktop/ui/widget_message_bubble.ui")
class MessageBubbleRow(Gtk.Box):
    __gtype_name__ = 'MessageBubbleRow'

    text = Gtk.Template.Child()
    avatar = Gtk.Template.Child()

    def __init__(self, uid, **kwargs):
        super().__init__(**kwargs)
        self.uid = uid

    def reverse(self):
        self.child_set_property(self.text, "pack-type", Gtk.PackType.END)
        self.avatar.destroy()
