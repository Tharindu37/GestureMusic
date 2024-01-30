from keras.models import load_model
import cv2
from keras.preprocessing import image
import numpy as np
from keras.models import load_model
import cv2
from keras.preprocessing import image
import numpy as np


class EmotionPredictor:
    # def __init__(self, model_path="E:/HCI_Project/GestureMusic/best_model.h5"):
    def __init__(self, model_path="E:/HCI_Project/GestureMusic/best_model.h5"):
        self.model = load_model(model_path)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def predict_emotion(self, frame):
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces_detected = self.face_cascade.detectMultiScale(gray_img, 1.32, 5)

        predicted_emotion = ""
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (255, 0, 0), thickness=7)
            roi_gray = gray_img[y:y + w, x:x + h]
            roi_gray = cv2.resize(roi_gray, (224, 224))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255

            predictions = self.model.predict(img_pixels)
            max_index = np.argmax(predictions[0])
            emotions = ('angry', 'disgust', 'fear', 'happy',
                        'sad', 'surprise', 'neutral')
            predicted_emotion = emotions[max_index]
            break  # Only process the first face detected

        return predicted_emotion
