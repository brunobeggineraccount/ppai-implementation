import datetime
from typing import Union
import json
import os
import django
from ...models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.join('../ppai/settings.py'))
django.setup()



class Bodega:
    def __init__(self, coordenadas_ubicacion, descripcion, fecha_ultima_actualizacion, historia, nombre,
                 periodo_actualizacion, vinos=None):
        self.coordenadas_ubicacion = coordenadas_ubicacion
        self.descripcion = descripcion
        self.fecha_ultima_actualizacion = fecha_ultima_actualizacion
        self.historia = historia
        self.nombre = nombre
        self.periodo_actualizacion: int = periodo_actualizacion
        self.vinos = vinos

    def tenes_este_vino(self, vino_actualizacion: list):
        for mi_vino in self.vinos:
            if mi_vino.sos_este_vino(vino_actualizacion.nombre):
                return True
        return False

    def esta_para_actualizar_novedades_vino(self, fecha):
        diferencia_dias = (fecha - self.fecha_ultima_actualizacion).days
        if diferencia_dias > int(self.periodo_actualizacion):
            return True

    def actualizar_datos_vino(self, datos_vino_act):
        for vino in self.vinos:
            if vino.nombre == datos_vino_act.nombre:
                # seteamos los atributos con los respectivos metodos del objeto vino
                vino.set_precio(datos_vino_act.precio_ars)
                vino.set_nota_cata(datos_vino_act.nota_cata_bodega)
                vino.set_imagen_etiqueta(datos_vino_act.imagen_etiqueta)
                vino.set_fecha_actualizacion(datos_vino_act.fecha_actualizacion)

                # obtenemos el vino de la base de datos filtrandolo por nombre y bodega para asi guardar
                # efectivamente los datos
                bodega_db = BodegaModel.objects.get(nombre=self.nombre)
                vino_db = VinoModel.objects.get(nombre=vino.nombre, bodega=bodega_db)
                vino_db.precio_ars = vino.precio_ars
                vino_db.nota_cata_bodega = vino.nota_cata_bodega
                vino_db.imagen_etiqueta = vino.imagen_etiqueta
                vino_db.fecha_actualizacion = vino.fecha_actualizacion
                vino_db.save()
                return vino_db.id

    def get_nombre(self):
        return self.nombre

    def set_fecha_ultima_actualizacion(self):
        self.fecha_ultima_actualizacion = datetime.date.today()
        bodega_db = BodegaModel.objects.get(
            nombre=self.nombre
        )
        bodega_db.fecha_ultima_actualizacion = self.fecha_ultima_actualizacion
        bodega_db.save()

    def __str__(self):
        return 'Bodega: ' + self.nombre

