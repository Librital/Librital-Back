from rest_framework import routers
from .api import EtiquetaViewSet

router = routers.DefaultRouter()

router.register('api/etiqueta', EtiquetaViewSet, 'etiqueta')

urlpatterns = router.urls
