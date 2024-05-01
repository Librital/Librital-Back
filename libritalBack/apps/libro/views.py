from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Libro

from .serailizers import LibroSerializer

# Create your views here.

@api_view(['POST'])
def identificarISBN(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        return Response({'message': 'Creado',
                         'isbn': 'Ha llegado'})


@api_view(['POST'])
def obtenerLibros(request):
    if request.method == 'POST':
        data = request.data

        numMostrar = 16
        pagina = int(data['pagina'])
        offset = (pagina - 1) * numMostrar

        try:
            librosTotales = Libro.objects.filter(es_activo=1).all()
            libros = Libro.objects.filter(es_activo=1).all().order_by('-added_at')[offset:offset+numMostrar]
            librosResultados = LibroSerializer(libros, many=True)

            return Response({'message': 'Obtenido',
                             'libros': librosResultados.data,
                             'librosPerPage': numMostrar,
                             'total': len(librosTotales)})
        except:
            return Response({'message': 'Error'})


@api_view(['GET'])
def obtenerLibroId(request, id):
    if request.method == 'GET':
        data = request.data
        print(data)

        libro = get_object_or_404(Libro, id_libro=id)
        libro_serializer = LibroSerializer(libro)

        if libro is not None:
            return Response({'message': 'Obtenido',
                                'libro': libro_serializer.data})
        else:
            return Response({'message': 'Error'})


@api_view(['GET'])
def obtenerNewArrivals(request):

    if request.method == 'GET':
        data = request.data
        print(data)

        try:
            libros = Libro.objects.filter(es_activo=1).all().order_by('-added_at')[:12]
            libros2 = Libro.objects.filter(es_activo=1).all().order_by('-added_at')[12:22]
            librosResultados = LibroSerializer(libros, many=True)
            librosResultados2 = LibroSerializer(libros2, many=True)

            return Response({'message': 'Obtenido',
                             'libros': librosResultados.data,
                             'libros2': librosResultados2.data})
        except:
            return Response({'message': 'Error'})