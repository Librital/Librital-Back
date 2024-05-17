from django.urls import path
from rest_framework import routers
from .api import MapaViewSet

from .views import *

router = routers.DefaultRouter()

router.register('api/mapa', MapaViewSet, 'mapa')

urlpatterns = router.urls

urlpatterns += [path('api/mapa/obtenerTodosMarkerMapa', obtenerTodosMarkerMapa),
                path('api/mapa/addMarcadorMapaUser', addMarcadorMapaUser),
                path('api/mapa/obtenerMarkerUserMapa', obtenerMarkerUserMapa),
                path('api/mapa/desactivarPuntoMapaUser', desactivarPuntoMapaUser),
                path('api/mapa/obtenerTodosMarkerMapaAdmin', obtenerTodosMarkerMapaAdmin),
                path('api/mapa/buscarMarcadorLatitudLongitud', buscarMarcadorLatitudLongitud),
                path('api/mapa/actualizarPuntoMapa', actualizarPuntoMapa),
                path('api/mapa/eliminarPuntoMapa', eliminarPuntoMapa),]