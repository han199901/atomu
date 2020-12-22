#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
from gi.repository import Gtk, Gio, GLib, Gdk, GObject

import sys
import ctypes

import vlc

class VLCWidget:

    def get_window_pointer(self, window):
        ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
        return ctypes.pythonapi.PyCapsule_GetPointer(window.__gpointer__, None)

    def __init__(self, draw_area):
        self.draw_area = draw_area

        self.draw_area.realize()
        self.vlcInstance = vlc.Instance(["--no-xlib"])
        self.player = self.vlcInstance.media_player_new()

        self.draw_area.connect("draw", self.da_draw_event)

        if sys.platform == 'win32':
            gdkdll = ctypes.CDLL('libgdk-3-0.dll')
            gdkdll.gdk_win32_window_get_handle.restype = ctypes.c_void_p
            gdkdll.gdk_win32_window_get_handle.argtypes = [ctypes.c_void_p]
            handle = gdkdll.gdk_win32_window_get_handle(self.get_window_pointer(draw_area.get_window()))
            self.player.set_hwnd(handle)
        elif sys.platform == 'darwin':
            gdkdll = ctypes.CDLL('libgdk-3.0.dylib')
            get_nsview = gdkdll.gdk_quaerz_window_get_nsview
            get_nsview.restype, get_nsview.argtypes = [ctypes.c_void_p],  ctypes.c_void_p
            self.player.set_nsobject(get_nsview(self.get_window_pointer(draw_area.get_window())))
        else:
            from gi.repository import GdkX11
            self.player.set_xwindow(self.draw_area.get_window().get_xid())

    def da_draw_event(self, widget, cairo_ctx):
        cairo_ctx.set_source_rgb(0, 0, 0)
        cairo_ctx.paint()

    def set_mrl(self, mrl):
        self.player.stop()
        self.player.set_mrl(mrl)
        self.player.play()
        
    def stop(self):
        self.player.stop()
