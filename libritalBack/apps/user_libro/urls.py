from rest_framework import routers
from .serializers import libro_UsuarioSerializer
from .api import libro_UsuarioViewSet
from django.urls import path

from .views import *

router = routers.DefaultRouter()

router.register('api/libro_usuario', libro_UsuarioViewSet, 'libro_usuario')

urlpatterns = router.urls

urlpatterns += [path('api/libro_usuario/saveUserLibro', saveUserLibro),
                path('api/libro_usuario/cargarInfoLibroUser', cargarInfoLibroUser),
                path('api/libro_usuario/cargarInfoLibro', cargarInfoLibro),
                path('api/libro_usuario/eliminarValoracionUsuario', eliminarValoracionUsuario),
                path('api/libro_usuario/obtenerMejoresLibros', obtenerMejoresLibros),
                path('api/libro_usuario/obtenerEtiquetasDefaultUserLibro', obtenerEtiquetasDefaultUserLibro),
                path('api/libro_usuario/addFavoritoLibroUser', addFavoritoLibroUser),
                path('api/libro_usuario/addReadLaterUserLibro', addReadLaterUserLibro),
                path('api/libro_usuario/addTerminadoLeerUserLibro', addTerminadoLeerUserLibro),
                path('api/libro_usuario/addActualmenteLeyendoUserLibro', addActualmenteLeyendoUserLibro),
                path('api/libro_usuario/addBibliotecaUserLibro', addBibliotecaUserLibro),]
