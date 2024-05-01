from django.conf.global_settings import MEDIA_ROOT
from django.db import models


# Create your models here.
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    sub_categoria = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    es_activo = models.BooleanField(default=True)
    img = models.ImageField(upload_to=MEDIA_ROOT, null=True, blank=True)

    objects = models.Manager()
