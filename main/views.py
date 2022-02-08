from django.shortcuts import render
from six import string_types
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
import cv2
import numpy as np 
import base64
from django.core.files.base import ContentFile
from django.db.models import Q, Count
# Create your views here.

class ImageUploadAPI(APIView):
    def get_queryset(self):
        return Image.objects.all()
    
    def post(self, request, *args, **kwargs):
        try:
            images = dict(request.FILES)['image']
            for image in images:
                image = ImageSerializer(data = {'image' : image})
                if image.is_valid():
                    image.save()
                else:
                    return Response(data={'message':image.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            return Response(data={'message':'Images uploaded successfully'}, status=status.HTTP_201_CREATED)
            
        except KeyError:
            image = ImageSerializer(data = request.FILES)
            if not image.is_valid():
                return Response(data={'message':image.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            


    def get(self, request, *args, **kwargs):
        images = [ImageSerializer(image).data for image in Image.objects.all()]
        return Response(data = images )

def decode_base64_file(data):

    def get_file_extension(file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    from django.core.files.base import ContentFile
    import base64
    import six
    import uuid

    # Check if this is a base64 string
    if isinstance(data, string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension, )

        return ContentFile(decoded_file, name=complete_file_name)

class EncodedImageUploadAPI(ImageUploadAPI):
    def post(self, request, *args, **kwargs):
        print(request.POST.get('image')[:100])
        # image = Image(image=decode_base64_file(request.POST.get('image')))
        # image.save()
        image = ImageSerializer(data = {'image': decode_base64_file(request.POST.get('image'))})
        if image.is_valid():
            image.save()
        else:
            return Response(data={'message':image.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'message':'Image created'}, status=status.HTTP_201_CREATED)
            
def main_view(request):
    classified_images = Image.objects.filter(~Q(classified_as = None))
    class_labels = dict(Image.classLabels)
    class_label_no_count = classified_images.values('classified_as').annotate(count = Count("classified_as"))
    class_label_count = [[ class_labels[i['classified_as']] , i['count'] ] for i in class_label_no_count]
    print(class_label_count)
    return render(request, 'main/graph.html', {'class_label_count': class_label_count})

def gallery_view(request):
    images = Image.objects.all()
    return render(request, 'main/gallery.html', {'images': images})