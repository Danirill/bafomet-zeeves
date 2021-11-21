import uuid as uuid
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.safestring import mark_safe




class Image(models.Model):
    image = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(['pdf', 'jpg', 'svg', 'png', 'gif', 'webp'])])
    url = models.URLField(blank=True, null=True)
    owner = models.CharField(max_length=3000, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    uuid = models.UUIDField(auto_created=True, editable=True, default=uuid.uuid4, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def thumbnail_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.image.url))
        elif self.url:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.url))
        return ""

    def __str__(self):
        if self.image:
            return f'FILE {self.image.name}'
        return f'{self.url}'


class NFTRequest(models.Model):
    key = models.CharField(max_length=100, unique=True, null=False, blank=False)
    owner = models.CharField(max_length=3000, null=True, blank=True)
    result = models.ManyToManyField(Image, blank=True)
    data = models.JSONField(null=True, blank=True)
    broken = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.key}'


