#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
from gettext import gettext as _

#from dateutil.relativedelta import relativedelta
import tzlocal
from dateutil.tz import gettz
from datetime import datetime

from .config import *
from .defaults import *

tz = gettz(str(tzlocal.get_localzone()))

provider = None

def dark_mode_init(res):
    global provider

    provider = Gtk.CssProvider()
    provider.load_from_resource(res + "/main-dark.css")

def dark_mode_switch(switch):
    dark = config_get("dark_mode", False)
    if switch:
        dark = not dark
        config_set("dark_mode", dark)
    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", dark)

    screen = Gdk.Screen.get_default()
    if dark:
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1)
    else:
        Gtk.StyleContext.remove_provider_for_screen(screen, provider)

def format_date(date, cur):
    tmp = date - cur
    if date.year == cur.year:
        if date.month == cur.month:
            if date.day == cur.day:
                return date.strftime("%H:%M")
            return date.strftime(_("%d %H:%M"))
        return date.strftime(_("%d %b %H:%M"))
    return date.strftime(_("%d %b %Y %H:%M"))

def format_date_ml(begin, end):
    cur = datetime.now(tz)
    begin = begin.astimezone(tz=tz)
    end = end.astimezone(tz=tz)
    f = format_date(begin, cur)
    t = format_date(end, cur)

    return _("From %(from)s, to %(to)s") % ({
        "from": f,
        "to": t
    })

def sharelink(id, code):
    return f"{URL_PREFIX}/join/{id}:{code}"
