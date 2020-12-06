#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk

@Gtk.Template(resource_path="/com/atomu/client/desktop/ui/widget_meeting_list_row.ui")
class MeetingListRow(Gtk.Box):
    __gtype_name__ = 'MeetingListRow'

    title = Gtk.Template.Child()
    description = Gtk.Template.Child()
    delete = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
