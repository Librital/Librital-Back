from os import path

from rest_framework import routers
from .api import LibritalViewSet
from .serializers import LibritalSerializer
from django.urls import path

router = routers.DefaultRouter()

router.register('api/librital', LibritalViewSet, 'librital')

urlpatterns = router.urls
# urlpatterns += [path('api/librital/obtener_mensaje', obtener_mensaje),
#                 path('api/librital/recibir', recibir)]




