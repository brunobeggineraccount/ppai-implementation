# Generated by Django 5.0.6 on 2024-05-27 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importar_actualizacion', '0002_alter_vino_fecha_actualizacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodega',
            name='fecha_ultima_actualizacion',
            field=models.DateField(max_length=255),
        ),
    ]
