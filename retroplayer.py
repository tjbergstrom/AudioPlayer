# Retro audio player
# Plays mp3s through VLC
# Loads a gif of some retro cassette tape or another
# And the tape spins while playing
# Starts up with a cassette tape loading sound effect
# Not all of the playback buttons work
# It's impossible to replace the buttons with images
# Expand the window to the right to reveal the playlist

# usage:
# python3 retroplayer.py

from ttkthemes import ThemedStyle
from itertools import count
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
import pygame
import vlc
import cv2
import os

class RetroPlayer:
    def __init__(self,root):
        self.root = root
        self.root.title("Retro Player")
        #self.root.geometry("560x320")
        self.root.geometry("385x320")
        self.track = StringVar()
        self.status = StringVar()

        #######################################
        # display the track currently playing #
        #######################################
        trackframe = LabelFrame(self.root,
        bg="grey", fg="white", bd=5, relief=GROOVE)
        #trackframe.place(x=386, y=0)
        trackframe.place(x=90, y=45)
        songtrack = Label(trackframe,
        textvariable=os.path.splitext(str(self.track))[0],
        width=30).grid(row=0, column=0)

        #################################
        # display the playlist of songs #
        #################################
        songsframe = LabelFrame(self.root, text="Playlist",bd=5, relief=GROOVE)
        songsframe.place(x=386, y=0, height=320, width=250)
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set,
        selectmode=SINGLE, height=320, width=250, bg="black", fg="white")
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.select(self.playlist.curselection()))
        self.playlist.pack(fill=BOTH)

        ####################
        # playback buttons #
        ####################
        buttonframe = LabelFrame(self.root)
        buttonframe.place(x=0, y=269, width=385, height=193)
        playbtn = Button(buttonframe, text=">", relief="raised",
        command=self.playsong, width=7, height=1).grid(row=0,
        column=0, padx=10, pady=5)
        pausebtn = Button(buttonframe, text="| |", command=self.pausesong,
        width=7, height=1).grid(row=0, column=1, padx=10, pady=5)
        nextbtn = Button(buttonframe, text=">>>", command=self.nextsong,
        width=7, height=1).grid(row=0, column=2, padx=6, pady=5)
        stopbtn = Button(buttonframe, text="[ ]", command=self.stopsong,
        width=7, height=1).grid(row=0, column=3, padx=10, pady=5)

        #################################
        # get songs and add to playlist #
        #################################
        os.chdir("playlist")
        songtracks = os.listdir()
        for track in songtracks:
            self.playlist.insert(END,track)
        self.p = vlc.MediaPlayer(self.playlist.get(ACTIVE))

    #######################
    # playback operations #
    #######################
    def playsong(self):
        if self.status != "-Playing":
            self.track.set(self.playlist.get(ACTIVE))
            self.status.set("-Playing")
            self.p.play()
        else:
            self.status.set("-Paused")
            self.p.pause()

    def stopsong(self):
        self.status.set("-Stopped")
        self.p.stop()

    def pausesong(self):
        self.status.set("-Paused")
        self.p.pause()

    def nextsong(self):
        self.status.set("-Playing")
        # doesn't work

    def select(self, song):
        self.track.set(song)
        # doesn't work


#######################################
# play the spinning tape cassette gif #
#######################################
class ImageLabel(Label):
    def load(self, im):
        im = Image.open(im)
        self.loc = 0
        self.frames = []
        try:
            for i in range(20):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


##############################
# just initializing stuff... #
##############################
root = Tk()
lbl = ImageLabel(root)
lbl.pack(side="left", anchor=NW)
lbl.load("spinning tape.gif")
#style = ThemedStyle(root)
#style.set_theme("arc")
pygame.init()
pygame.mixer.Sound.play(pygame.mixer.Sound("cassette sound effect.wav"))
RetroPlayer(root)
root.mainloop()
# easily change gif dimensions:
# https://ezgif.com/resize/ezgif-7-f720df37ff39.gif



