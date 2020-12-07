#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk
from gettext import gettext as _

import sys
from datetime import datetime, timedelta, timezone

from .api import *
from .window import Window
from .asynchelper import async_function
from .misc import dark_mode_switch, tz
from .config import *

class CreateMeetingDialog(Window):
    def __init__(self, parent):
        super().__init__(parent.app, "create_meeting")
        self.parent = parent
        self.window.set_transient_for(parent.window)

        dt = datetime.now(tz)

        calendar = self.get("calendar")
        calendar.set_property("day", dt.day)
        calendar.set_property("month", dt.month - 1)
        calendar.set_property("year", dt.year)

        hour = self.get("hour")
        for i in range(0, 23):
            hour.append_text(str(i))
        hour.set_active(dt.hour)

        mintute = self.get("mintute")
        for i in range(0, 59):
            mintute.append_text(str(i))
        mintute.set_active(dt.minute)

        self.window.show_all()

    def on_ok_clicked(self, button):
        button.set_sensitive(False)

        name = self.get("name").get_text()
        length = int(self.get("length").get_active_text())

        calendar = self.get("calendar")
        d = calendar.get_property("day")
        m = calendar.get_property("month") + 1
        y = calendar.get_property("year")

        hour = self.get("hour")
        hh = int(hour.get_active_text())

        mintute = self.get("mintute")
        mm = int(mintute.get_active_text())

        btime = datetime(y, m, d, hh, mm, 0, 0, tz)
        etime = btime + timedelta(minutes=length)

        def on_done(r, e):
            button.set_sensitive(True)

            try:
                result = finish(r, e)
                self.parent.list_all_my_meetings()
                self.window.close()
            except CError as e:
                self.defexphandler(e)

        api_async("/meeting/create", {
            "name": name,
            "start": btime.isoformat(),
            "end": etime.isoformat()
        }, on_done)
