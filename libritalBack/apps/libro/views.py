import json
import os

import pymysql
from django.core.files.storage import default_storage
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Libro
from .models import Categoria
from ..libro_categoria.models import libro_Categoria
from ..user.models import Usuario
from ..user_libro.models import libro_Usuario

from .serailizers import LibroSerializer


# Create your views here.

@api_view(['POST'])
def identificarISBN(request):
    global libroIsbn
    if request.method == 'POST':
        data = request.data

        isbn = data['isbn']

        if len(isbn) == 13:
            libroIsbn = Libro.objects.filter(es_activo=1, isbn13=isbn).first()
        elif len(isbn) == 10:
            libroIsbn = Libro.objects.filter(es_activo=1, isbn10=isbn).first()

        if libroIsbn is not None:

            libroIsbnResult = LibroSerializer(libroIsbn)

            return Response({'message': 'Encontrado',
                             'libro': libroIsbnResult.data})

        else:
            return Response({'message': 'No encontrado'})


@api_view(['POST'])
def obtenerLibros(request):
    if request.method == 'POST':

        data = request.data

        numMostrar = 16
        filtro = data['filtro']
        valorBuscar = data['valorBuscar']
        pagina = int(data['pagina'])
        genero = data['genero']
        offset = (pagina - 1) * numMostrar

        if filtro == 'titulo':

            try:
                librosTotales = Libro.objects.filter(es_activo=1, titulo__icontains=valorBuscar).values('id_libro',
                                                                                                        'titulo',
                                                                                                        'autor',
                                                                                                        'portada').all()
                libros = Libro.objects.filter(es_activo=1, titulo__icontains=valorBuscar).values('id_libro', 'titulo',
                                                                                                 'autor',
                                                                                                 'portada').all().order_by(
                    'titulo')[offset:offset + numMostrar]

                return Response({'message': 'Obtenido',
                                 'libros': libros,
                                 'librosPerPage': numMostrar,
                                 'total': len(librosTotales)})
            except:
                return Response({'message': 'Error'})

        if filtro == 'autor':
            try:
                librosTotales = Libro.objects.filter(es_activo=1, autor__icontains=valorBuscar).values('id_libro',
                                                                                                       'titulo',
                                                                                                       'autor',
                                                                                                       'portada').all()
                libros = Libro.objects.filter(es_activo=1, autor__icontains=valorBuscar).values('id_libro', 'titulo',
                                                                                                'autor',
                                                                                                'portada').all().order_by(
                    'autor')[offset:offset + numMostrar]

                return Response({'message': 'Obtenido',
                                 'libros': libros,
                                 'librosPerPage': numMostrar,
                                 'total': len(librosTotales)})
            except:
                return Response({'message': 'Error'})

        if filtro == 'isbn':

            if len(valorBuscar) == 13:
                try:
                    librosTotales = Libro.objects.filter(es_activo=1, isbn13=valorBuscar).values('id_libro', 'titulo',
                                                                                                 'autor',
                                                                                                 'portada').all()
                    libros = Libro.objects.filter(es_activo=1, isbn13=valorBuscar).values('id_libro', 'titulo', 'autor',
                                                                                          'portada').all().order_by(
                        'isbn13')[offset:offset + numMostrar]

                    return Response({'message': 'Obtenido',
                                     'libros': libros,
                                     'librosPerPage': numMostrar,
                                     'total': len(librosTotales)})
                except:
                    return Response({'message': 'Error'})

            elif len(valorBuscar) == 10:
                try:
                    librosTotales = Libro.objects.filter(es_activo=1, isbn10=valorBuscar).values('id_libro', 'titulo',
                                                                                                 'autor',
                                                                                                 'portada').all()
                    libros = Libro.objects.filter(es_activo=1, isbn10=valorBuscar).values('id_libro', 'titulo', 'autor',
                                                                                          'portada').all().order_by(
                        'isbn10')[offset:offset + numMostrar]

                    return Response({'message': 'Obtenido',
                                     'libros': libros,
                                     'librosPerPage': numMostrar,
                                     'total': len(librosTotales)})
                except:
                    return Response({'message': 'Error'})

        if filtro == 'categoria':

            if valorBuscar == '':
                try:
                    idCategoria = Categoria.objects.filter(es_activo=1, nombre=genero).first().id
                    idsLibros = libro_Categoria.objects.filter(activo=1, id_categoria=idCategoria).values_list('id_libro',
                                                                                                     flat=True)

                    librosTotales = Libro.objects.filter(es_activo=1, id_libro__in=idsLibros).values('id_libro',
                                                                                                     'titulo', 'autor',
                                                                                                     'portada').all()
                    libros = Libro.objects.filter(es_activo=1, id_libro__in=idsLibros).values('id_libro', 'titulo',
                                                                                              'autor',
                                                                                              'portada').all().order_by(
                        '-added_at')[offset:offset + numMostrar]

                    return Response({'message': 'Obtenido',
                                     'libros': libros,
                                     'librosPerPage': numMostrar,
                                     'total': len(librosTotales)})
                except:
                    return Response({'message': 'Error'})

            else:

                try:
                    idCategoria = Categoria.objects.filter(es_activo=1, nombre=genero).first().id
                    idsLibros = libro_Categoria.objects.filter(activo=1, id_categoria=idCategoria).values_list('id_libro',
                                                                                                     flat=True)

                    librosTotales = Libro.objects.filter(es_activo=1, id_libro__in=idsLibros).values('id_libro',
                                                                                                     'titulo', 'autor',
                                                                                                     'portada').all()
                    libros = Libro.objects.filter(es_activo=1, id_libro__in=idsLibros).values('id_libro', 'titulo',
                                                                                              'autor',
                                                                                              'portada').all().order_by(
                        '-added_at')[offset:offset + numMostrar]

                    return Response({'message': 'Obtenido',
                                     'libros': libros,
                                     'librosPerPage': numMostrar,
                                     'total': len(librosTotales)})
                except:
                    return Response({'message': 'Error'})

        else:
            try:
                librosTotales = Libro.objects.filter(es_activo=1).all()
                libros = Libro.objects.filter(es_activo=1).values('id_libro', 'titulo', 'autor',
                                                                  'portada').all().order_by('-added_at')[
                         offset:offset + numMostrar]

                return Response({'message': 'Obtenido',
                                 'libros': libros,
                                 'librosPerPage': numMostrar,
                                 'total': len(librosTotales)})
            except:
                return Response({'message': 'Error'})


@api_view(['GET'])
def obtenerLibroId(request, id):
    if request.method == 'GET':
        data = request.data

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


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def addLibroNuevoBiblioteca(request):
    if request.method == 'POST':

        libro = json.loads(request.POST.get('libro'))
        nombre_categoria = request.POST.get('categoria')
        usuario = json.loads(request.POST.get('usuario'))

        cover_file = request.FILES.get('cover')

        conn = pymysql.connect(host='localhost', user='root', password='963963', database='libritalbd')
        cursor = conn.cursor()

        sql_select_libro = ''
        fechaFormat = libro['fecha'].split('-')
        fecha = fechaFormat[2] + '/' + fechaFormat[1] + '/' + fechaFormat[0]

        if libro['isbn10'] == 'No ISBN':
            isbn = libro['isbn13']

            sql_select_libro = "SELECT * FROM libro_libro WHERE isbn13 = {0}".format(isbn)

        elif libro['isbn13'] == 'No ISBN':
            isbn = libro['isbn10']

            sql_select_libro = "SELECT * FROM libro_libro WHERE isbn10 = {0}".format(isbn)

        cursor.execute(sql_select_libro)
        libroExiste = cursor.fetchone()

        # COMPROBAR SI EL LIBRO YA EXISTE EN LA BD
        if libroExiste is not None:

            print("El libro ya existe en la base de datos")

            select_libro_user_existe = "SELECT en_biblioteca, activo FROM user_libro_libro_usuario WHERE id_libro = {0} AND id_usuario = {1}".format(
                libroExiste[0], usuario['id'])

            cursor.execute(select_libro_user_existe)
            libro_user_existe = cursor.fetchone()

            # COMPROBAR SI EL LIBRO A AGREGAR YA EXISTE EN LA BIBLIOTECA DEL USUARIO
            if libro_user_existe is not None:
                if libro_user_existe[0] == 1:
                    # EL LIBRO YA EXISTE EN LA BIBLIOTECA DEL USUARIO
                    return Response({'message': 'Ya existe en tu biblioteca'})
                else:
                    # EL LIBRO EXISTE EN LA BD RELACION LIBRO-USER POR OTRO MOTIVO
                    # PERO NO ESTA EN LA BIBLIOTECA DEL USUARIO

                    if libro_user_existe[1] == 0:
                        # EL LIBRO YA EXISTE EN LA BD RELACION LIBRO-USER PERO NO ESTA ACTIVO
                        # SE ACTIVA EL REGISTRO

                        libroAdd = Libro.objects.filter(id_libro=libroExiste[0]).first()
                        usuarioAdd = Usuario.objects.filter(id=usuario['id']).first()

                        libro_usuario = libro_Usuario.objects.filter(id_libro=libroAdd, id_usuario=usuarioAdd).first()

                        libro_usuario.activo = 1
                        libro_usuario.en_biblioteca = 1
                        libro_usuario.save()

                        return Response({'message': 'Guardado en tu biblioteca'})

                    else:

                        libroAdd = Libro.objects.filter(id_libro=libroExiste[0]).first()
                        usuarioAdd = Usuario.objects.filter(id=usuario['id']).first()

                        libro_usuario = libro_Usuario.objects.filter(id_libro=libroAdd,
                                                                     id_usuario=usuarioAdd).first()
                        libro_usuario.en_biblioteca = 1
                        libro_usuario.save()

                        return Response({'message': 'Guardado en tu biblioteca'})
            else:
                # EL LIBRO YA EXISTE PERO NO ESTA EN LA BIBLIOTECA DEL USUARIO
                # NI EN LA RELACION LIBRO-USER

                libroAdd = Libro.objects.filter(id_libro=libroExiste[0]).first()
                usuarioAdd = Usuario.objects.filter(id=usuario['id']).first()

                userLibro = libro_Usuario.objects.create(es_favorito=False, actualmente_leyendo=False, es_leer_mas_tarde=False,
                                                         es_leido=False, calificacion=0, id_libro=libroAdd, id_usuario=usuarioAdd,
                                                         activo=True, en_biblioteca=1)
                userLibro.save()

                return Response({'message': 'Guardado en tu biblioteca'})
        else:

            # EL LIBRO NO EXISTE EN BD

            print("El libro no existe en la base de datos")

            nuevoLibro = ''

            if libro['portada'].startswith('https'):
                # INSERTAR DIRECTAMENTE EN LA BD
                # EL LIBRO SE HA ENCONTRADO AL ESCANEAR LA PORTADA
                portada = libro['portada']

                if libro['isbn13'] == 'No ISBN':
                    isbn = libro['isbn10']

                    nuevoLibro = Libro.objects.create(titulo=libro['titulo'], autor=libro['autor'],
                                                      editorial=libro['editorial'],
                                                      fecha=fecha, descripcion=libro['descripcion'], portada=portada,
                                                      isbn13='No ISBN', isbn10=isbn, es_activo=True)

                elif libro['isbn10'] == 'No ISBN':
                    isbn = libro['isbn13']

                    nuevoLibro = Libro.objects.create(titulo=libro['titulo'], autor=libro['autor'],
                                                      editorial=libro['editorial'],
                                                      fecha=fecha, descripcion=libro['descripcion'], portada=portada,
                                                      isbn13=isbn, isbn10='No ISBN', es_activo=True)
                nuevoLibro.save()

                categoria_id = Categoria.objects.filter(nombre=nombre_categoria).first()
                libroAdd = Libro.objects.filter(id_libro=nuevoLibro.id_libro).first()

                libro_categoria = libro_Categoria.objects.create(id_libro=libroAdd, id_categoria=categoria_id,
                                                                 activo=True)
                libro_categoria.save()

                usuarioAdd = Usuario.objects.filter(id=usuario['id']).first()

                userLibro = libro_Usuario.objects.create(es_favorito=False, actualmente_leyendo=False,
                                                         es_leer_mas_tarde=False, es_leido=False,
                                                         calificacion=0, id_libro=libroAdd, id_usuario=usuarioAdd,
                                                         activo=True, en_biblioteca=1)

                userLibro.save()

                return Response({'message': 'Guardado'})

            else:
                # TRATAR LA IMAGEN GUARDANDO SOLO LA RELATIVA URL

                imagen = request.FILES['cover']


                nombre_archivo = default_storage.save(imagen.name, imagen)
                url_imagen = default_storage.url(nombre_archivo)


                # with default_storage.open(url_imagen, 'wb+') as destino:
                #     for parte in imagen.chunks():
                #         destino.write(parte)



                if libro['isbn13'] == 'No ISBN':
                    isbn = libro['isbn10']

                    nuevoLibro = Libro.objects.create(titulo=libro['titulo'], autor=libro['autor'],
                                                      editorial=libro['editorial'],
                                                      fecha=fecha, descripcion=libro['descripcion'], portada=url_imagen,
                                                      isbn13='No ISBN', isbn10=isbn, es_activo=True)

                elif libro['isbn10'] == 'No ISBN':
                    isbn = libro['isbn13']

                    nuevoLibro = Libro.objects.create(titulo=libro['titulo'], autor=libro['autor'],
                                                      editorial=libro['editorial'],
                                                      fecha=fecha, descripcion=libro['descripcion'], portada=url_imagen,
                                                      isbn13=isbn, isbn10='No ISBN', es_activo=True)
                nuevoLibro.save()


                categoria_id = Categoria.objects.filter(nombre=nombre_categoria).first()
                libroAdd = Libro.objects.filter(id_libro=nuevoLibro.id_libro).first()


                libro_categoria = libro_Categoria.objects.create(id_libro=libroAdd, id_categoria=categoria_id, activo=True)
                libro_categoria.save()

                usuarioAdd = Usuario.objects.filter(id=usuario['id']).first()

                userLibro = libro_Usuario.objects.create(es_favorito=False, actualmente_leyendo=False, es_leer_mas_tarde=False, es_leido=False,
                                                         calificacion=0, id_libro=libroAdd, id_usuario=usuarioAdd, activo=True, en_biblioteca=1)

                userLibro.save()

                return Response({'message': 'Guardado'})
