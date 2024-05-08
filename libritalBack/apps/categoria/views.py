from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Categoria
from .serializers import CategoriaSerializer


# Create your views here.


@api_view(['GET'])
def obtenerCategorias(request):

    if request.method == 'GET':
        categorias = Categoria.objects.filter(sub_categoria_id__isnull=True, es_activo=1).all()
        serializer = CategoriaSerializer(categorias, many=True)

        return Response(serializer.data)
