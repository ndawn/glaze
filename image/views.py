import os.path
import uuid
from urllib.request import urlretrieve

from rest_framework.permissions import AllowAny

from image.models import Image
from image.serializers import ImageSerializer
from image.upload import UploadedImageProcessor

from django.http import HttpResponse
from django.urls import reverse
from rest_framework.parsers import FileUploadParser
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.conf import settings
import requests


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def retrieve(self, request, *args, pk=None, **kwargs):
        instance = get_object_or_404(self.queryset, pk=pk)

        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, pk=None, **kwargs):
        instance = get_object_or_404(self.queryset, pk=pk)

        instance.file.delete()
        instance.delete()

        return Response({'status': 'success'})


class ImageRetrieveView(RetrieveAPIView):
    queryset = Image.objects.all()
    authentication_classes = [AllowAny]

    def retrieve(self, request, *args, pk=None, **kwargs):
        instance = get_object_or_404(self.queryset, pk=pk)

        return HttpResponse(instance.file.read(), content_type=instance.mime)


class UploadView(CreateAPIView):
    queryset = Image.objects.none()
    parser_classes = [FileUploadParser]

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({'error': 'no image provided'}, status=400)

        source_file = request.FILES['file']

        if source_file.size > settings.MAX_FILE_SIZE:
            return Response({'error': 'file size exceeds the limit'}, status=400)

        file_uuid = uuid.uuid4()

        destination_file_path = os.path.join(
            settings.MEDIA_ROOT,
            Image.file.field.upload_to,
            str(file_uuid),
        )

        destination_file = open(destination_file_path, 'wb')

        for chunk in source_file.chunks():
            destination_file.write(chunk)

        destination_file.close()

        UploadedImageProcessor.create(
            file_uuid=file_uuid,
            file_path=destination_file_path,
            file_name=source_file.name,
            file_owner=request.user,
        )

        return Response(headers={'Location': reverse('images-detail', kwargs={'pk': str(file_uuid)})},
                        status=303)


class URLUploadView(CreateAPIView):
    queryset = Image.objects.none()

    def post(self, request, *args, **kwargs):
        if 'url' not in request.data:
            return Response({'error': 'no url provided'}, status=400)

        file_name = os.path.basename(request.data['url'])
        file_uuid = uuid.uuid4()

        destination_file_path = os.path.join(
            settings.MEDIA_ROOT,
            Image.file.field.upload_to,
            str(file_uuid),
        )

        head_response = requests.head(request.data['url'])

        if int(head_response.headers.get('Content-Length')) > settings.MAX_FILE_SIZE:
            return Response({'error': 'file size exceeds the limit'}, status=400)

        urlretrieve(request.data['url'], destination_file_path)

        UploadedImageProcessor.create(
            file_uuid=file_uuid,
            file_path=destination_file_path,
            file_name=file_name,
            file_owner=request.user,
        )

        return Response(headers={'Location': reverse('images-detail', kwargs={'pk': str(file_uuid)})},
                        status=303)
