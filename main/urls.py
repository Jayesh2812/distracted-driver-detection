from django.urls import path
from .views import ImageUploadAPI
urlpatterns = [
    path('upload/', ImageUploadAPI.as_view(), name='upload')
]
