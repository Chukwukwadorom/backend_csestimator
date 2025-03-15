import uuid
import io
import boto3
import traceback
import json
import numpy as np
import cv2
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .models import RealMeasurement, PredictedMeasurement
from .process_image import process_images, predict_sizes
from .chart_comparison import generate_average_comparison_chart

class ImageUploadView(APIView):
    parser_classes = [MultiPartParser]

    def upload_to_s3(self, file_content, folder, file_name):
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            s3.upload_fileobj(
                io.BytesIO(file_content), 
                settings.AWS_STORAGE_BUCKET_NAME, 
                f"{folder}/{file_name}"
            )
        except Exception as e:
            raise Exception(f"Failed to upload to S3: {str(e)}")

    def post(self, request, *args, **kwargs):
        try:
            front_img = request.FILES.get('front_image')
            side_img = request.FILES.get('side_image')
            consent = request.data.get('consent') == 'true'
            real_measurements = request.data.get('real_measurements')

            if not front_img or not side_img:
                return Response({'error': 'Please provide both front and side images'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate a unique image name (UUID)
            image_name = f"{uuid.uuid4()}.jpg"

            # Read the file contents into memory
            front_img_content = front_img.read()
            side_img_content = side_img.read()

            
            # Process the images using the content from memory
            front_img_processed = process_images(io.BytesIO(front_img_content))
            side_img_processed = process_images(io.BytesIO(side_img_content))

            # Predict measurements
            predicted_measurements = predict_sizes(front_img_processed, side_img_processed)

            if consent and real_measurements:
                try:
                    self.upload_to_s3(front_img_content, 'front_images', image_name)
                    self.upload_to_s3(side_img_content, 'side_images', image_name)

                    measurements_dict = json.loads(real_measurements)  #parse JSON string to dict
                    measurements_dict["image_name"] = image_name
                    real_measurement = RealMeasurement(**measurements_dict)
                    real_measurement.save()
                    print("Real measurements saved to database.")
                    predicted_measurements["image_name"] = image_name
                    predicted_measurement = PredictedMeasurement(**predicted_measurements)
                    predicted_measurement.save()
                    print("Predicted measurements saved to database.")
                except Exception as e:
                    print(f"Error saving real measurements: {str(e)}")
                    print(traceback.format_exc())

            return Response(predicted_measurements, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            print("Error occurred: ", str(e))
            print(traceback.format_exc())  # Print the full stack trace
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AverageComparisonView(APIView):

    def get(self, request):
        try:
            # Generate and return the average comparison chart
            return generate_average_comparison_chart()
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

