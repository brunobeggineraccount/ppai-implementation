import datetime
from typing import Union
import json
import os
import django
from ...models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.join('../ppai/settings.py'))
django.setup()


class Maridaje:

    def __init__(self, descripcion, nombre):
        self.descripcion = descripcion
        self.nombre = nombre

    def sos_maridaje(self, maridaje_vino_a_crear):
        if self.nombre == maridaje_vino_a_crear:
            return True
        return False
