# Generated by Django 5.0.3 on 2024-04-18 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libro', '0005_alter_libro_isbn10_alter_libro_isbn13'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='editorial',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]