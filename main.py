import warnings
import cv2
from tkinter import ACTIVE, END, PhotoImage, filedialog
from keras.preprocessing import image


import matplotlib.pyplot as plt
from keras.preprocessing.image import load_img, img_to_array


from tkinter import *
import tkinter as tk
from tkinter import PhotoImage, filedialog
from music_player import open_folder, play_song, move_up, move_down, un_pause, stop, pause

# Now you can use these functions in your current file


import os
from emotion_mode import update_frame
from hand_gesture_mode import handDetector, update_frame_hand

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # warning
warnings.filterwarnings("ignore")


def open_folder_by_path(default_path=None):
    if default_path:
        path = default_path
        print(path)
    else:
        path = filedialog.askdirectory()
        print(path)

    if path:
        os.chdir(path)
        songs = [song for song in os.listdir(path) if song.endswith(".mp3")]
        print(songs)
        playlist.delete(0, END)  # Clear existing items in the playlist
        for song in songs:
            playlist.insert(END, song)


def hand():
    global cap
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    update_frame_hand(cap, detector, panel, root)


def start_camera():
    global cap
    cap = cv2.VideoCapture(0)
    update_frame(cap, panel, root)


def stop_camera():
    cap.release()
    panel.config(image="")
    panel.img = None


root = tk.Tk()
root.title("Camera App")
root.geometry("1480x700")
# root.configure(bg="#0f1a2b")
# Disable window resizing
root.resizable(False, False)

# Create left and right frames
left_frame = tk.Frame(root, width=480, height=600, bg="#0f1a2b")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

# Disable propagation for the left frame
left_frame.pack_propagate(False)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

# Right frame content for camera preview
panel = tk.Label(right_frame)
panel.pack()

# label
music = Label(root, text="", font=("arial", 13), fg="white")
root.title(music.cget("text"))

music_frame = Frame(root, bd=2, relief=RIDGE)
# music_frame.place(x=60, y=75, width=360, height=199)
music_frame.place(x=50, y=10, width=380, height=520)

scroll = Scrollbar(music_frame)
playlist = Listbox(music_frame, width=60, font=("arial", 10), bg="#0f1a2b", fg="white",
                   selectbackground="#21b3de", selectforeground="white",
                   highlightthickness=0, bd=0, activestyle="none",
                   exportselection=False, cursor="hand2")
playlist.config(yscrollcommand=scroll.set)
scroll.pack(side=RIGHT, fill=Y)
playlist.pack(side=LEFT, fill=BOTH, expand=True)

# Left frame content
Button(root, text="Open Playlist", width=13, height=2, font=(
    "arial", 7, "bold"), fg="white", bg="#21b3de", command=lambda: open_folder(playlist)).place(x=60, y=540)

Button(root, text="Emotion Mode", width=12, height=2, font=(
    "arial", 7, "bold"), fg="white", bg="#21b3de", command=start_camera).place(x=148, y=540)

Button(root, text="Hand Gesture Mode", width=15, height=2, font=(
    "arial", 7, "bold"), fg="white", bg="#21b3de", command=hand).place(x=230, y=540)

Button(root, text="Stop Camera", width=12, height=2, font=(
    "arial", 7, "bold"), fg="white", bg="#21b3de", command=stop_camera).place(x=330, y=540)

# Canvas-based buttons
play_button = PhotoImage(file="play.png")
canvas_play = Canvas(root, width=play_button.width(
), height=play_button.height(), bg="#ffffff", bd=0, highlightthickness=0)
canvas_play.place(x=40, y=590)
canvas_play.create_image(0, 0, anchor=NW, image=play_button)
canvas_play.bind("<Button-1>", lambda event: play_song(playlist))

pause_button = PhotoImage(file="pause.png")
canvas_pause = Canvas(root, width=pause_button.width(
), height=pause_button.height(), bg="#ffffff", bd=0, highlightthickness=0)
canvas_pause.place(x=140, y=590)
canvas_pause.create_image(0, 0, anchor=NW, image=pause_button)
canvas_pause.bind("<Button-1>", lambda event: pause())

stop_button = PhotoImage(file="stop.png")
canvas_stop = Canvas(root, width=stop_button.width(
), height=stop_button.height(), bg="#ffffff", bd=0, highlightthickness=0)
canvas_stop.place(x=240, y=590)
canvas_stop.create_image(0, 0, anchor=NW, image=stop_button)
canvas_stop.bind("<Button-1>", lambda event: stop())

resume_button = PhotoImage(file="fastforward.png")
canvas_resume = Canvas(root, width=resume_button.width(
), height=resume_button.height(), bg="#ffffff", bd=0, highlightthickness=0)
canvas_resume.place(x=340, y=590)
canvas_resume.create_image(0, 0, anchor=NW, image=resume_button)
canvas_resume.bind("<Button-1>", lambda event: un_pause())

root.mainloop()
