import uuid

from accounts.models import User

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Image(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        default='',
    )

    file_type = models.CharField(
        max_length=32,
        default='',
    )

    mime = models.CharField(
        max_length=64,
        default='',
    )

    tags = ArrayField(
        models.CharField(
            max_length=255,
            default='',
        ),
        default=list,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    file = models.ImageField(
        upload_to='storage',
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )
