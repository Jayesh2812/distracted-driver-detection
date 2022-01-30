from django.urls import path
from .views import ImageUploadAPI, EncodedImageUploadAPI, main_view, gallery_view
urlpatterns = [
    path('upload/', ImageUploadAPI.as_view(), name='upload'),
    path('upload-encoded/', EncodedImageUploadAPI.as_view(), name='upload-encoded'),
    path('main/', main_view, name="main-view"),
    path('gallery/', gallery_view, name="gallery")
]
