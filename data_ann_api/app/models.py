from django.db import models

# Create your models here.


class ImageRef(models.Model):
    rulebook = models.CharField(max_length=256, null=True, blank=True)
    image_id = models.CharField(max_length=128)
    image = models.ImageField(null=True, blank=True)
    label = models.CharField(max_length=128, null=True, blank=True)
    user_id = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f'{self.image_id} - {self.label}'
