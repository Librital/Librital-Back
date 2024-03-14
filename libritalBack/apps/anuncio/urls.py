from rest_framework import routers
from .serializers import AnuncioSerializer
from .api import AnuncioViewSet

router = routers.DefaultRouter()

router.register('api/anuncio', AnuncioViewSet, AnuncioSerializer)

urlpatterns = router.urls

