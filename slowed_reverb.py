from moviepy.editor import *
import argparse
import os
import sys
import requests

R = '\033[31m'  # red
G = '\033[32m'  # green
B = '\033[34m'  # blue
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

version = "1.0.0"

current_dir = os.path.dirname(os.path.realpath(__file__))

class Generator:
    def __init__(self, videofile, audiofile, audio_type, output_dir, clip_speed=0.5, audio_speed=0.88):
        self.clip = VideoFileClip(videofile)
        self.audio = AudioFileClip(audiofile)
        self.audio_type = audio_type
        self.output_dir = output_dir
        self.clip_speed = clip_speed
        self.audio_speed = audio_speed

    def slow_clip(self, clip):
        return vfx.speedx(clip, factor=self.clip_speed, final_duration=None)

    def slow_audio(self, audio):
        return vfx.speedx(audio, factor=self.audio_speed, final_duration=None)

    def loop_clip(self, clip, audio):
        return clip.fx(vfx.loop, n=None, duration=audio.duration)

    def write_file(self):
        if self.audio_type == "original":
            slowedclip = self.slow_clip(self.clip)
            slowedaudio = self.slow_audio(self.audio)
            loopedclip = self.loop_clip(slowedclip, slowedaudio)
            final = loopedclip.set_audio(slowedaudio)
        elif self.audio_type == "edited":
            slowedclip = self.slow_clip(self.clip)
            loopedclip = self.loop_clip(slowedclip, self.audio)
            final = loopedclip.set_audio(self.audio)

        final.write_videofile(os.path.join(self.output_dir, "output.mp4"), codec="libx264", audio_codec="aac")


def banner():
    text = r"""
         __                       __                                     __
   _____/ /___ _      _____  ____/ /    __     ________ _   _____  _____/ /_
  / ___/ / __ \ | /| / / _ \/ __  /  __/ /_   / ___/ _ \ | / / _ \/ ___/ __ \
 (__  ) / /_/ / |/ |/ /  __/ /_/ /  /_  __/  / /  /  __/ |/ /  __/ /  / /_/ /
/____/_/\____/|__/|__/\___/\__,_/    /_/    /_/   \___/|___/\___/_/  /_.___/"""

    print(B + text + W + '\n')
    print(G + '[>]' + C + ' Created By : ' + W + 'https://github.com/devhambe')
    print(G + '[>]' + C + ' Version    : ' + W + version + '\n')


def menu():
    while True:
        print('\n' + Y + '[!] Actions : ' + W)
        print(G + '[1]' + C + ' Video + original audio' + W)
        print(G + '[2]' + C + ' Video + edited audio' + W)
        print(G + '[0]' + C + ' Exit' + W)

        choice = input('\n' + R + '[>]' + W)

        if choice == "1":
            prompt("original")
        elif choice == "2":
            prompt("edited")
        elif choice == "0":
            sys.exit()
        else:
            print('\n' + R + '[-]' + C + ' Invalid Choice...Try Again.' + W)
            menu()


def version_check():
    print(G + '[+]' + C + ' Checking for Updates...', end='')
    version_url = 'https://raw.githubusercontent.com/devhambe/Slowed_Reverb_Tool/master/version.txt'
    try:
        version_req = requests.get(version_url, timeout=5)
        if version_req.status_code == 200:
            github_version = version_req.text
            github_version = github_version.strip()
            if version == github_version:
                print(C + '[' + G + ' Up-To-Date ' + C + ']' + '\n')
            else:
                print(C + '[' + G + ' Available : {} '.format(github_version) + C + ']' + '\n')
        else:
            print(C + '[' + R + ' Status : {} '.format(version_req.status_code) + C + ']' + '\n')
    except Exception as e:
        print('\n\n' + R + '[-]' + C + ' Exception : ' + W + str(e))


def get_valid_path(text):
    while True:
        path = input(text)

        if not os.path.exists(path):
            print(R + '[-]' + C + ' Invalid path' + W)
            continue
        else:
            break

    return path


def get_valid_speed(text, default):
    while True:
        try:
            speed = input(text)
            if speed == "":
                speed = default
            else:
                speed = float(speed)
        except ValueError:
            print(R + '[-]' + C + ' Invalid speed' + W)
            continue

        if speed <= 0 or speed > 1:
            print(R + '[-]' + C + ' Speed has to be between 0 and 1' + W)
            continue
        else:
            break
    return speed


def prompt(audio_type):
    video = get_valid_path('\n' + G + '[+]' + C + ' Path to video : ' + W)
    audio = get_valid_path('\n' + G + '[+]' + C + ' Path to audio : ' + W)
    video_speed = get_valid_speed('\n' + G + '[+]' + C + ' Video speed (default is 0.5) : ' + W, 0.5)
    if audio_type == "original":
        audio_speed = get_valid_speed('\n' + G + '[+]' + C + ' Audio speed (default is 0.88) : ' + W, 0.88)

    try:
        g = Generator(video, audio, audio_type, current_dir, video_speed, audio_speed)
        g.write_file()
    except Exception as e:
        print(R + '[-]' + C + ' Exception : ' + W + str(e))

try:
    banner()
    version_check()
    menu()
except KeyboardInterrupt:
    print('\n' + R + '[-]' + C + ' Keyboard Interrupt.' + W)
    sys.exit()

# TODO: Add reverb (use ffmpeg?)
