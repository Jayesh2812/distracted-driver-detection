from django.contrib import admin
from .models import Image
from django.utils.html import format_html
from django.conf import settings
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .classify import classify_image

# Register your models here.
def classify_selected_images(modeladmin, request, images):

    for image in images:
        classify_image(image.id)

class ImageAdmin(ImportExportModelAdmin):
    list_display = ['image_name', 'preview', 'link', 'uploaded_at', 'classified_as']
    actions = [classify_selected_images]

    def image_name(self, obj):
        return obj.image

    def classified(self,obj):
        return not not obj.classified_as

    classified.boolean = True
    
    def preview(self, obj):
        image_url = f'{settings.MEDIA_URL}{obj.image}'
        return format_html(f'''<a target="_blank" href="{image_url}">
                            <img width="100" src="{image_url}"/>  
                            </a>''')

    def link(self, obj):
        return f'{settings.MEDIA_URL}{obj.image}'
admin.site.register(Image, ImageAdmin)
