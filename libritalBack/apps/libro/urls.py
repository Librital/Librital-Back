from django.urls import path
from rest_framework import routers
from .api import LibroViewSet
from .views import *

router = routers.DefaultRouter()

router.register('api/libro', LibroViewSet, 'libro')

urlpatterns = router.urls

urlpatterns += [path('api/libro/identificarISBN', identificarISBN),
                path('api/libro/obtenerLibros', obtenerLibros),
                path('api/libro/obtenerLibroId/<int:id>/', obtenerLibroId),
                path('api/libro/obtenerNewArrivals', obtenerNewArrivals),
                path('api/libro/identificarISBN', identificarISBN),
                path('api/libro/addLibroNuevoBiblioteca', addLibroNuevoBiblioteca),]
