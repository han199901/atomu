#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk, GObject
from gettext import gettext as _

import sys
import os
import re
from datetime import datetime, timedelta, timezone

from .api import *
from .window import Window
from .asynchelper import async_function
from .misc import dark_mode_switch, tz
from .config import *

class DevWebcam(GObject.Object):
    def __init__(self, name, mrl, extra_options=None):
        super().__init__()
        self.name = name
        self.mrl = mrl
        self.extra_options = None
        if extra_options:
            self.extra_options = extra_options

class DevAudioRecoder(GObject.Object):
    def __init__(self, name, options=None):
        super().__init__()
        self.name = name
        self.options = None
        if options:
            self.options = options

def list_webcam_linux():
    tmp = [i for i in os.listdir("/dev/") if re.match(r"^video[0-9]+$", i)]
    tmp = list(map(lambda i: DevWebcam(_("V4L2 device: /dev/") + i, "v4l2:///dev/" + i), tmp))
    tmp.insert(0, DevWebcam(_("Desktop Screen"), "screen://"))
    tmp.insert(0, DevWebcam(_("Default Device"), "v4l2://"))
    return tmp

def list_audiorecoder_linux():
    def chname(i):
        i = re.sub(r'^pcmC', 'hw:', i)
        i = re.sub(r'c$', '', i)
        i = re.sub(r'D', ',', i)
        return DevAudioRecoder(_("ALSA device: ") + i, options=[":input-slave=alsa://" + i])

    tmp = [i for i in os.listdir("/dev/snd/") if re.match(r"^pcmC.*D.*c$", i)]
    tmp = list(map(lambda i: chname(i), tmp))
    tmp.insert(0, DevAudioRecoder(_("Defult Device (ALSA)"), options=[":input-slave=alsa://"]))
    tmp.insert(0, DevAudioRecoder(_("Defult Device (Pulseaudio)"), options=[":input-slave=pulse://"]))
    tmp.insert(0, DevAudioRecoder(_("Disable")))
    return tmp

def colon_escape(i):
    return i.replace(":", "\\:")

def list_webcam_windows():
    tmp = []
    tmp.insert(0, DevWebcam(_("Desktop Screen"), "screen://", extra_options=[":input-slave=dshow://"]))
    tmp.insert(0, DevWebcam(_("Default Device"), "dshow://"))
    #tmp.insert(0, DevWebcam(_("Default Device"), "dshow://"), extra_options=[':dshow-vdev=xxxx'])
    return tmp

def list_audiorecoder_windows():
    tmp = []
    tmp.insert(0, DevAudioRecoder(_("Default Device")))
    tmp.insert(0, DevAudioRecoder(_("Disable"), ":dshow-adev=none"))
    #tmp.insert(0, DevAudioRecoder("",":dshow-adev=xxx"))
    return tmp

class StartLiveDialog(Window):
    def __init__(self, parent):
        super().__init__(parent.app, "start_live")
        self.parent = parent
        self.window.set_transient_for(parent.window)
        self.mid = parent.mid
        self.mcode = parent.mcode

        self.list_of_video_inputs = None
        self.list_of_audio_inputs = None

        if sys.platform == "win32":
            self.list_of_video_inputs = list_webcam_windows()
            self.list_of_audio_inputs = list_audiorecoder_windows()
        elif sys.platform == "linux":
            self.list_of_video_inputs = list_webcam_linux()
            self.list_of_audio_inputs = list_audiorecoder_linux()

        videos = self.get("videos")
        model = Gtk.ListStore(str, DevWebcam)
        for i in self.list_of_video_inputs:
            model.append([i.name, i])
        videos.set_model(model)
        videos.set_active(0)

        audios = self.get("audios")
        model = Gtk.ListStore(str, DevAudioRecoder)
        for i in self.list_of_audio_inputs:
            model.append([i.name, i])
        audios.set_model(model)
        audios.set_active(0)

        self.window.show_all()

    def on_ok_clicked(self, button):

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
