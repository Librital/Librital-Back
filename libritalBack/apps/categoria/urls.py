from rest_framework import routers
from .api import CategoriaViewSet

router = routers.DefaultRouter()

router.register('categoria', CategoriaViewSet)

urlpatterns = router.urls

