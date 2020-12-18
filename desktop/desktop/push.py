#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import GObject

import ctypes

import vlc

class DevWebcam(GObject.Object):
    def __init__(self, name, mrl, extra_options=None):
        super().__init__()
        self.name = name
        self.mrl = mrl
        self.extra_options = None
        if extra_options:
            self.extra_options = extra_options

        print(f"DevWebcam found: {self.__dict__}")

class DevAudioRecoder(GObject.Object):
    def __init__(self, name, options=None):
        super().__init__()
        self.name = name
        self.options = None
        if options:
            self.options = options

        print(f"DevAudioRecoder found: {self.__dict__}")

class StreamPush:
    def __init__(self):
        self.vlcInstance = vlc.Instance(["--no-xlib"])

    def stop(self):
        self.vlcInstance.vlm_stop_media("def")

    def start(self, video: DevWebcam, audio: DevAudioRecoder, sout: str):
        self.vlcInstance.vlm_stop_media("def")

        options = video.extra_options
        if not options:
            options = []
        if audio.options:
            options.extend(audio.options)

        l = len(options)
        options = list(map(lambda i: i.encode('utf-8'), options))

        self.vlcInstance.vlm_add_broadcast("def", video.mrl, sout, l, options, True, False)
        self.vlcInstance.vlm_play_media("def")
