# Generated by Django 5.0.3 on 2024-03-14 23:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('libro', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_publicacion', models.DateField()),
                ('activo', models.BooleanField(default=True)),
                ('id_libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libro.libro')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.usuario')),
            ],
        ),
    ]
