import datetime
from typing import Union
import json
import os
import django
from ...models import *
from .varietal import Varietal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.join('../ppai/settings.py'))
django.setup()


class Vino:
    def __init__(self, añada, fecha_actualizacion, imagen_etiqueta, nombre,
                 nota_cata_bodega, precio_ars, bodega=None, tipo_uva=None,
                 maridaje=None, varietal=None):
        self.añada = añada
        self.fecha_actualizacion = fecha_actualizacion
        self.imagen_etiqueta = imagen_etiqueta
        self.nombre = nombre
        self.nota_cata_bodega = nota_cata_bodega
        self.precio_ars = precio_ars
        self.bodega = bodega
        self.tipo_uva = tipo_uva
        self.maridaje = maridaje
        self.varietal = varietal

    def new(self, tipo_uva, maridaje, bodega):
        # creamos varietal enviandole por parametro el tipo de uva
        varietal_db = self.crear_varietal(tipo_uva)
        vino_result = VinoModel.objects.get_or_create(
            aniada=self.añada,
            fecha_actualizacion=datetime.datetime.strptime(self.fecha_actualizacion, "%d-%m-%Y").date(),
            imagen_etiqueta=self.imagen_etiqueta,
            nombre=self.nombre,
            nota_cata_bodega=self.nota_cata_bodega,
            precio_ars=self.precio_ars,
            bodega=bodega,
            maridaje=maridaje,
            varietal=varietal_db[0],
        )
        return vino_result[0].id

    def crear_varietal(self, tipo_uva):
        varietal_obj = Varietal(
            tipo_uva=tipo_uva,
            descripcion=self.varietal["descripcion"],
            porcentaje_composicion=self.varietal["porcentaje_composicion"]
        )
        return varietal_obj.new()

    def set_fecha_actualizacion(self, fecha):
        self.fecha_actualizacion = datetime.date.today()

    def set_imagen_etiqueta(self, imagen):
        self.imagen_etiqueta = imagen

    def set_nota_cata(self, nota_cata: str):
        self.nota_cata_bodega = nota_cata

    def set_precio(self, precio: Union[int, float]):
        self.precio_ars = precio

    def sos_este_vino(self, vino_act):
        if self.nombre == vino_act:
            return True
        return False

    def sos_vino_actualizar(self):
        ...

