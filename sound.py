import subprocess


def play_sound(filename):
    subprocess.call("aplay " + filename, shell=True)


def alert():
    subprocess.call("aplay assets/alert.mp3", shell=True)

def touch_sound():
    subprocess.call("aplay assets/touch.mp3", shell=True)

def locked_sound():
    subprocess.call("aplay assets/locked.mp3", shell=True)