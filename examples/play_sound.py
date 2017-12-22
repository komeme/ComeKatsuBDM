#-*- cording: utf-8 -*-

import subprocess


def play_sound(filename):
    #subprocess.call("play " + filename, shell=True)
    subprocess.call("aplay " + filename, shell=True)

filename = "se7.wav"
play_sound(filename)
