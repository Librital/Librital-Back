# Generated by Django 5.0.3 on 2024-04-22 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libro', '0008_alter_libro_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='fecha',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]