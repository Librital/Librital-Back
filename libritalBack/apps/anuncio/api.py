from rest_framework import viewsets, permissions
from .models import Anuncio
from .serializers import AnuncioSerializer

class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnuncioSerializer
