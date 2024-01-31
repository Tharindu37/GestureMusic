from pygame import mixer
from tkinter import ACTIVE, END, PhotoImage, filedialog
import os
from emotion_mode import EmotionPredictor
from hand_gesture_mode import handDetector
from tkinter import *
import tkinter as tk
import cv2
import time
from PIL import Image, ImageTk

mixer.init()


# def hand_gesture_mode(cap, detector, panel, root):

#     pTime = 0
#     cTime = 0
#     ret, test_img = cap.read()
#     test_img = cv2.flip(test_img, 1)

#     if ret:
#         img = detector.findHands(test_img)
#         lmList = detector.findPosition(img)

#         if len(lmList) != 0:

#             if (lmList[0][2]-lmList[16][2] < 50 and lmList[17][1]-lmList[4][1] > 0):
#                 move_down()
#                 print("down")

#             elif (lmList[0][2]-lmList[16][2] < 100 and lmList[17][1]-lmList[4][1] < 0):
#                 print("Up")
#                 move_up()

#         cTime = time.time()
#         fps = 1/(cTime-pTime)
#         pTime = cTime

#         bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#         resized_img = cv2.resize(bgr_img, (1000, 700))
#         img = Image.fromarray(resized_img)
#         img = ImageTk.PhotoImage(image=img)
#         panel.img = img
#         panel.config(image=img)

#         # Adjust the delay for smoother performance
#         root.after(30, hand_gesture_mode, cap, detector, panel, root)

# Initialize hand state


root = tk.Tk()
root.title("Camera App")
root.geometry("1480x700")
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


# def play_song(playlist):
#     music_name = playlist.get(ACTIVE)
#     mixer.music.load(playlist.get(ACTIVE))
#     mixer.music.play()
# music.config(text=music_name[0:-4])

def emotion_mode(cap, panel, root, emotion_predictor=None, interval=5, start_time=None):
    if emotion_predictor is None:
        emotion_predictor = EmotionPredictor()

    if start_time is None:
        start_time = time.time()

    ret, test_img = cap.read()
    test_img = cv2.flip(test_img, 1)

    if not ret:
        return

    predicted_emotion = emotion_predictor.predict_emotion(test_img)

    # Update panel with the predicted emotion
    cv2.putText(test_img, predicted_emotion, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    bgr_img = cv2.cvtColor(test_img, cv2.COLOR_RGB2BGR)
    resized_img = cv2.resize(bgr_img, (1000, 700))
    img = Image.fromarray(resized_img)
    img = ImageTk.PhotoImage(image=img)
    panel.img = img
    panel.config(image=img)
    print(predicted_emotion)

    elapsed_time = time.time() - start_time
    if elapsed_time >= interval:
        start_time = time.time()
        print(f"Emotion after {interval} seconds: {predicted_emotion}")
        if (predicted_emotion == "angry"):
            open_folder_by_path("C:/Users/ASUS/Music/HCI_Songs/Angry")
        elif (predicted_emotion == "happy"):
            open_folder_by_path("C:/Users/ASUS/Music/HCI_Songs/Happy")
        elif (predicted_emotion == "sad"):
            open_folder_by_path("C:/Users/ASUS/Music/HCI_Songs/Sad")
        elif (predicted_emotion == "neutral"):
            open_folder_by_path("C:/Users/ASUS/Music/HCI_Songs/Neutral")
        elif (predicted_emotion == "fear"):
            open_folder_by_path("C:/Users/ASUS/Music/HCI_Songs/Fear")
        elif (predicted_emotion == "surprise"):
            open_folder_by_path("C:/Users/ASUS/Music/HCI_Songs/Surprise")

    root.after(10, emotion_mode, cap, panel, root,
               emotion_predictor, interval, start_time)


def open_folder(playlist):
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)
        for song in songs:
            if song.endswith(".mp3"):
                playlist.insert(END, song)
        # playlist.selection_set(0)


def un_pause():
    print("un_pause")
    mixer.music.unpause()


def stop():
    print("stop")
    mixer.music.stop()


def pause():
    print("pause")
    mixer.music.pause()


def hand():
    global cap
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    hand_gesture_mode(cap, detector, panel, root)


def start_camera():
    global cap
    cap = cv2.VideoCapture(0)
    emotion_mode(cap, panel, root)


def stop_camera():
    cap.release()
    panel.config(image="")
    panel.img = None


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
        # playlist.selection_set(0)


def play_song():
    music_name = playlist.get(ACTIVE)
    mixer.music.load(playlist.get(ACTIVE))
    mixer.music.play()


def move_up():
    selected_song = playlist.curselection()
    if not selected_song:  # Check if selected_song is empty
        playlist.select_clear(0)
        playlist.selection_set(0)
        playlist.activate(0)
        play_song()
    if selected_song:
        index = selected_song[0]
        if index > 0:
            playlist.select_clear(index)
            playlist.selection_set(index - 1)
            playlist.activate(index - 1)
            play_song()


def move_down():
    selected_song = playlist.curselection()
    if not selected_song:  # Check if selected_song is empty
        playlist.select_clear(0)
        playlist.selection_set(0)
        playlist.activate(0)
        play_song()
    if selected_song:
        index = selected_song[0]
        if index < playlist.size() - 1:
            playlist.select_clear(index)
            playlist.selection_set(index + 1)
            playlist.activate(index + 1)
            play_song()


hand_state = 'none'
music_state = 'none'


def hand_gesture_mode(cap, detector, panel, root):
    global hand_state, music_state
    pTime = 0
    cTime = 0
    ret, test_img = cap.read()
    test_img = cv2.flip(test_img, 1)

    if ret:
        img = detector.findHands(test_img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            # Calculate distances
            # Distance between index and wrist
            distance1 = lmList[0][2] - lmList[16][2]
            # Distance between middle and little finger
            distance2 = lmList[17][1] - lmList[4][1]

            if (lmList[0][2]-lmList[12][2] > 200 and lmList[0][2] - lmList[16][2] > 200):
                hand_state = 'set'

            if (lmList[0][2]-lmList[12][2] > 100 and lmList[0][2]-lmList[8][2] > 100):
                music_state = 'set'
            if distance1 < 50 and distance2 > 0:  # Downward motion detected
                if hand_state != 'none':
                    move_down()
                    hand_state = 'none'

            elif distance1 < 100 and distance2 < 0:  # Upward motion detected
                if hand_state != 'none':
                    move_up()
                    hand_state = 'none'

            print(lmList[5][1]-lmList[4][1])
            if (lmList[0][2] - lmList[12][2] > 200 and lmList[0][2] - lmList[4][2] > 100 and lmList[5][1]-lmList[4][1] < 50):
                stop()

            # if lmList[0][2]-lmList[8][2] > 200 and lmList[0][2]-lmList[12][2] > 200 and lmList[8][2]-lmList[12][2] > 10:
            #     if music_state != 'none':
            #         play_song(playlist)
            #         music_state = 'none'
            # elif lmList[0][2]-lmList[8][2] > 200 and lmList[0][2]-lmList[12][2] > 200 and lmList[8][2]-lmList[12][2] < 10:
            #     if music_state != 'none':
            #         stop()
            #         music_state = 'none'

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        resized_img = cv2.resize(bgr_img, (1000, 700))
        img = Image.fromarray(resized_img)
        img = ImageTk.PhotoImage(image=img)
        panel.img = img
        panel.config(image=img)

        # Adjust the delay for smoother performance
        root.after(30, hand_gesture_mode, cap, detector, panel, root)


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
canvas_play.bind("<Button-1>", lambda event: play_song())

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
