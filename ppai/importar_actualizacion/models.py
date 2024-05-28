from django.db import models


# Create your models here.

class BodegaModel(models.Model):
    coordenadas_ubicacion = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    fecha_ultima_actualizacion = models.DateField(max_length=255)
    historia = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    periodo_actualizacion = models.CharField(max_length=255)


class VinoModel(models.Model):
    aniada = models.CharField(max_length=255)
    fecha_actualizacion = models.DateField(max_length=255)
    imagen_etiqueta = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    nota_cata_bodega = models.CharField(max_length=255)
    precio_ars = models.IntegerField()
    bodega = models.ForeignKey('BodegaModel', on_delete=models.CASCADE, null=True, blank=True)


class EnofiloModel(models.Model):
    apellido = models.CharField(max_length=255)
    imagen_perfil = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)


class MaridajeModel(models.Model):
    descripcion = models.TextField()
    nombre = models.CharField(max_length=255)


class VarietalModel(models.Model):
    descripcion = models.TextField()
    porcentaje_composicion = models.IntegerField()


class TipoUvaModel(models.Model):
    descripcion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)


class SiguiendoModel(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()