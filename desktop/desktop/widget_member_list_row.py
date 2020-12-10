#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk

@Gtk.Template(resource_path="/com/atomu/client/desktop/ui/widget_member_list_row.ui")
class MemberListRow(Gtk.Box):
    __gtype_name__ = 'MemberListRow'

    title = Gtk.Template.Child()
    description = Gtk.Template.Child()

    def __init__(self, id, name, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.title.set_text(name)
