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
from .push import DevWebcam, DevAudioRecoder
from .defaults import *

def list_webcam_linux(window):
    tmp = [i for i in os.listdir("/dev/") if re.match(r"^video[0-9]+$", i)]
    def_v4l2 = "/dev/" + tmp[-1]

    tmp = list(map(lambda i: DevWebcam(_("V4L2 device: /dev/") + i, ["-f", "v4l2", "-i", "/dev/" + i]), tmp))

    if "DISPLAY" in os.environ:
        screen = window.get_screen()
        vs = str(screen.get_width()) + "x" + str(screen.get_height())
        tmp.insert(0, DevWebcam(_("Desktop Screen (X11)"), ["-framerate", "25", "-f", "x11grab", "-s", vs, "-i", os.environ["DISPLAY"]]))

    tmp.insert(0, DevWebcam(_("Default Device"), ["-f", "v4l2", "-i", def_v4l2]))

    return tmp

def list_audiorecoder_linux():
    def chname(i):
        i = re.sub(r'^pcmC', 'hw:', i)
        i = re.sub(r'c$', '', i)
        i = re.sub(r'D', ',', i)
        return DevAudioRecoder(_("ALSA device: ") + i, ["-f", "alsa", "-i", i])

    tmp = [i for i in os.listdir("/dev/snd/") if re.match(r"^pcmC.*D.*c$", i)]
    def_alsa = tmp[0]
    tmp = list(map(lambda i: chname(i), tmp))
    tmp.insert(0, DevAudioRecoder(_("Disable"), None))
    tmp.insert(0, DevAudioRecoder(_("Defult Device (ALSA)"), ["-f", "alsa", "-i", def_alsa]))
    tmp.insert(0, DevAudioRecoder(_("Defult Device (Pulseaudio)"), ["-f", "pulse", "-i", "default"]))
    return tmp

def colon_escape(i):
    return i.replace(":", "\\:")

def list_webcam_windows():
    from . import winext
    """
    tmp = winext.device.getVideoInputDeviceList()
    tmp = list(map(lambda i: DevWebcam(_("DirectShow device: ") + i, "dshow://", extra_options=[f":dshow-vdev={colon_escape(i)}"]), tmp))
    tmp.insert(0, DevWebcam(_("Desktop Screen"), "screen://", extra_options=[":input-slave=dshow://"]))
    tmp.insert(0, DevWebcam(_("Default Device"), "dshow://"))
    return tmp
    """

def list_audiorecoder_windows():
    from . import winext
    """
    tmp = winext.device.getAudioInputDeviceList()
    tmp = list(map(lambda i: DevAudioRecoder(_("DirectShow device: ") + i, options=[f":dshow-adev={colon_escape(i)}"]), tmp))
    tmp.insert(0, DevAudioRecoder(_("Default Device")))
    tmp.insert(0, DevAudioRecoder(_("Disable"), options=[":dshow-adev=none"]))
    return tmp
    """

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
            self.list_of_video_inputs = list_webcam_linux(self.window)
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

                videos = self.get("videos")
                audios = self.get("audios")

                i = videos.get_active_iter()
                model = videos.get_model()
                dwebcam = model[i][1]

                i = audios.get_active_iter()
                model = audios.get_model()
                darec = model[i][1]

                self.parent.push_start(dwebcam, darec, \
                    result["upload_addr"], result["download_addr"], result["token"])
                self.window.close()
            except CError as e:
                self.defexphandler(e)

        api_async("/live/start", {
            "id": self.mid,
            "code": self.mcode
        }, on_done)
