from rest_framework import routers
from .views import *
from .api import UsuarioViewSet
from django.urls import path

router = routers.DefaultRouter()

router.register('api/usuario', UsuarioViewSet, 'usuario')

urlpatterns = router.urls

urlpatterns += [path('api/usuario/registrarUsuario', registrarUsuario),
                # path('api/usuario/loginUsuario', loginUsuario),
                path('api/usuario/actualizarInfoUsuario', actualizarInfoUsuario),
                path('api/token', obtenerJWT_Token),
                path('api/usuario/cambiarPasswordUsuario', cambiarPasswordUsuario),
                path('api/usuario/cambiarImagenPerfil', cambiarImagenPerfil),
                ]

