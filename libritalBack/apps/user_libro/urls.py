from rest_framework import routers
from .serializers import libro_UsuarioSerializer
from .api import libro_UsuarioViewSet

router = routers.DefaultRouter()

router.register('api/libro_usuario', libro_UsuarioViewSet, 'libro_usuario')

urlpatterns = router.urls
