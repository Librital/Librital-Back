from django.urls import path
from rest_framework import routers
from .api import CategoriaViewSet

from .views import *

router = routers.DefaultRouter()

router.register('categoria', CategoriaViewSet)

urlpatterns = router.urls

urlpatterns += [path('api/categoria/obtenerCategorias', obtenerCategorias),]

