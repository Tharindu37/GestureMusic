from keras.models import load_model
import cv2
import time
from PIL import Image, ImageTk
from keras.preprocessing import image
import numpy as np

global start_time
start_time = time.time()
interval = 10
# load model
model = load_model("best_model.h5")
face_haar_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def update_frame(cap, panel, root):
    global start_time, predicted_emotion  # Reference the global variables

    ret, test_img = cap.read()
    test_img = cv2.flip(test_img, 1)

    if not ret:
        return

    predicted_emotion = ""  # Initialize predicted_emotion outside the loop

    gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

    for (x, y, w, h) in faces_detected:
        cv2.rectangle(test_img, (x, y), (x + w, y + h),
                      (255, 0, 0), thickness=7)
        roi_gray = gray_img[y:y + w, x:x + h]
        roi_gray = cv2.resize(roi_gray, (224, 224))
        img_pixels = image.img_to_array(roi_gray)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels /= 255

        predictions = model.predict(img_pixels)
        max_index = np.argmax(predictions[0])
        emotions = ('angry', 'disgust', 'fear', 'happy',
                    'sad', 'surprise', 'neutral')
        predicted_emotion = emotions[max_index]
        # if predicted_emotion == 'angry':
        # open_folder_by_path('C:\\Users\\ASUS\\Music\\Kasun')

        cv2.putText(test_img, predicted_emotion, (int(x), int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Convert the image back to BGR format
    bgr_img = cv2.cvtColor(test_img, cv2.COLOR_RGB2BGR)

    resized_img = cv2.resize(bgr_img, (1000, 700))
    img = Image.fromarray(resized_img)
    img = ImageTk.PhotoImage(image=img)
    panel.img = img
    panel.config(image=img)

    elapsed_time = time.time() - start_time
    if elapsed_time >= interval:
        start_time = time.time()  # Reset the start time
        print(f"Emotion after {interval} seconds: {predicted_emotion}")

    # root.after(10, update_frame)
    root.after(10, update_frame, cap, panel, root)
