import datetime
from typing import Union
import json
import os
import django
from ...models import *
from .siguiendo import Siguiendo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.join('../ppai/settings.py'))
django.setup()


class Enofilo:
    def __init__(self, apellido, imagen_perfil, nombre, enofilo_db=None):
        self.apellido = apellido
        self.imagen_perfil = imagen_perfil
        self.nombre = nombre
        self.enofilo_db = enofilo_db

    def get_nombre_usuario(self):
        ...

    def seguis_a_bodega(self, bodega_elegida):
        siguiendos_db_list = SiguiendoModel.objects.filter(enofilo=self.enofilo_db)
        for siguiendo_db in siguiendos_db_list:
            siguiendo_obj = Siguiendo(
                fecha_inicio=siguiendo_db.fecha_inicio,
                fecha_fin=siguiendo_db.fecha_fin,
                bodega=siguiendo_db.bodega
            )
            if siguiendo_obj.sos_de_bodega(bodega_elegida):
                return True
        return False

