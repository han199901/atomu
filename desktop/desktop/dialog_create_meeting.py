#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk
from gettext import gettext as _

import sys
from datetime import datetime

from .api import *
from .window import Window
from .asynchelper import async_function
from .misc import dark_mode_switch
from .config import *


class CreateMeetingDialog(Window):
    def __init__(self, app, parent):
        super().__init__(app, "create_meeting")
        self.window.set_transient_for(parent)

        dt = datetime.now()

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
