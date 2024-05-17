from rest_framework import viewsets, permissions
from .models import Mapa

from .serializers import MapaSerializer

class MapaViewSet(viewsets.ModelViewSet):
    queryset = Mapa.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = MapaSerializer