from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from rest_framework import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .backends import AuthenticateBackend
from .models import Usuario

from django.utils.timezone import localtime

from .serializers import UsuarioSerializer



# Create your views here.

@api_view(['POST'])
def registrarUsuario(request):
    if request.method == 'POST':
        data = request.data
        contrasenia = make_password(data['password'], hasher='default')
        usuario_existente = Usuario.objects.filter(email=data['email']).exists()
        if usuario_existente:
            return Response({'message': 'Existente'})
        else:
            usuarioNuevo = Usuario.objects.create(
                nombre=data['nombre'],
                apellido=data['apellido'],
                email=data['email'],
                password=contrasenia,
                fecha_nacimiento=data['fecha_nacimiento'],
                tipo=data['tipo'],
                subscripcion=data['subscripcion'],
                es_activo=data['es_activo'],
                img=data.get('img')
            )
            return Response({'message': 'Creado'})


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def actualizarInfoUsuario(request):

    if request.method == 'PUT':
        data = request.data

        usuario = Usuario.objects.filter(email=data['usuario']['email']).first()
        usuarioInicial = Usuario.objects.filter(email=data['emailInicial']).first()

        if usuario == usuarioInicial:
            if check_password(data['usuario']['password'], usuario.password):
                usuario.nombre = data['usuario']['nombre']
                usuario.apellido = data['usuario']['apellido']
                usuario.email = data['usuario']['email']
                usuario.fecha_nacimiento = data['usuario']['fecha_nacimiento']
                # usuario.tipo = data['usuario']['tipo']
                # usuario.subscripcion = data['usuario']['subscripcion']
                # usuario.es_activo = data['usuario']['es_activo']
                # usuario.img = data.get('usuario').get('img')
                usuario.save()

                refresh = RefreshToken.for_user(usuario)
                refresh["usuario"] = UsuarioSerializer(usuario).data

                return Response({
                    'message': 'Actualizado',
                    'refresh': str(refresh),
                    'access_token': str(refresh.access_token),
                })
            else:
                return Response({'message': 'Contraseña incorrecta'})

        else:
            if usuario is not None:
                return Response({'message': 'Correo ya existe'})
            else:
                print("correo nuevo no existe")
                if check_password(data['usuario']['password'], usuarioInicial.password):
                    usuarioInicial.nombre = data['usuario']['nombre']
                    usuarioInicial.apellido = data['usuario']['apellido']
                    usuarioInicial.email = data['usuario']['email']
                    usuarioInicial.fecha_nacimiento = data['usuario']['fecha_nacimiento']
                    # usuarioInicial.tipo = data['usuario']['tipo']
                    # usuarioInicial.subscripcion = data['usuario']['subscripcion']
                    # usuarioInicial.es_activo = data['usuario']['es_activo']
                    # usuarioInicial.img = data.get('usuario').get('img')
                    usuarioInicial.save()

                    refresh = RefreshToken.for_user(usuarioInicial)
                    refresh["usuario"] = UsuarioSerializer(usuarioInicial).data

                    return Response({
                        'message': 'Actualizado',
                        'refresh': str(refresh),
                        'access_token': str(refresh.access_token),
                    })

                else:
                    return Response({'message': 'Contraseña incorrecta'})


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def cambiarPasswordUsuario(request):
    if request.method == 'PUT':
        data = request.data

        usuario = Usuario.objects.filter(email=data['usuario']['email']).first()

        if check_password(data['passwordInicial'], usuario.password):
            usuario.password = make_password(data['usuario']['password'], hasher='default')
            usuario.save()

            refresh = RefreshToken.for_user(usuario)
            refresh["usuario"] = UsuarioSerializer(usuario).data

            return Response({
                'message': 'Actualizada',
                'refresh': str(refresh),
                'access_token': str(refresh.access_token),
            })
        else:
            return Response({'message': 'Incorrecta'})


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def cambiarImagenPerfil(request):
    if request.method == 'PUT':
        data = request.data

        usuario = Usuario.objects.filter(email=data['email']).first()

        usuario.img = data.get('img')
        usuario.save()

        refresh = RefreshToken.for_user(usuario)
        refresh["usuario"] = UsuarioSerializer(usuario).data

        return Response({
            'message': 'Actualizada',
            'refresh': str(refresh),
            'access_token': str(refresh.access_token),
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def obtenerJWT_Token(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']

        backend = AuthenticateBackend()
        usuario = backend.authenticate(request, email=email, password=password)

        if usuario is not None:
            refresh = RefreshToken.for_user(usuario)
            refresh["usuario"] = UsuarioSerializer(usuario).data

            return Response({
                'message': 'Correcto',
                'refresh': str(refresh),
                'access_token': str(refresh.access_token),
            })
        else:
            return Response({'message': 'Credenciales incorrectas'})
