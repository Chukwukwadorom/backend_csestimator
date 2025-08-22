from django.conf import settings
from tensorflow import keras
from dotenv import load_dotenv
import tensorflow as tf
import os
# from tensorflow.keras.preprocessing import image
import numpy as np
import pandas as pd
import cv2
import boto3
from io import BytesIO



MODEL_PATH = "/tmp/my_model.h5"


# Create S3 client (it will automatically pick up keys from env)
BUCKET=settings.AWS_STORAGE_BUCKET_NAME
KEY=settings.S3_MODEL_KEY

# def get_model(BUCKET,KEY):
#     if not os.path.exists(MODEL_PATH):
#         print("Downloading model from S3...")
#         s3 = boto3.client("s3")
#         obj = s3.get_object(Bucket=BUCKET, Key=KEY)
#         bytestream = BytesIO(obj['Body'].read())

#         with open(MODEL_PATH, "wb") as f:
#             f.write(bytestream.getbuffer())

#     print("Loading model from local cache...")
#     return keras.models.load_model(MODEL_PATH, compile=False)


_model = None

def get_model(BUCKET, KEY):
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            print("Downloading model from S3...")
            s3 = boto3.client("s3")
            obj = s3.get_object(Bucket=BUCKET, Key=KEY)
            bytestream = BytesIO(obj['Body'].read())

            with open(MODEL_PATH, "wb") as f:
                f.write(bytestream.getbuffer())

        print("Loading model from local cache...")
        _model = keras.models.load_model(MODEL_PATH, compile=False)
    return _model




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
    model = get_model(BUCKET,KEY)
    predicted_measurements = model.predict([front_img, side_img])
    # predicted_measurements = np.round(predicted_measurements, 1)
    predicted_df = pd.DataFrame(predicted_measurements, columns=Columns)
    return predicted_df