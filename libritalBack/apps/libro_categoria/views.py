from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import libro_Categoria
from .models import Categoria
from .serializers import libro_CategoriaSerializer


# Create your views here.

@api_view(['POST'])
def obtenerCategoriaLibro(request):
    if request.method == 'POST':
        data = request.data

        id_libro = data['id_libro']
        listaCategorias = []

        categoria_search = libro_Categoria.objects.filter(id_libro=id_libro, activo=1).values('id_categoria').all()

        if categoria_search is not None:

            if len(categoria_search) > 1:
                for categoria in categoria_search:
                    categorias = Categoria.objects.filter(id=categoria['id_categoria']).values('nombre').first()
                    listaCategorias.append(categorias)

                return Response({'message': 'Obtenida lista',
                                 'categoria': listaCategorias})

            elif len(categoria_search) == 1:
                id_categoria = categoria_search[0]['id_categoria']
                nombre_categoria = Categoria.objects.filter(id=id_categoria).values('nombre').first()

                return Response({'message': 'Obtenido',
                                 'categoria': nombre_categoria})
            else:
                return Response({'message': 'No encontrado'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def obtenerCategoriaLibroAdmin(request):
    if request.method == 'POST':
        data = request.data

        id_libro = data['id']
        listaCategorias = []

        categoria_search = libro_Categoria.objects.filter(id_libro=id_libro).values('id_categoria').all()

        if categoria_search is not None:

            if len(categoria_search) > 1:
                for categoria in categoria_search:
                    categorias = Categoria.objects.filter(id=categoria['id_categoria']).values('nombre').first()
                    listaCategorias.append(categorias)

                return Response({'message': 'Obtenida lista',
                                 'categoria': listaCategorias})

            elif len(categoria_search) == 1:
                id_categoria = categoria_search[0]['id_categoria']
                nombre_categoria = Categoria.objects.filter(id=id_categoria).values('nombre').first()

                return Response({'message': 'Obtenido',
                                 'categoria': nombre_categoria})
            else:

                sin_categoria = {'nombre': 'Sin categoría'}

                return Response({'message': 'No encontrado',
                                 'categoria': sin_categoria})