from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer

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