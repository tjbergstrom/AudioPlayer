



# not a GUI, just a start

from pygame import mixer
from imutils import paths
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--song", required=True, help="path to input song (i.e., directory of songs)")
args = vars(ap.parse_args())

songPaths = sorted(list(paths.list_images(args["song"])))

mixer.init()

mixer.music.load("Clairo - Bags.mp3")
mixer.music.set_volume(0.8)
mixer.music.play()
while True:
    print("Press p to pause and c to continue")
    print("press q to quit")
    query = input(">>> ")
    if query == 'p':
        mixer.music.pause()
    elif query == 'c':
        mixer.music.unpaused()
    elif query == 'q':
        mixer.music.stop()
        break



'''
for songPath in songPaths:
    #song = mixer.music.load(songPath)
    song = mixer.music.load('Clairo - Bags.mp3')
    mixer.music.set_volume(0.8)
    mixer.music.play()
    while True:
        print("Press p to pause and c to continue")
        print("press q to quit")
        query = input(">>> ")
        if query == 'p':
            mixer.music.pause()
        elif query == 'c':
            mixer.music.unpaused()
        elif query == 'q':
            mixer.music.stop()
            break
'''

print("task failed successfully")

