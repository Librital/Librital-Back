from django.db.models import Sum, Max, Count, Avg
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Categoria
from .serializers import CategoriaSerializer, RankingCategoriaSerializer
from ..libro.models import Libro
from ..libro.serailizers import LibroSerializer, LibroCategoriasSerializer
from ..libro_categoria.models import libro_Categoria
from ..user_libro.models import libro_Usuario


# Create your views here.


@api_view(['GET'])
def obtenerCategorias(request):
    if request.method == 'GET':
        categorias = Categoria.objects.filter(sub_categoria_id__isnull=True, es_activo=1).all()
        serializer = CategoriaSerializer(categorias, many=True)

        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def obtenerMejoresLibrosPerCategoria(request):
    if request.method == 'GET':
        data = request.data

        categorias = Categoria.objects.filter(sub_categoria_id__isnull=True, es_activo=1)

        mejores_libros_por_categoria = []
        num_votos = []
        for categoria in categorias:
            libros_categoria_actual = libro_Categoria.objects.filter(id_categoria=categoria.id, activo=1)

            # Obtener los IDs de los libros asociados a la categoría actual
            libros_ids = libros_categoria_actual.values_list('id_libro', flat=True)

            # Filtrar los libros con esos IDs
            libros = Libro.objects.filter(id_libro__in=libros_ids, es_activo=1)

            # Obtener el mejor libro valorado, el número de votos y los nombres de las categorías
            mejor_libro = libros.filter(libro_usuario__calificacion__gt=0).annotate(
                max_calificacion=Max('libro_usuario__calificacion'),
                num_votos=Count('libro_usuario__calificacion')
            ).order_by('-max_calificacion').first()

            if mejor_libro:
                # Obtener los nombres de las categorías para este libro
                nombres_categorias = [c.nombre for c in Categoria.objects.filter(
                    id__in=libros_categoria_actual.values_list('id_categoria', flat=True))]
                mejor_libro.nombres_categorias = nombres_categorias
                mejores_libros_por_categoria.append(mejor_libro)
                num_votos.append(mejor_libro.num_votos)

        librosResultados = LibroCategoriasSerializer(mejores_libros_por_categoria, many=True)

        return Response({'message': 'Obtenido',
                         'libros': librosResultados.data,
                         'num_votos': num_votos})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def obtenerLibrosPerCategoria(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()

        resultado = []

        for categoria in categorias:
            num_libros = libro_Categoria.objects.filter(id_categoria=categoria.id, activo=1).count()

            nombre_categoria = categoria.nombre

            resultado.append({'name': nombre_categoria, 'value': num_libros})

        return Response({'message': 'Obtenido',
                         'libros_por_categoria': resultado})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def obtenerBestCategorias(request):
    # Obtener todas las categorías
    categorias = Categoria.objects.all()

    mejores_categorias = []

    # Iterar sobre cada categoría
    for categoria in categorias:
        # Obtener los libros asociados a la categoría
        libros_categoria = libro_Categoria.objects.filter(id_categoria=categoria.id, activo=1)

        # Obtener las valoraciones promedio de los libros de esta categoría
        valoracion_promedio = libros_categoria.aggregate(promedio=Avg('id_libro__libro_usuario__calificacion'))[
            'promedio']

        # Si hay valoraciones promedio, agregar la categoría a la lista de mejores categorías
        if valoracion_promedio is not None:
            mejores_categorias.append({'nombre': categoria.nombre, 'ranking': valoracion_promedio})

    # Ordenar las categorías según su valoración promedio
    mejores_categorias.sort(key=lambda x: x['ranking'], reverse=True)

    # mejores_categorias = mejores_categorias[:5]

    resultadosCategorias = RankingCategoriaSerializer(mejores_categorias, many=True)

    return Response({'message': 'Obtenido',
                     'mejores_categorias': resultadosCategorias.data})




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def obtenerCategoriasActivasNoActivasAdmin(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)

        return Response(serializer.data)
