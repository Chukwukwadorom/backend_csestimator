from django.db import models

# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class RealMeasurement(models.Model):
    image_name = models.CharField(max_length=100, unique=True)  # Store the image name for reference
    ankle = models.FloatField(null=True, blank=True)
    armLength = models.FloatField(null=True, blank=True)
    bicep = models.FloatField(null=True, blank=True)
    calf = models.FloatField(null=True, blank=True)
    chest = models.FloatField(null=True, blank=True)
    forearm = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    hip = models.FloatField(null=True, blank=True)
    legLength = models.FloatField(null=True, blank=True)
    shoulderBreadth = models.FloatField(null=True, blank=True)
    shoulderToCrotch = models.FloatField(null=True, blank=True)
    thigh = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    wrist = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Measurement for Image: {self.image_name}"


class PredictedMeasurement(models.Model):
    image_name = models.CharField(max_length=100, unique=True)  # Store the image name for reference
    ankle = models.FloatField(null=True, blank=True)
    armLength = models.FloatField(null=True, blank=True)
    bicep = models.FloatField(null=True, blank=True)
    calf = models.FloatField(null=True, blank=True)
    chest = models.FloatField(null=True, blank=True)
    forearm = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    hip = models.FloatField(null=True, blank=True)
    legLength = models.FloatField(null=True, blank=True)
    shoulderBreadth = models.FloatField(null=True, blank=True)
    shoulderToCrotch = models.FloatField(null=True, blank=True)
    thigh = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    wrist = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"predicted Measurement for Image: {self.image_name}"