from background_task import background
from .models import Image
from random import randint
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Image) 
def create_profile(sender, instance: Image, created : bool, **kwargs):
    if created:
        classify_image(instance.id)

@background
def classify_image(image_id: int):
    # do something with image
    image = Image.objects.get(id = image_id)
    class_number = classify(image)
    print('Class', image_id, class_number)
    image.classified_as = str(class_number)
    image.save()

def classify(image : Image):
    # Actual Classification
    return randint(0, 9)