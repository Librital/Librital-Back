# Generated by Django 5.0.3 on 2024-03-14 23:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoria', '0001_initial'),
        ('libro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='libro_Categoria',
            fields=[
                ('id_libro_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('activo', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id_categoria', models.ForeignKey(db_column='id_categoria', on_delete=django.db.models.deletion.CASCADE, to='categoria.categoria')),
                ('id_libro', models.ForeignKey(db_column='id_libro', on_delete=django.db.models.deletion.CASCADE, to='libro.libro')),
            ],
        ),
    ]
