from rest_framework import viewsets, permissions
from .models import Categoria

from .serializers import CategoriaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CategoriaSerializer
