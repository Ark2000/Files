import time
import os
import subprocess
import json
from datetime import datetime

BEEP_SFX_FILE = './beep.mp3'

def get_android_music_volume():
    result = subprocess.run(['termux-volume'], stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    volume_info = json.loads(output)
    for info in volume_info:
        if info["stream"] == "music":
            return info["volume"]
    return 0

def set_android_music_volume(val):
    subprocess.run(['termux-volume', 'music', str(val)])

def get_hourly_remaining_seconds():
    now = datetime.now()
    next = (60 - now.minute) * 60 - now.second
    return next

def play_beep_sound_on_android():
    # pulseaudio
    vol = 40
    tmp = get_android_music_volume()
    set_android_music_volume(vol)
    os.system('mpv ' + BEEP_SFX_FILE)
    set_android_music_volume(tmp)

def play_beep_sound_on_windows():
    os.system('ffplay ' + BEEP_SFX_FILE + ' -nodisp -loglevel quiet -autoexit')

def main_loop():
    print("hourly-beep is running...")
    for i in range(24 * 7):
        delay = get_hourly_remaining_seconds()
        print("next beep delay:", delay)
        time.sleep(delay)
        if os.name == "nt":
            play_beep_sound_on_windows()
        else:
            play_beep_sound_on_android()

if __name__ == "__main__":
    main_loop()
