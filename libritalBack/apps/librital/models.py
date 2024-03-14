from django.db import models


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    appellido1 = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    es_activo = models.BooleanField(default=True)
    es_admin = models.BooleanField(default=False)
    es_staff = models.BooleanField(default=False)

