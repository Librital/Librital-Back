from django.db.models import Sum, Count, Avg, Q
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import libro_Usuario
from ..categoria.models import Categoria
from ..etiqueta.models import Etiqueta
from ..libro.models import Libro
from ..libro.serailizers import LibroSerializer
from ..libro_categoria.models import libro_Categoria
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

            userLibroValoracion = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True,
                                                               es_favorito=False, actualmente_leyendo=False,
                                                               es_leer_mas_tarde=False, es_leido=False,
                                                               calificacion=valoracion)
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

        userLibroValoracion = libro_Usuario.objects.filter(id_usuario=id_user, id_libro=id_libro).values(
            'calificacion').first()

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

            if userLibroValoracion.es_favorito == False and userLibroValoracion.actualmente_leyendo == False and userLibroValoracion.es_leer_mas_tarde == False and userLibroValoracion.es_leido == False and userLibroValoracion.en_biblioteca == False:

                userLibroEtiquetas = Etiqueta.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

                if userLibroEtiquetas is None:
                    userLibroValoracion.activo = False
                    userLibroValoracion.save()

            return Response({'message': 'Eliminado'})
        else:
            return Response({'message': 'Error'})


@api_view(['GET'])
def obtenerMejoresLibros(request):
    if request.method == 'GET':
        librosResultados = []

        libros = libro_Usuario.objects.filter(activo=1).values('id_libro').annotate(media=Avg('calificacion')).order_by(
            '-media')[:10]

        for libro_info in libros:
            id_libro = libro_info['id_libro']
            libro = Libro.objects.filter(id_libro=id_libro, es_activo=1).values('id_libro', 'titulo', 'autor',
                                                                                'portada').first()

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

        etiquetas = libro_Usuario.objects.filter(id_libro=id_libro, id_usuario=id_user, activo=1).values('es_favorito',
                                                                                                         'actualmente_leyendo',
                                                                                                         'es_leer_mas_tarde',
                                                                                                         'es_leido',
                                                                                                         'en_biblioteca').first()

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

            if userLibro.es_favorito == False and userLibro.actualmente_leyendo == False and userLibro.es_leer_mas_tarde == False and userLibro.es_leido == False and userLibro.en_biblioteca == False and userLibro.calificacion == 0:

                userLibroEtiquetas = Etiqueta.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

                if userLibroEtiquetas is None:
                    userLibro.activo = False
                    userLibro.save()

            return Response({'message': 'Guardado',
                             'es_favorito': userLibro.es_favorito})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True,
                                                     es_favorito=True, actualmente_leyendo=False,
                                                     es_leer_mas_tarde=False, es_leido=False, calificacion=0)
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

            if userLibro.es_favorito == False and userLibro.actualmente_leyendo == False and userLibro.es_leer_mas_tarde == False and userLibro.es_leido == False and userLibro.en_biblioteca == False and userLibro.calificacion == 0:

                userLibroEtiquetas = Etiqueta.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

                if userLibroEtiquetas is None:
                    userLibro.activo = False
                    userLibro.save()


            return Response({'message': 'Guardado',
                             'es_leer_mas_tarde': userLibro.es_leer_mas_tarde})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True,
                                                     es_favorito=False, actualmente_leyendo=False,
                                                     es_leer_mas_tarde=True, es_leido=False, calificacion=0)
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

            if userLibro.es_favorito == False and userLibro.actualmente_leyendo == False and userLibro.es_leer_mas_tarde == False and userLibro.es_leido == False and userLibro.en_biblioteca == False and userLibro.calificacion == 0:

                userLibroEtiquetas = Etiqueta.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

                if userLibroEtiquetas is None:
                    userLibro.activo = False
                    userLibro.save()


            return Response({'message': 'Guardado',
                             'es_leido': userLibro.es_leido})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True,
                                                     es_favorito=False, actualmente_leyendo=False,
                                                     es_leer_mas_tarde=False, es_leido=True, calificacion=0)
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

            if userLibro.es_favorito == False and userLibro.actualmente_leyendo == False and userLibro.es_leer_mas_tarde == False and userLibro.es_leido == False and userLibro.en_biblioteca == False and userLibro.calificacion == 0:

                userLibroEtiquetas = Etiqueta.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

                if userLibroEtiquetas is None:
                    userLibro.activo = False
                    userLibro.save()


            return Response({'message': 'Guardado',
                             'actualmente_leyendo': userLibro.actualmente_leyendo})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True,
                                                     es_favorito=False, actualmente_leyendo=True,
                                                     es_leer_mas_tarde=False, es_leido=False, calificacion=0)
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

            if userLibro.es_favorito == False and userLibro.actualmente_leyendo == False and userLibro.es_leer_mas_tarde == False and userLibro.es_leido == False and userLibro.en_biblioteca == False and userLibro.calificacion == 0:

                userLibroEtiquetas = Etiqueta.objects.filter(id_usuario=id_user, id_libro=id_libro).first()

                if userLibroEtiquetas is None:
                    userLibro.activo = False
                    userLibro.save()


            return Response({'message': 'Guardado',
                             'en_biblioteca': userLibro.en_biblioteca})
        else:
            userLibro = libro_Usuario.objects.create(id_usuario_id=id_user, id_libro_id=id_libro, activo=True,
                                                     es_favorito=False, actualmente_leyendo=False,
                                                     es_leer_mas_tarde=False, es_leido=False, calificacion=0,
                                                     en_biblioteca=True)
            userLibro.save()
            return Response({'message': 'Guardado',
                             'en_biblioteca': userLibro.en_biblioteca})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def cargarTodosLibrosUsuario(request):
    if request.method == 'POST':
        data = request.data

        numMostrar = 12
        etiqueta = data['etiqueta']
        tipoEtiqueta = data['tipoEtiqueta']
        valorBuscar = data['valorBuscar']
        pagina = int(data['pagina'])
        offset = (pagina - 1) * numMostrar

        id_user = data['id_user']

        if tipoEtiqueta == 'default':

            if etiqueta == 'Todos':

                librosUsuario = libro_Usuario.objects.filter(id_usuario=id_user, activo=True).values('id_libro',
                                                                                                  'calificacion',
                                                                                                  'es_favorito',
                                                                                                  'actualmente_leyendo',
                                                                                                  'es_leer_mas_tarde',
                                                                                                  'es_leido',
                                                                                                  'en_biblioteca')

                librosConEtiquetas = Etiqueta.objects.filter(id_usuario=id_user).values('id_libro', 'nombre').all()

                if len(librosUsuario) != 0 or len(librosConEtiquetas) != 0:

                    if len(librosUsuario) != 0:
                        numLibrosTotalesDefault = Libro.objects.filter(
                            id_libro__in=[libro['id_libro'] for libro in librosUsuario], es_activo=True).values('id_libro', 'titulo',
                                                                                                'autor',
                                                                                                'portada').all()
                        # librosResultados = Libro.objects.filter(id_libro__in=[libro['id_libro'] for libro in librosUsuario]).values('id_libro', 'titulo', 'autor', 'portada')[offset:offset + numMostrar]

                    if len(librosConEtiquetas) != 0:
                        numLibrosTotalesCustom = Libro.objects.filter(
                            id_libro__in=[libro['id_libro'] for libro in librosConEtiquetas], es_activo=True).values('id_libro',
                                                                                                     'titulo', 'autor',
                                                                                                     'portada').all()

                    librosTotales = librosUsuario.values('id_libro').union(librosConEtiquetas.values('id_libro'))

                    librosTotal = Libro.objects.filter(id_libro__in=librosTotales, es_activo=True).values('id_libro', 'titulo', 'autor',
                                                                                          'portada').all()
                    librosUnicos = Libro.objects.filter(id_libro__in=librosTotales, es_activo=True).values('id_libro', 'titulo',
                                                                                           'autor', 'portada')[
                                   offset:offset + numMostrar]

                    return Response({'message': 'Obtenidos',
                                     'libros': librosUnicos,
                                     'numLibroPerPage': numMostrar,
                                     'totalLibros': len(librosTotal)})

                else:
                    print('Entra primer else')
                    return Response({'message': 'No hay libros'})

            if etiqueta == 'Favoritos':

                librosFavoritosUsuario = libro_Usuario.objects.filter(id_usuario=id_user, es_favorito=True,
                                                                      activo=1).values('id_libro', 'calificacion',
                                                                                       'es_favorito',
                                                                                       'actualmente_leyendo',
                                                                                       'es_leer_mas_tarde', 'es_leido',
                                                                                       'en_biblioteca')

                if librosFavoritosUsuario is not None:
                    numLibrosTotales = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosFavoritosUsuario]).values('id_libro',
                                                                                                     'titulo', 'autor',
                                                                                                     'portada').all()
                    librosResultados = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosFavoritosUsuario]).values('id_libro',
                                                                                                     'titulo', 'autor',
                                                                                                     'portada')[
                                       offset:offset + numMostrar]

                    return Response({'message': 'Obtenidos',
                                     'libros': librosResultados,
                                     'numLibroPerPage': numMostrar,
                                     'totalLibros': len(numLibrosTotales)})
                else:
                    return Response({'message': 'No hay libros'})

            if etiqueta == 'Actualmente leyendo':

                librosActualmenteUser = libro_Usuario.objects.filter(id_usuario=id_user, actualmente_leyendo=True,
                                                                     activo=1).values('id_libro', 'calificacion',
                                                                                      'es_favorito',
                                                                                      'actualmente_leyendo',
                                                                                      'es_leer_mas_tarde', 'es_leido',
                                                                                      'en_biblioteca')

                if librosActualmenteUser is not None:
                    numLibrosTotales = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosActualmenteUser]).values('id_libro',
                                                                                                    'titulo', 'autor',
                                                                                                    'portada').all()
                    librosResultados = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosActualmenteUser]).values('id_libro',
                                                                                                    'titulo', 'autor',
                                                                                                    'portada')[
                                       offset:offset + numMostrar]

                    return Response({'message': 'Obtenidos',
                                     'libros': librosResultados,
                                     'numLibroPerPage': numMostrar,
                                     'totalLibros': len(numLibrosTotales)})
                else:
                    return Response({'message': 'No hay libros'})

            if etiqueta == 'Pendientes':

                librosPendientesUsuario = libro_Usuario.objects.filter(id_usuario=id_user, es_leer_mas_tarde=True,
                                                                       activo=1).values('id_libro', 'calificacion',
                                                                                        'es_favorito',
                                                                                        'actualmente_leyendo',
                                                                                        'es_leer_mas_tarde', 'es_leido',
                                                                                        'en_biblioteca')

                if librosPendientesUsuario is not None:
                    numLibrosTotales = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosPendientesUsuario]).values('id_libro',
                                                                                                      'titulo', 'autor',
                                                                                                      'portada').all()
                    librosResultados = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosPendientesUsuario]).values('id_libro',
                                                                                                      'titulo', 'autor',
                                                                                                      'portada')[
                                       offset:offset + numMostrar]

                    return Response({'message': 'Obtenidos',
                                     'libros': librosResultados,
                                     'numLibroPerPage': numMostrar,
                                     'totalLibros': len(numLibrosTotales)})
                else:
                    return Response({'message': 'No hay libros'})

            if etiqueta == 'Ya leídos':

                librosLeidosUsuario = libro_Usuario.objects.filter(id_usuario=id_user, es_leido=True, activo=1).values(
                    'id_libro', 'calificacion', 'es_favorito', 'actualmente_leyendo', 'es_leer_mas_tarde', 'es_leido',
                    'en_biblioteca')

                if librosLeidosUsuario is not None:
                    numLibrosTotales = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosLeidosUsuario]).values('id_libro', 'titulo',
                                                                                                  'autor',
                                                                                                  'portada').all()
                    librosResultados = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosLeidosUsuario]).values('id_libro', 'titulo',
                                                                                                  'autor', 'portada')[
                                       offset:offset + numMostrar]

                    return Response({'message': 'Obtenidos',
                                     'libros': librosResultados,
                                     'numLibroPerPage': numMostrar,
                                     'totalLibros': len(numLibrosTotales)})
                else:
                    return Response({'message': 'No hay libros'})

            if etiqueta == 'Con valoración':

                librosValoradosUsuario = libro_Usuario.objects.filter(id_usuario=id_user, calificacion__gt=0,
                                                                      activo=1).values('id_libro', 'calificacion',
                                                                                       'es_favorito',
                                                                                       'actualmente_leyendo',
                                                                                       'es_leer_mas_tarde', 'es_leido',
                                                                                       'en_biblioteca')

                if librosValoradosUsuario is not None:
                    numLibrosTotales = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosValoradosUsuario]).values('id_libro',
                                                                                                     'titulo', 'autor',
                                                                                                     'portada').all()
                    librosResultados = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosValoradosUsuario]).values('id_libro',
                                                                                                     'titulo', 'autor',
                                                                                                     'portada')[
                                       offset:offset + numMostrar]

                    return Response({'message': 'Obtenidos',
                                     'libros': librosResultados,
                                     'numLibroPerPage': numMostrar,
                                     'totalLibros': len(numLibrosTotales)})
                else:
                    return Response({'message': 'No hay libros'})

            else:
                print('Entra segundo else')
                print(etiqueta)


        elif tipoEtiqueta == 'custom':

            etiquetaUsuario = Etiqueta.objects.filter(id_usuario=id_user, nombre=etiqueta).values('id_libro').all()

            if len(etiquetaUsuario) != 0:
                numLibrosTotales = Libro.objects.filter(id_libro__in=[libro['id_libro'] for libro in etiquetaUsuario], es_activo=1).values('id_libro', 'titulo', 'autor', 'portada').all()
                librosConEtiquetaActivos = Libro.objects.filter(id_libro__in=[libro['id_libro'] for libro in etiquetaUsuario], es_activo=1).values('id_libro', 'titulo', 'autor', 'portada')[offset:offset + numMostrar]

                return Response({'message': 'Obtenidos',
                                 'libros': librosConEtiquetaActivos,
                                 'numLibroPerPage': numMostrar,
                                 'totalLibros': len(numLibrosTotales)})

            else:
                return Response({'message': 'No hay libros'})


        elif tipoEtiqueta == 'busqueda':

            librosUsuario = libro_Usuario.objects.filter(id_usuario=id_user, activo=1).values('id_libro',
                                                                                              'calificacion',
                                                                                              'es_favorito',
                                                                                              'actualmente_leyendo',
                                                                                              'es_leer_mas_tarde',
                                                                                              'es_leido',
                                                                                              'en_biblioteca')

            librosConEtiquetas = Etiqueta.objects.filter(id_usuario=id_user).values('id_libro', 'nombre').all()

            if len(librosUsuario) != 0 or len(librosConEtiquetas) != 0:

                if len(librosUsuario) != 0:
                    numLibrosTotalesDefault = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosUsuario]).values('id_libro', 'titulo',
                                                                                            'autor',
                                                                                            'portada').all()
                    # librosResultados = Libro.objects.filter(id_libro__in=[libro['id_libro'] for libro in librosUsuario]).values('id_libro', 'titulo', 'autor', 'portada')[offset:offset + numMostrar]

                if len(librosConEtiquetas) != 0:
                    numLibrosTotalesCustom = Libro.objects.filter(
                        id_libro__in=[libro['id_libro'] for libro in librosConEtiquetas]).values('id_libro',
                                                                                                 'titulo', 'autor',
                                                                                                 'portada').all()

                librosTotales = librosUsuario.values('id_libro').union(librosConEtiquetas.values('id_libro'))

                librosUnicos = Libro.objects.filter(id_libro__in=librosTotales).values('id_libro', 'titulo',
                                                                                       'autor', 'portada')

                numLibrosBusqueda = librosUnicos.filter(titulo__icontains=valorBuscar).all()

                librosBusqueda = librosUnicos.filter(titulo__icontains=valorBuscar)[offset:offset + numMostrar]

                return Response({'message': 'Obtenidos',
                                 'libros': librosBusqueda,
                                 'numLibroPerPage': numMostrar,
                                 'totalLibros': len(numLibrosBusqueda)})

            else:
                return Response({'message': 'No hay libros'})




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def obtenerRecomendacionesCategoriaLibrosUser(request):
    if request.method == 'POST':
        data = request.data

        id_user = data.get('id_user')

        libroUserValorados = libro_Usuario.objects.filter(id_usuario=id_user, activo=True).values('id_libro',
                                                                                                     'calificacion')

        if libroUserValorados.exists():
            categorias_usuario = Categoria.objects.filter(
                libro_categoria__id_libro__in=libroUserValorados.values('id_libro')).distinct()

            # Obtener libros en las mismas categorías, ordenados por calificación promedio de otros usuarios
            libros_recomendados = Libro.objects.filter(
                libro_categoria__id_categoria__in=categorias_usuario
            ).exclude(
                libro_usuario__id_usuario=id_user
            ).annotate(
                promedio_calificacion=Avg('libro_usuario__calificacion')
            ).order_by('-promedio_calificacion')

            libros_recomendados = libros_recomendados[:15]

            libros_serializer = LibroSerializer(libros_recomendados, many=True)

            return Response({'message': 'Obtenido',
                            'libros': libros_serializer.data})

        return Response({'message': 'No hay libros valorados'})

