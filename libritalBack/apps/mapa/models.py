from django.db import models

from ..user.models import Usuario


# Create your models here.
class Mapa(models.Model):
    id_marker = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
