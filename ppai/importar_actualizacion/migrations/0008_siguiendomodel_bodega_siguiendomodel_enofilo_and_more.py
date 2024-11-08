# Generated by Django 5.0.6 on 2024-05-29 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importar_actualizacion', '0007_vinomodel_maridaje_vinomodel_varietal'),
    ]

    operations = [
        migrations.AddField(
            model_name='siguiendomodel',
            name='bodega',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='importar_actualizacion.bodegamodel'),
        ),
        migrations.AddField(
            model_name='siguiendomodel',
            name='enofilo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='importar_actualizacion.enofilomodel'),
        ),
        migrations.AlterField(
            model_name='siguiendomodel',
            name='fecha_fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='varietalmodel',
            name='porcentaje_composicion',
            field=models.CharField(max_length=255),
        ),
    ]
