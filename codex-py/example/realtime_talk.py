import sounddevice as sd

rec_time = 2
fs = 44100
# print(sd.query_devices())
while True:
    print("正在录制")
    backup_recording = sd.rec(int(rec_time * fs), samplerate=fs, channels=2,device=2)
    sd.wait()
    print("录制完成正在播放")
    sd.play(backup_recording,fs)
    sd.wait()
    