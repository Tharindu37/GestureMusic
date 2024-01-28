import cv2
import mediapipe as mp
import time
from PIL import Image, ImageTk


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=False):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                # if draw:
                # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList


def update_frame_hand(cap, detector, panel, root):
    pTime = 0
    cTime = 0
    ret, test_img = cap.read()
    test_img = cv2.flip(test_img, 1)

    if ret:
        img = detector.findHands(test_img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            # print(lmList[4][2])
            # print(lmList[8][2])
            # print(lmList[12][2])
            # print("top", lmList[16][2])
            # # print(lmList[20][2])
            # print("bottom", lmList[0][2])
            print("first", lmList[0][2]-lmList[16][2])
            print("second", lmList[17][1]-lmList[4][1])
            if (lmList[0][2]-lmList[16][2] < 50 and lmList[17][1]-lmList[4][1] > 0):
                # move_down()
                print("down")

            elif (lmList[0][2]-lmList[16][2] < 100 and lmList[17][1]-lmList[4][1] < 0):
                print("Up")
                # move_up()

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        resized_img = cv2.resize(bgr_img, (1000, 700))
        img = Image.fromarray(resized_img)
        img = ImageTk.PhotoImage(image=img)
        panel.img = img
        panel.config(image=img)

        # Adjust the delay for smoother performance
        root.after(30, update_frame_hand, cap, detector, panel, root)
