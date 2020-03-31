from accounts.views import UserViewSet
from image.views import ImageViewSet, UploadView, ImageRetrieveView

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'images', ImageViewSet, basename='images')

urlpatterns = [
    path('authorize/', obtain_auth_token, name='authorize'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('<pk>/', ImageRetrieveView.as_view(), name='image_view'),
    # path('image/<id>/<transformations>/', TransformView.as_view(), name='image_transform'),
] + router.urls
