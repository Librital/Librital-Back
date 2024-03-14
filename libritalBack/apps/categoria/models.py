from django.db import models


# Create your models here.
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
