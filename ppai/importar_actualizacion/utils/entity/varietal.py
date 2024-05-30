import datetime
from typing import Union
import json
import os
import django
from ...models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.join('../ppai/settings.py'))
django.setup()

class Varietal:
    def __init__(self, descripcion=None, porcentaje_composicion=None, tipo_uva=None):
        self.descripcion = descripcion
        self.porcentaje_composicion = porcentaje_composicion
        self.tipo_uva = tipo_uva

    def new(self):
        # guardamos el varietal creado en la base de datos
        varietal = VarietalModel.objects.get_or_create(
            descripcion=self.descripcion,
            porcentaje_composicion=self.porcentaje_composicion,
            tipo_uva=self.tipo_uva
        )
        return varietal

