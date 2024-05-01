from django.urls import path
from rest_framework import routers
from .api import libro_CategoriaViewSet

from .views import *

router = routers.DefaultRouter()

router.register('api/libro_categoria', libro_CategoriaViewSet, 'libro_categoria')

urlpatterns = router.urls

urlpatterns += [path('api/libro_categoria/obtenerCategoriaLibro', obtenerCategoriaLibro)]
