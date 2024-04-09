from django.conf.global_settings import MEDIA_ROOT
from django.db import models

from ..libro.models import Libro
from ..user.models import Usuario


# Create your models here.
class Anuncio(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    activo = models.BooleanField(default=True)

    objects = models.Manager()
