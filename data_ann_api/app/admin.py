import requests
from django.conf import settings
from django.contrib import admin

from django.http import HttpResponseRedirect
from django.urls import path

from app.models import ImageRef


@admin.register(ImageRef)
class ImageRefAdmin(admin.ModelAdmin):
    change_list_template = "admin/images_changelist.html"

    actions = ['update_database', ]

    def update_database(self, request):
        try:
            res = requests.get(settings.CLOUDINARY_URL, )
            images = res.json()['resources']
            counter = 0
            for i in images:
                ImageRef.objects.get_or_create(image_id=i.get('public_id'), defaults={
                    'image_url': i.get('url')
                })
                counter += 1
            self.message_user(request, f'Added {counter} new objects')

        except:
            self.message_user(request, 'An error has occurred')
        return HttpResponseRedirect("../")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update/', self.update_database),
        ]
        return my_urls + urls
