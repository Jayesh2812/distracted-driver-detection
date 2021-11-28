from django.urls import path
from .views import ImageUploadAPI, EncodedImageUploadAPI
urlpatterns = [
    path('upload/', ImageUploadAPI.as_view(), name='upload'),
    path('upload-encoded/', EncodedImageUploadAPI.as_view(), name='upload-encoded'),
]
