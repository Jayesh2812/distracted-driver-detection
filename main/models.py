from django.db import models
from django.conf import settings
import os
from django.db.models.enums import Choices
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from datetime import timezone, datetime

# Create your models here.


def update_filename(intance, filename):
    last_image = Image.objects.last()
    id = last_image.id if last_image else 0
    return f"Image_{id}.{filename.split('.')[-1]}"

class Image(models.Model):
    classLabels = [
        ('0' , "drinking"),
        ('1' , "hair and makeup"),
        ('2' , "reaching behind"),
        ('3' , "operating the radio"),
        ('4' , "safe driving"),
        ('5' , "talking on the phone - left"),
        ('6' , "talking on the phone - right"),
        ('7' , "talking to passenger"),
        ('8' , "texting - left"),
        ('9' , "texting - right")
    ]
    image = models.ImageField(upload_to = update_filename)
    uploaded_at = models.DateTimeField(blank = True, null = True)
    classified_as = models.CharField(max_length = 1, choices = classLabels, null = True, default = None)


@receiver(post_save, sender=Image) 
def add_uploaded_time(sender, instance: Image, created : bool, **kwargs):
    if created:
        instance.uploaded_at = datetime.now(timezone.utc)
        instance.save()




@receiver(post_delete, sender = Image)
def delete_actual_image(sender, instance, *args, **kwargs):
    os.remove(f"{settings.MEDIA_ROOT}\{instance.image}")


