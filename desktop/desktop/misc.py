#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .config import *

from gi.repository import Gtk

def dark_mode_switch(switch):
    dark = config_get("dark_mode", False)
    if switch:
        dark = not dark
        config_set("dark_mode", dark)
    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", dark)

