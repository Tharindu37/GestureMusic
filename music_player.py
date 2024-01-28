from pygame import mixer
from tkinter import ACTIVE, END, PhotoImage, filedialog
import os
mixer.init()


def open_folder(playlist):
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)
        for song in songs:
            if song.endswith(".mp3"):
                playlist.insert(END, song)


def play_song(playlist):
    music_name = playlist.get(ACTIVE)
    mixer.music.load(playlist.get(ACTIVE))
    mixer.music.play()
    # music.config(text=music_name[0:-4])


def move_up(playlist):
    selected_song = playlist.curselection()
    if selected_song:
        index = selected_song[0]
        if index > 0:
            song = playlist.get(index)
            playlist.delete(index)
            playlist.insert(index - 1, song)
            playlist.selection_set(index - 1)


def move_down(playlist):
    selected_song = playlist.curselection()
    if selected_song:
        index = selected_song[0]
        if index < playlist.size() - 1:
            song = playlist.get(index)
            playlist.delete(index)
            playlist.insert(index + 1, song)
            playlist.selection_set(index + 1)


def un_pause():
    print("un_pause")
    mixer.music.unpause()


def stop():
    print("stop")
    mixer.music.stop()


def pause():
    print("pause")
    mixer.music.pause()
