
from image.models import Image

from django.urls import reverse
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url', 'name', 'extension', 'mime', 'tags']

    url = SerializerMethodField()

    def get_url(self, instance):
        return reverse('image_view', kwargs={'pk': str(instance.id)})
