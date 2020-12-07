#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gettext import gettext as _

#from dateutil.relativedelta import relativedelta
import tzlocal
from dateutil.tz import gettz
from datetime import datetime

from .config import *

tz = gettz(str(tzlocal.get_localzone()))

def dark_mode_switch(switch):
    dark = config_get("dark_mode", False)
    if switch:
        dark = not dark
        config_set("dark_mode", dark)
    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", dark)

def format_date(date, cur):
    tmp = date - cur
    if tmp.days == 0:
        return date.strftime("%H:%M")
    #elif tmp.year == 0:
    #    return date.strftime(_("%d %b %H:%M"))
    else:
        return date.strftime(_("%d %b %Y %H:%M"))

def format_date_ml(begin, end):
    cur = datetime.now(tz)
    begin = begin.astimezone(tz=tz)
    end = end.astimezone(tz=tz)
    print(cur)
    print(begin)
    print(end)
    f = format_date(begin, cur)
    t = format_date(end, cur)

    return _("From %s, to %s") % (f, t)

def sharelink(id, code):
    return f"http://help.hanblog.fun/join/{id}:{code}"
