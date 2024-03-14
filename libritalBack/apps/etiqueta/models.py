from django.db import models

# Create your models here.
class Etiqueta(models.Model):
    id = models.AutoField(primary_key=True)
    id_libro = models.ForeignKey('libro.Libro', on_delete=models.CASCADE, db_column='id_libro')
    id_usuario = models.ForeignKey('user.Usuario', on_delete=models.CASCADE, db_column='id_usuario')
    nombre = models.CharField(max_length=50)

    objects = models.Manager()
