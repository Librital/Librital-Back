from django.urls import path
from rest_framework import routers
from .api import EtiquetaViewSet

from .views import *

router = routers.DefaultRouter()

router.register('api/etiqueta', EtiquetaViewSet, 'etiqueta')

urlpatterns = router.urls

urlpatterns += [path('api/etiqueta/addEtiquetaUserLibro', addEtiquetaUserLibro),
                path('api/etiqueta/obtenerEtiquetasCustomUserLibro', obtenerEtiquetasCustomUserLibro),
                path('api/etiqueta/removeEtiquetaCustomUserLibro', removeEtiquetaCustomUserLibro),
                path('api/etiqueta/obtenerTodasEtiquetasCustomUser/<int:id_user>', obtenerTodasEtiquetasCustomUser),]
