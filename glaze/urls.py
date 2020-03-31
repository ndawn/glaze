import glaze.router

import rest_framework.urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(glaze.router), name='api'),
]
