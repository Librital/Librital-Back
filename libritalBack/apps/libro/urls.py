from rest_framework import routers
from .api import LibroViewSet

router = routers.DefaultRouter()

router.register('api/libro', LibroViewSet, 'libro')

urlpatterns = router.urls
