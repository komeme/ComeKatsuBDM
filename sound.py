import subprocess


def play_sound(filename):
    subprocess.call("aplay " + filename, shell=True)


def alert():
    subprocess.call("aplay assets/alert.wav", shell=True)

def touch_sound():
    subprocess.call("aplay assets/touch.wav", shell=True)