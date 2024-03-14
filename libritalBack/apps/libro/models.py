from django.db import models
from django.conf.global_settings import MEDIA_ROOT

# Create your models here.
class Libro(models.Model):
    id_libro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100)
    fecha = models.DateField()
    descripcion = models.TextField()
    portada = models.ImageField(upload_to=MEDIA_ROOT, null=True, blank=True)
    isbn13 = models.CharField(max_length=13)
    isbn10 = models.CharField(max_length=10)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
