from rest_framework import viewsets, permissions
from .models import libro_Usuario

from .serializers import libro_UsuarioSerializer


class libro_UsuarioViewSet(viewsets.ModelViewSet):
    queryset = libro_Usuario.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = libro_UsuarioSerializer
