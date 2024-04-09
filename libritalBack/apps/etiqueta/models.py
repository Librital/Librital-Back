from django.db import models

from ..libro.models import Libro
from ..user.models import Usuario


# Create your models here.
class Etiqueta(models.Model):
    id = models.AutoField(primary_key=True)
    id_libro = models.ForeignKey(Libro, on_delete=models.CASCADE, db_column='id_libro')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    nombre = models.CharField(max_length=50)

    objects = models.Manager()
