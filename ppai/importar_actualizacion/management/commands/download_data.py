import json
from ...models import *
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Command(BaseCommand):
    help = 'Save data to database sqlite'

    def handle(self, *args, **options):
        with open(os.path.join(BASE_DIR, 'vinosv2.json'), 'r') as f:
            json_data_base = json.load(f)

            for key, vino in json_data_base["vinos"].items():
                vino_model = VinoModel.objects.get_or_create(
                    aniada=vino["aniada"],
                    fecha_actualizacion=vino["fechaActualizacion"],
                    imagen_etiqueta=vino["imagenEtiqueta"],
                    nombre=vino["nombre"],
                    nota_cata_bodega=vino["notaDeCataBodega"],
                    precio_ars=vino["precioARS"]
                )

            for key, bodega in json_data_base["bodegas"].items():
                bodega_model = BodegaModel.objects.get_or_create(
                    coordenadas_ubicacion=bodega["coordenadasUbicacion"],
                    descripcion=bodega["descripcion"],
                    fecha_ultima_actualizacion=bodega["fechaUltimaActualizacion"],
                    historia=bodega["historia"],
                    nombre=bodega["nombre"],
                    periodo_actualizacion=bodega["periodoActualizacion"]
                )

            for key, maridaje in json_data_base["maridaje"].items():
                maridaje_model = MaridajeModel.objects.get_or_create(
                    descripcion=maridaje["descripcion"],
                    nombre=maridaje["nombre"],
                )

            for key, varietal in json_data_base["varietales"].items():
                varietal_model = VarietalModel.objects.get_or_create(
                    porcentaje_composicion=varietal["porcentajeComposicion"],
                    descripcion=varietal["descripcion"],
                )
            for key, tipo_uva in json_data_base["tipoUvas"].items():
                tipo_uva_model = TipoUvaModel.objects.get_or_create(
                    descripcion=tipo_uva["descripcion"],
                    nombre=tipo_uva["nombre"],
                )
