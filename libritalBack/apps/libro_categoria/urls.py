from rest_framework import routers
from .api import libro_CategoriaViewSet

router = routers.DefaultRouter()

router.register('api/libro_categoria', libro_CategoriaViewSet, 'libro_categoria')

urlpatterns = router.urls
