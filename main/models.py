from django.db import models
from django.conf import settings
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.


def update_filename(intance, filename):
    last_image = Image.objects.last()
    id = last_image.id if last_image else 0
    return f"Image_{id}.{filename.split('.')[-1]}"

class Image(models.Model):
    image = models.ImageField(upload_to = update_filename)
    uploaded_at = models.DateTimeField(auto_now = True)



@receiver(post_delete, sender = Image)
def delete_actual_image(sender, instance, *args, **kwargs):
    os.remove(f"{settings.MEDIA_ROOT}\{instance.image}")


