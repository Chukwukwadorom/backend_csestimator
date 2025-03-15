import tensorflow as tf
# from tensorflow.keras.preprocessing import image
import numpy as np
import pandas as pd
import cv2


import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'revised_best_model.h5')

model = tf.keras.models.load_model(MODEL_PATH, compile=False)





def process_images(img_file):
    # Read the image file into a numpy array
    img = cv2.imdecode(np.frombuffer(img_file.read(), np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Columns =		 ['ankle', 'arm-length', 'bicep', 'calf', 'chest', 'forearm', 'height', 'hip', 'leg-length', 'shoulder-breadth', 'shoulder-to-crotch', 'thigh', 'waist', 'wrist']
Columns = [
    "ankle", "armLength", "bicep", "calf", "chest", "forearm", 
    "height", "hip", "legLength", "shoulderBreadth", 
    "shoulderToCrotch", "thigh", "waist", "wrist"
]
def predict_sizes(front_img, side_img):
    predicted_measurements = model.predict([front_img, side_img])
    predicted_df = pd.DataFrame(predicted_measurements, columns=Columns)
    return predicted_df