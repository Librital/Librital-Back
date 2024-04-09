from django.db import models


class Librital(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    objects = models.Manager()



