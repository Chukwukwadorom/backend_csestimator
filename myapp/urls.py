from django.urls import path
from .views import ImageUploadView
from .views import AverageComparisonView


    



urlpatterns = [
    # path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('predict/', ImageUploadView.as_view(), name='predict'),
    path('comparison/average/', AverageComparisonView.as_view(), name='average-comparison'),
]