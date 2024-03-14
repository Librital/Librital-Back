from rest_framework import viewsets, permissions
from .models import libro_Categoria

from .serializers import libro_CategoriaSerializer

class libro_CategoriaViewSet(viewsets.ModelViewSet):
    queryset = libro_Categoria.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = libro_CategoriaSerializer

