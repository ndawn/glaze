from image.models import Image

from django.db import models


class TransformationChain(models.Model):
    id = models.CharField(
        primary_key=True,
        null=False,
        blank=False,
        max_length=256,
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
    )

    file = models.ImageField(
        upload_to='transformations',
        max_length=512,
    )

    extension = models.CharField(
        max_length=32,
        default='',
    )

    mime = models.CharField(
        max_length=64,
        default='',
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )
