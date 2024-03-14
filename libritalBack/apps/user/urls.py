from rest_framework import routers

from .api import UsuarioViewSet

router = routers.DefaultRouter()

router.register('api/usuario', UsuarioViewSet, 'usuario')

urlpatterns = router.urls
