from rest_framework import viewsets, permissions
from .models import Etiqueta

from .serializers import EtiquetaSerializer


class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EtiquetaSerializer
