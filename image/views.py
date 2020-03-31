import os.path
from urllib.request import urlretrieve

from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser

from image.filetypes import detect_file_type
from image.models import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django.conf import settings

from image.serializers import ImageSerializer


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

        return Response('success')


class ImageRetrieveView(RetrieveAPIView):
    queryset = Image.objects.all()
    authentication_classes = []

    def retrieve(self, request, *args, pk=None, **kwargs):
        instance = get_object_or_404(self.queryset, pk=pk)

        return HttpResponse(instance.file.read(), content_type=instance.mime)


class UploadView(CreateAPIView, RetrieveModelMixin):
    queryset = Image.objects.all()
    parser_classes = [FileUploadParser]

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        if 'url' in request.POST:
            source_file = request.POST['url']
            source_file_name = os.path.basename(source_file)
        elif 'file' in request.FILES:
            source_file = request.FILES['file']
            source_file_name = source_file.name
        else:
            return Response({'error': 'no image provided',
                             'post': str(request.POST),
                             'files': request.FILES['file'].name}, status=400)

        image_instance = Image(name=source_file_name, owner=request.user)

        destination_file_path = os.path.join(
            settings.MEDIA_ROOT,
            image_instance.file.field.upload_to,
            str(image_instance.id),
        )

        if isinstance(source_file, str):
            urlretrieve(source_file, destination_file_path)
        elif isinstance(source_file, InMemoryUploadedFile):
            destination_file = open(destination_file_path, 'wb')

            for chunk in source_file.chunks():
                destination_file.write(chunk)

            destination_file.close()
        else:
            return Response({'error': 'no image provided',
                             'post': str(request.POST),
                             'files': request.FILES['file'].name}, status=400)

        destination_file = open(destination_file_path, 'rb')

        file_type, file_mime = detect_file_type(destination_file.read(16))

        destination_file.close()

        if file_type is None and file_mime is None:
            return Response({'error': 'invalid file type'}, status=400)

        destination_file_path_with_extension = f'{destination_file_path}.{file_type}'

        os.rename(destination_file_path, destination_file_path_with_extension)

        image_instance.mime = file_mime
        image_instance.file = destination_file_path_with_extension
        image_instance.save()

        return Response(headers={'Location': reverse('images-detail', kwargs={'pk': str(image_instance.id)})},
                        status=303)
