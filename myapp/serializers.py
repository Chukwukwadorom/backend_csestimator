from rest_framework import serializers
from .models import Image
from .models import RealMeasurement

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'uploaded_at']



class RealMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealMeasurement
        fields = [
            'image_name', 'ankle', 'armLength', 'bicep', 'calf', 'chest', 
            'forearm', 'height', 'hip', 'legLength', 'shoulderBreadth', 
            'shoulderToCrotch', 'thigh', 'waist', 'wrist'
        ]
