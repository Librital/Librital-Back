from django.db import models


# Create your models here.

class libro_Categoria(models.Model):
    id_libro_categoria = models.AutoField(primary_key=True)
    id_libro = models.ForeignKey('libro.Libro', on_delete=models.CASCADE, db_column='id_libro')
    id_categoria = models.ForeignKey('categoria.Categoria', on_delete=models.CASCADE, db_column='id_categoria')
    activo = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
