from accounts.views import UserViewSet
from image.views import ImageViewSet, UploadView, ImageRetrieveView, URLUploadView

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'images', ImageViewSet, basename='images')

urlpatterns = [
    path('authorize/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authorize/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('upload_url/', URLUploadView.as_view(), name='url_upload'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('<pk>/', ImageRetrieveView.as_view(), name='image_view'),
    # path('image/<id>/<transformations>/', TransformView.as_view(), name='image_transform'),
] + router.urls
