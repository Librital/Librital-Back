from datetime import datetime, timedelta
from enum import auto

from django.db import models

from ..libro.models import Libro


# Create your models here.
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # default=datetime.now()
    updated_at = models.DateTimeField(auto_now=True)
    tipo = models.IntegerField()
    subscripcion = models.BooleanField(default=False)
    es_activo = models.BooleanField(default=True)
    img = models.CharField(max_length=255, null=True)

    objects = models.Manager()

    libros_usuario = models.ManyToManyField(Libro, through='user_libro.Libro_Usuario')

    is_anonymous = True
    is_authenticated = False
    is_active = True

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
