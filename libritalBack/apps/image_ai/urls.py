from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import procesarImagenLibro
from django.urls import path


urlpatterns = [path('api/image/procesarImagenLibro', procesarImagenLibro)]

