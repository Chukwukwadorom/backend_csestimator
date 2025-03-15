from django.contrib import admin
# Register your models here.
from .models import RealMeasurement

@admin.register(RealMeasurement)
class RealMeasurementAdmin(admin.ModelAdmin):
    list_display = [
        'image_name', 'ankle', 'armLength', 'bicep', 'calf', 'chest', 
        'forearm', 'height', 'hip', 'legLength', 'shoulderBreadth', 
        'shoulderToCrotch', 'thigh', 'waist', 'wrist'
    ]
    search_fields = ['image_name']
    list_filter = ['height', 'waist', 'chest']