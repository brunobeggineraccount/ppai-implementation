import datetime
from typing import Union
import json
import os
import django
from ...models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.join('../ppai/settings.py'))
django.setup()


class Siguiendo:
    def __init__(self, fecha_inicio=None, fecha_fin=None, bodega=None, enofilo=None):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.bodega = bodega
        self.enofilo = enofilo

    def sos_de_bodega(self, bodega_elegida):
        if self.bodega.nombre == bodega_elegida:
            return True
        return False
