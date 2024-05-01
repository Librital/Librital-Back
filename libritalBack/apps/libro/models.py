from django.db import models
from django.conf.global_settings import MEDIA_ROOT

from ..categoria.models import Categoria

# Create your models here.
class Libro(models.Model):
    id_libro = models.AutoField(primary_key=True)
    titulo = models.TextField(null=False, blank=False)
    autor = models.CharField(max_length=100)
    editorial = models.TextField(null=True, blank=True)
    fecha = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    portada = models.ImageField(upload_to=MEDIA_ROOT, null=True, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    isbn10 = models.CharField(max_length=10, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    es_activo = models.BooleanField(default=True)

    objects = models.Manager()

    libro_categorias = models.ManyToManyField(Categoria, through='libro_categoria.Libro_Categoria')


