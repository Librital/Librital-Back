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
                path('api/libro_usuario/obtenerMejoresLibros', obtenerMejoresLibros),]
