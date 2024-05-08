import pymysql
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Libro
from .models import Categoria
from ..libro_categoria.models import libro_Categoria
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
            libroIsbn = Libro.objects.filter(isbn13=isbn).first()
        elif len(isbn) == 10:
            libroIsbn = Libro.objects.filter(isbn10=isbn).first()

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
                    idCategoria = Categoria.objects.filter(nombre=genero).first().id
                    idsLibros = libro_Categoria.objects.filter(id_categoria=idCategoria).values_list('id_libro',
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
                    idCategoria = Categoria.objects.filter(nombre=genero).first().id
                    idsLibros = libro_Categoria.objects.filter(id_categoria=idCategoria).values_list('id_libro',
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

        data = request.data

        conn = pymysql.connect(host='localhost', user='root', password='963963', database='libritalbd')
        cursor = conn.cursor()

        sql_select_libro = ''
        fechaFormat = data['libro']['fecha'].split('-')
        fecha = fechaFormat[2] + '/' + fechaFormat[1] + '/' + fechaFormat[0]

        if data['libro']['isbn10'] == 'No ISBN':
            isbn = data['libro']['isbn13']

            sql_select_libro = "SELECT * FROM libro_libro WHERE isbn13 = {0}".format(isbn)

        elif data['libro']['isbn13'] == 'No ISBN':
            isbn = data['libro']['isbn10']

            sql_select_libro = "SELECT * FROM libro_libro WHERE isbn10 = {0}".format(isbn)

        cursor.execute(sql_select_libro)
        libroExiste = cursor.fetchone()

        print(data['usuario'])

        print(data['libro']['fecha'])

        if len(libroExiste) > 0:

            print("El libro ya existe en la base de datos")

            select_libro_user_existe = "SELECT * FROM user_libro_libro_usuario WHERE id_libro = {0} AND id_usuario = {1}".format(
                libroExiste[0], data['usuario']['id'])



            return Response({'message': 'Ya existe'})
        #else:

            # EL LIBRO NO EXISTE EN BD

            # libro = Libro.objects.create(
            #     titulo=data['libro']['titulo'],
            #     autor=data['libro']['autor'],
            #     editorial=data['libro']['editorial'],
            #     fecha=data['libro']['fecha'],
            #     isbn10=data['libro']['isbn10'],
            #     isbn13=data['libro']['isbn13'],
            #     descripcion=data['libro']['descripcion'],
            #     portada=data['libro']['portada'],
            #     es_activo=1
            # )
            # libro.save()
            #
            # print(libro.id_libro)
            #
            # categoria_id = Categoria.objects.filter(nombre=data['categoria']).first().id
            #
            # libroAdd = Libro.objects.filter(id_libro=libro.id_libro).first()
            #
            # libroC = Libro()
            # libroC.id_libro = libro
            #
            # categoriaL = Categoria()
            # categoriaL.id_categoria = categoria_id
            #
            # libro_categoria = libro_Categoria.objects.create(
            #     id_libro=libroC.id_libro,
            #     id_categoria=categoriaL.id_categoria,
            # )
            # print(libro_categoria)
            # # libro_categoria.save()
            #
            # print(data['usuario'])
            #
            # userLibro = libro_Usuario.objects.create(
            #     es_favortito=1,
            #     id_libro=libroC.id_libro,
            #     id_usuario=data['usuario']['id_usuario'],
            # )
            # # userLibro.save()
            #
            # print(userLibro)

        return Response({'message': 'Guardado'})
