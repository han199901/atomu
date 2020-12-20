#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import GObject, Gio

import ctypes

class DevWebcam(GObject.Object):
    def __init__(self, name, options):
        super().__init__()
        self.name = name
        self.options = options

        print(f"DevWebcam found: {self.__dict__}")

class DevAudioRecoder(GObject.Object):
    def __init__(self, name, options):
        super().__init__()
        self.name = name
        self.options = options

        print(f"DevAudioRecoder found: {self.__dict__}")

class StreamPush:
    def __init__(self):
        self.p = None

    def stop(self):
        if self.p:
            self.p.force_exit()
            self.p = None

    def start(self, video: DevWebcam, audio: DevAudioRecoder, sout: str, on_exit):
        self.stop()

        options = ["ffmpeg"]

        if video.options:
            options.extend(video.options)
        if audio.options:
            options.extend(audio.options)

        options.extend(["-f", "rtsp", sout])

        flags = Gio.SubprocessFlags.STDOUT_SILENCE | Gio.SubprocessFlags.STDERR_SILENCE
        self.p = Gio.Subprocess.new(options, flags)

        print(f'start process: {" ".join(options)}')

        def on_done(p, result):
            print("process done.")
            try:
                p.wait_check_finish(result)
            except Exception as e:
                print(e)

            self.stop()
            on_exit(None)

        self.p.wait_check_async(None, on_done)
