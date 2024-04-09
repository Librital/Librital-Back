from django.db import models

from ..libro.models import Libro
from ..user.models import Usuario


# Create your models here.
class libro_Usuario(models.Model):
    id_libro_Usuario = models.AutoField(primary_key=True)
    id_libro = models.ForeignKey(Libro, models.DO_NOTHING, db_column='id_libro')
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    activo = models.BooleanField()
    es_favorito = models.BooleanField()
    actualmente_leyendo = models.BooleanField()
    es_leer_mas_tarde = models.BooleanField()
    es_leido = models.BooleanField()
    calificacion = models.FloatField(default=0)

    objects = models.Manager()
