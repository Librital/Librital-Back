from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Mapa
from .serializers import MapaSerializer
from ..user.models import Usuario


# Create your views here.

@api_view(['GET'])
def obtenerTodosMarkerMapa(request):

    if request.method == 'GET':

        puntosMapa = Mapa.objects.filter(activo=True).all()

        puntosMapaResultado = MapaSerializer(puntosMapa, many=True)

        if len(puntosMapa) == 0:
            return Response({'message': 'No hay puntos en el mapa'})

        return Response({'message': 'Obtenidos',
                         'puntosMapa': puntosMapaResultado.data})




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def addMarcadorMapaUser(request):

    if request.method == 'POST':

        data = request.data

        mapa = data['punto']

        marcadorExiste = Mapa.objects.filter(latitud=mapa['latitud'], longitud=mapa['longitud']).first()

        if marcadorExiste is not None:
            return Response({'message': 'Ya existe'})
        else:

            usuario = Usuario.objects.filter(id=mapa['id_usuario']).first()

            marcadorUser = Mapa.objects.create(
                titulo=mapa['titulo'],
                descripcion=mapa['descripcion'],
                id_usuario=usuario,
                latitud=mapa['latitud'],
                longitud=mapa['longitud'],
                activo=True
            )
            marcadorUser.save()

        return Response({'message': 'Correcto'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def obtenerMarkerUserMapa(request):

    if request.method == 'POST':

        data = request.data

        id_user = data['id_user']

        marcadoresUser = Mapa.objects.filter(id_usuario=id_user).all()

        marcadoresResultado = MapaSerializer(marcadoresUser, many=True)

        if len(marcadoresUser) == 0:
            return Response({'message': 'No hay marcadores'})

        return Response({'message': 'Obtenidos',
                         'marcadores': marcadoresResultado.data})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def desactivarPuntoMapaUser(request):

    if request.method == 'POST':

        data = request.data

        id_punto = data['id_marker']
        estado_punto = data['estado']

        punto = Mapa.objects.filter(id_marker=id_punto).first()

        punto.activo=estado_punto
        punto.save()

        return Response({'message': 'Correcto'})



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def obtenerTodosMarkerMapaAdmin(request):

    if request.method == 'GET':

        puntosMapa = Mapa.objects.all()

        puntosMapaResultado = MapaSerializer(puntosMapa, many=True)

        if len(puntosMapa) == 0:
            return Response({'message': 'No hay puntos en el mapa'})

        return Response({'message': 'Obtenidos',
                        'puntosMapa': puntosMapaResultado.data})



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def buscarMarcadorLatitudLongitud(request):

    if request.method == 'POST':

        data = request.data

        latitud = data['latitud']
        longitud = data['longitud']

        marcador = Mapa.objects.filter(latitud=latitud, longitud=longitud).first()

        if marcador is None:
            return Response({'message': 'No existe el marcador'})
        else:

            marcadorResultado = MapaSerializer(marcador)

            return Response({'message': 'Obtenido',
                            'marcador': marcadorResultado.data})



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def actualizarPuntoMapa(request):

    if request.method == 'POST':

        data = request.data

        id_punto = data['id_marker']
        punto = data['punto']

        puntoMapa = Mapa.objects.filter(id_marker=id_punto).first()

        puntoMapa.titulo=punto['titulo']
        puntoMapa.descripcion=punto['descripcion']
        puntoMapa.latitud=punto['latitud']
        puntoMapa.longitud=punto['longitud']
        puntoMapa.activo=punto['activo']
        puntoMapa.save()

        return Response({'message': 'Actualizado'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def eliminarPuntoMapa(request):

    if request.method == 'POST':

        data = request.data

        id_punto = data['id_marker']

        puntoMapa = Mapa.objects.filter(id_marker=id_punto).first()

        puntoMapa.delete()

        return Response({'message': 'Eliminado'})