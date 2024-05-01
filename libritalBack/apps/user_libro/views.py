from django.db.models import Sum, Count, Avg
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import libro_Usuario
from ..libro.models import Libro
from ..libro.serailizers import LibroSerializer



# Create your views here.


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def saveUserLibro(request):

    if request.method == 'POST':
        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']
        valoracion = data['valoracion']

        userLibroValoracion = libro_Usuario.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

        if userLibroValoracion is None:
            userLibroValoracion = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True, es_favorito=False, actualmente_leyendo=False, es_leer_mas_tarde=False, es_leido=False, calificacion=valoracion)
            userLibroValoracion.save()
        else:
            userLibroValoracion.calificacion = valoracion
            userLibroValoracion.save()

        return Response({'message': 'Guardado'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def cargarInfoLibroUser(request):

    if request.method == 'POST':

        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']

        userLibroValoracion = libro_Usuario.objects.filter(id_usuario=id_user, id_libro=id_libro).values('calificacion').first()

        if userLibroValoracion is not None:
            return Response({'message': 'Obtenido',
                             'userLibro': userLibroValoracion})
        else:
            return Response({'message': 'Error'})

@api_view(['POST'])
def cargarInfoLibro(request):

    if request.method == 'POST':

        data = request.data

        id_libro = data['id_libro']

        userlibroValoracion = libro_Usuario.objects.filter(id_libro=id_libro).values('calificacion').all()

        if len(userlibroValoracion) > 0:
            media = round(sum([x['calificacion'] for x in userlibroValoracion]) / len(userlibroValoracion), 1)
            tamanio = len(userlibroValoracion)

            return Response({'message': 'Obtenido',
                             'mediaLibro': media,
                             'numResenas': tamanio})
        else:
            return Response({'message': 'Sin valoracion'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def eliminarValoracionUsuario(request):

    if request.method == 'POST':

        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']

        userLibroValoracion = libro_Usuario.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

        if userLibroValoracion is not None:
            userLibroValoracion.delete()
            return Response({'message': 'Eliminado'})
        else:
            return Response({'message': 'Error'})


@api_view(['GET'])
def obtenerMejoresLibros(request):
    if request.method == 'GET':
        librosResultados = []

        libros = libro_Usuario.objects.values('id_libro').annotate(media=Avg('calificacion')).order_by('-media')[:10]

        for libro_info in libros:
            id_libro = libro_info['id_libro']
            libro = Libro.objects.filter(id_libro=id_libro).values('id_libro', 'titulo', 'autor', 'portada').first()

            if libro is not None:
                libro['media_calificaciones'] = libro_info['media']
                librosResultados.append(libro)

        return Response({'message': 'Obtenido', 'libros': librosResultados})




