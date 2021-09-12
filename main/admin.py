from django.contrib import admin
from .models import Image
from django.utils.html import format_html
from django.conf import settings

# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_name', 'preview', 'link', 'uploaded_at']

    def image_name(self, obj):
        return obj.image

    def preview(self, obj):
        image_url = f'{settings.MEDIA_URL}{obj.image}'
        return format_html(f'''<a target="_blank" href="{image_url}">
                            <img width="100" src="{image_url}"/>  
                            </a>''')

    def link(self, obj):
        return f'{settings.MEDIA_URL}{obj.image}'
admin.site.register(Image, ImageAdmin)
