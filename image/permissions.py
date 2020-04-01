from image.models import Image

from rest_framework.permissions import BasePermission


class IsImageOwner(BasePermission):
    def has_permission(self, request, view):
        image_instance = Image.objects.get(pk=view.kwargs['pk'])

        return image_instance.owner == request.user
