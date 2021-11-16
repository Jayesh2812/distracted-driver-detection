from background_task import background
from .models import Image
from random import randint
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as IMAGE
from tensorflow import Graph
import json
import numpy as np

from codetiming import Timer
t = Timer(name="class")



@receiver(post_save, sender=Image) 
def create_profile(sender, instance: Image, created : bool, **kwargs):
    if created:
        classify_image(instance.id)

@background
def classify_image(image_id: int):
    # do something with image
    image = Image.objects.get(id = image_id)
    class_number = classify(image)
    # print('Class', image_id, class_number)
    image.classified_as = str(class_number)
    image.save()

# model_path = settings.BASE_DIR / "main" / "PNP.h5"
# print(model_path)

def classify(image : Image):
    # start_time = t.start()
    model_path = settings.BASE_DIR / "main" / "PNP.h5"
    # print(model_path)
    model=load_model(model_path)


    # print(f"{settings.MEDIA_URL}{image.image}")
    # print(image.image)
    image_path = settings.BASE_DIR / "media" / str(image.image)
    # Actual Classification

    img=IMAGE.load_img(image_path,target_size=(280,200))
    x = IMAGE.img_to_array(img)
    x=x/255
    x=x.reshape(1,280,200,3)

    # print("this is x",x.shape)
    pred=model.predict(x)

    # print(pred)
    pred = list(pred[0])
    max_val = max(pred)
    label_index = pred.index(max_val)
    # print(max_val, pred.index(max_val))

    label_list = [
        "drinking",
        "hair and makeup",
        "operating the radio",
        "reaching behind",
        "safe driving",
        "talking on the phone - left",
        "talking on the phone - right",
        "talking to passenger",
        "texting - left",
        "texting - right"
    ]
    print()
    print(image.image)
    print("*********", label_list[label_index].capitalize(), "**********")

    # stop_time = t.stop()

    

    return label_index