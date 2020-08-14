# retroplayer.py
# April 2020
# Plays mp3s and wavs through VLC
# Loads a gif of some retro cassette tape
# And the tape spins while playing
# Starts up with a cassette tape loading sound effect
# Clicking next/prev track plays a cassette winding sound effect
# Expand the window to the right to see the playlist

# python3 retroplayer.py


from ttkthemes import ThemedStyle
from itertools import count
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
import time
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
        self.status.set("-NotPlaying")
        self.wind = "../cassette winding soundeffect.mp3"
        self.tapedeck = "../cassette inserting soundeffect.mp3"

        #######################################
        # display the track currently playing #
        #######################################
        trackframe = LabelFrame(self.root,
        fg="white", bd=0, relief=GROOVE)
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
        self.playlist.pack(fill=BOTH)

        ####################
        # playback buttons #
        ####################
        buttonframe = LabelFrame(self.root)
        buttonframe.place(x=0, y=269, width=385, height=193)
        playpausebtn = Button(buttonframe, text=">||", command=self.playpause,
        width=7, height=1).grid(row=0, column=1, padx=10, pady=5)
        ffwdbtn = Button(buttonframe, text=">>", command=self.ffwd,
        width=7, height=1).grid(row=0, column=2, padx=6, pady=5)
        rwdbtn = Button(buttonframe, text="<<", command=self.rwd,
        width=7, height=1).grid(row=0, column=0, padx=6, pady=5)
        stopbtn = Button(buttonframe, text="[_]", command=self.stopsong,
        width=7, height=1).grid(row=0, column=3, padx=10, pady=5)

        #################################
        # get songs and add to playlist #
        #################################
        os.chdir("playlist")
        songtracks = os.listdir()
        self.pl = []
        for track in songtracks:
            self.playlist.insert(END, os.path.splitext(track)[0])
            self.pl.append(track)
            self.lasttrack = track
        self.p = vlc.MediaPlayer()
        self.load()

    #######################
    # playback operations #
    #######################
    def load(self):
        self.p = vlc.MediaPlayer(self.tapedeck)
        self.p.play()
        time.sleep(4)
        self.startup(self.pl[0])

    def startup(self, song):
        self.p = vlc.MediaPlayer(song)
        self.track.set(song)
        self.status.set("-PlayPause")
        self.p.play()

    def stopsong(self):
        self.status.set("-Stopped")
        self.p.stop()
        self.load()

    def playpause(self):
        if self.status.get() == "-NotPlaying":
            self.startup(self.pl[0])
        self.status.set("-PlayPause")
        self.p.pause()

    def ffwd(self):
        curtrack = self.track.get()
        tr = 0
        if curtrack != self.lasttrack:
            for track in self.pl:
                if track == curtrack and tr != 1:
                    tr = 1
                    continue
                if tr == 1:
                    self.ffrw()
                    self.startup(track)
                    break

    def rwd(self):
        curtrack = self.track.get()
        prevtrack = curtrack
        if (self.p.get_time()/1000) < 5.0 and curtrack != self.pl[0]:
            for track in self.pl:
                if track == curtrack:
                    break
                prevtrack = track
        self.ffrw()
        self.startup(prevtrack)

    def ffrw(self):
        self.p.stop()
        self.p = vlc.MediaPlayer(self.wind)
        self.p.play()
        time.sleep(4)


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
lbl.load("tape spinning.gif")
#lbl.load("assets/cassette spinning 3.gif")
#style = ThemedStyle(root)
#style.set_theme("arc")
RetroPlayer(root)
root.mainloop()


# easily change gif dimensions:
# https://ezgif.com/resize/ezgif-7-f720df37ff39.gif



