from winext import device

print("[Video Input]")
videos = device.getVideoInputDeviceList()
print(videos)
print("[Audio Input]")
audios = device.getAudioInputDeviceList()
print(audios)