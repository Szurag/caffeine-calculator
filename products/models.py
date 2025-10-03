from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe

from media.models import Media


class Product(models.Model):
    name = models.CharField(max_length=200)
    caffeine_mg = models.FloatField()
    is_global = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    photo = models.ForeignKey(Media, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.photo and self.photo.file:
            return mark_safe(f'<img src="{self.photo.file.url}" width="80" height="80" />')
        return "No image"

    image_tag.short_description = "Preview"
