# -*- coding: utf-8 -*-

URL_PREFIX="http://47.93.29.67"
DEFAULT_VLC_SOUT_TEMP="#transcode{vcodec=h264,scale=Auto,acodec=mp3,ab=128,channels=2,samplerate=44100}:std{access=rtmp,mux=ffmpeg{mux=flv},dst=%(RTMP_URI)s}"
