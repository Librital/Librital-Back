# Generated by Django 5.0.3 on 2024-03-29 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoria', '0001_initial'),
        ('libro', '0001_initial'),
        ('libro_categoria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='libro_categorias',
            field=models.ManyToManyField(through='libro_categoria.libro_Categoria', to='categoria.categoria'),
        ),
    ]