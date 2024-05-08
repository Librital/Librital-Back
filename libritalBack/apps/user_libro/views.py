from django.db.models import Sum, Count, Avg
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import libro_Usuario
from ..libro.models import Libro
from ..libro.serailizers import LibroSerializer
from ..user.models import Usuario


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

            media = round(sum([x['calificacion'] for x in userlibroValoracion]) / len(userlibroValoracion), 0)
            tamanio = len(userlibroValoracion)

            if media == 0:
                return Response({'message': 'Sin valoracion'})

            else:
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
            userLibroValoracion.calificacion = 0
            userLibroValoracion.save()
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






@api_view(['POST'])
def obtenerEtiquetasDefaultUserLibro(request):

    if request.method == 'POST':

        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']

        etiquetas = libro_Usuario.objects.filter(id_libro=id_libro, id_usuario=id_user).values('es_favorito', 'actualmente_leyendo', 'es_leer_mas_tarde', 'es_leido', 'en_biblioteca').first()

        if etiquetas is not None:
            return Response({'message': 'Obtenido',
                             'etiquetas': etiquetas})
        else:
            return Response({'message': 'No etiquetas'})


@api_view(['POST'])
def addFavoritoLibroUser(request):

    if request.method == 'POST':
        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']

        userLibro = libro_Usuario.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

        if userLibro is not None:
            userLibro.es_favorito = not userLibro.es_favorito
            userLibro.save()

            return Response({'message': 'Guardado',
                             'es_favorito': userLibro.es_favorito})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True, es_favorito=True, actualmente_leyendo=False, es_leer_mas_tarde=False, es_leido=False, calificacion=0)
            userLibro.save()
            return Response({'message': 'Guardado',
                                'es_favorito': userLibro.es_favorito})


@api_view(['POST'])
def addReadLaterUserLibro(request):

    if request.method == 'POST':
        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']

        userLibro = libro_Usuario.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

        if userLibro is not None:
            userLibro.es_leer_mas_tarde = not userLibro.es_leer_mas_tarde
            userLibro.save()

            return Response({'message': 'Guardado',
                             'es_leer_mas_tarde': userLibro.es_leer_mas_tarde})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True, es_favorito=False, actualmente_leyendo=False, es_leer_mas_tarde=True, es_leido=False, calificacion=0)
            userLibro.save()
            return Response({'message': 'Guardado',
                                'es_leer_mas_tarde': userLibro.es_leer_mas_tarde})

@api_view(['POST'])
def addTerminadoLeerUserLibro(request):

    if request.method == 'POST':
        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']

        userLibro = libro_Usuario.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

        if userLibro is not None:
            userLibro.es_leido = not userLibro.es_leido
            userLibro.save()

            return Response({'message': 'Guardado',
                             'es_leido': userLibro.es_leido})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True, es_favorito=False, actualmente_leyendo=False, es_leer_mas_tarde=False, es_leido=True, calificacion=0)
            userLibro.save()
            return Response({'message': 'Guardado',
                                'es_leido': userLibro.es_leido})

@api_view(['POST'])
def addActualmenteLeyendoUserLibro(request):

    if request.method == 'POST':
        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']

        userLibro = libro_Usuario.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

        if userLibro is not None:
            userLibro.actualmente_leyendo = not userLibro.actualmente_leyendo
            userLibro.save()

            return Response({'message': 'Guardado',
                             'actualmente_leyendo': userLibro.actualmente_leyendo})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True, es_favorito=False, actualmente_leyendo=True, es_leer_mas_tarde=False, es_leido=False, calificacion=0)
            userLibro.save()
            return Response({'message': 'Guardado',
                                'actualmente_leyendo': userLibro.actualmente_leyendo})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def addBibliotecaUserLibro(request):

    if request.method == 'POST':
        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']

        userLibro = libro_Usuario.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

        if userLibro is not None:
            userLibro.en_biblioteca = not userLibro.en_biblioteca
            userLibro.save()

            return Response({'message': 'Guardado',
                             'en_biblioteca': userLibro.en_biblioteca})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True, es_favorito=False, actualmente_leyendo=False, es_leer_mas_tarde=False, es_leido=False, calificacion=0, en_biblioteca=True)
            userLibro.save()
            return Response({'message': 'Guardado',
                                'en_biblioteca': userLibro.en_biblioteca})





