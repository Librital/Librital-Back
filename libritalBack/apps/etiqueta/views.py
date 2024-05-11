from django.shortcuts import render
from rest_framework.decorators import api_view

from rest_framework.response import Response

from .models import Etiqueta
from ..libro.models import Libro


# Create your views here.

@api_view(['POST'])
def addEtiquetaUserLibro(request):

    if request.method == 'POST':
        data = request.data

        etiquetaUser = data['etiqueta']

        etiqueta = Etiqueta.objects.filter(nombre=etiquetaUser['nombre'], id_libro=etiquetaUser['id_libro'], id_usuario=etiquetaUser['id_usuario']).first()

        if etiqueta is None:

            etiqueta = Etiqueta.objects.create(nombre=etiquetaUser['nombre'], id_libro_id=etiquetaUser['id_libro'], id_usuario_id=etiquetaUser['id_usuario'])
            etiqueta.save()

            etiquetas = Etiqueta.objects.filter(id_libro=etiquetaUser['id_libro'], id_usuario=etiquetaUser['id_usuario']).values('nombre').all()

            return Response({'message': 'Guardado',
                             'etiquetas': etiquetas})
        else:
            return Response({'message': 'Ya existe'})



@api_view(['POST'])
def obtenerEtiquetasCustomUserLibro(request):
    if request.method == 'POST':

        data = request.data

        id_user = data['id_user']
        id_libro = data['id_libro']

        etiquetas = Etiqueta.objects.filter(id_libro_id=id_libro, id_usuario=id_user).values('nombre').all()

        if len(etiquetas) > 0:

            return Response({'message': 'Obtenido',
                             'etiquetas': etiquetas})
        else:
            return Response({'message': 'No etiquetas'})


@api_view(['POST'])
def removeEtiquetaCustomUserLibro(request):

    if request.method == 'POST':
        data = request.data

        etiquetaUser = data['etiqueta']

        etiqueta = Etiqueta.objects.filter(nombre=etiquetaUser['nombre'], id_libro=etiquetaUser['id_libro'], id_usuario=etiquetaUser['id_usuario']).first()

        if etiqueta is not None:
            etiqueta.delete()

            etiquetas = Etiqueta.objects.filter(id_libro=etiquetaUser['id_libro'], id_usuario=etiquetaUser['id_usuario']).values('nombre').all()

            return Response({'message': 'Eliminado',
                             'etiquetas': etiquetas})
        else:
            return Response({'message': 'Error'})



@api_view(['GET'])
def obtenerTodasEtiquetasCustomUser(request, id_user):

    if request.method == 'GET':

        librosEtiquetasUser = Etiqueta.objects.filter(id_usuario=id_user).values('id_libro').all()

        if librosEtiquetasUser is not None:

            librosActivos = Libro.objects.filter(id_libro__in=librosEtiquetasUser, es_activo=1).all()

            etiquetasUser = Etiqueta.objects.filter(id_usuario=id_user, id_libro__in=librosActivos).values('nombre').all()

            etiquetasUnicas = etiquetasUser.distinct()

            return Response({'message': 'Etiquetas cargadas',
                             'etiquetas': etiquetasUnicas})
        else:
            return Response({'message': 'No hay etiquetas'})