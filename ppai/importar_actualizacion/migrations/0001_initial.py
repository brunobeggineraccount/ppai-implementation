# Generated by Django 5.0.6 on 2024-05-27 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordenadas_ubicacion', models.CharField(max_length=255)),
                ('descripcion', models.CharField(max_length=255)),
                ('fecha_ultima_actualizacion', models.CharField(max_length=255)),
                ('historia', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('periodo_actualizacion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Enofilo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellido', models.CharField(max_length=255)),
                ('imagen_perfil', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Maridaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Siguiendo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoUva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Varietal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('porcentaje_composicion', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aniada', models.CharField(max_length=255)),
                ('fecha_actualizacion', models.CharField(max_length=255)),
                ('imagen_etiqueta', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('nota_cata_bodega', models.CharField(max_length=255)),
                ('precio_ars', models.IntegerField()),
            ],
        ),
    ]