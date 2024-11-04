import datetime
from typing import Union, List
import json
import os
import django
from ..entity.bodega import Bodega
from ..entity.enofilo import Enofilo
from ..entity.maridaje import Maridaje
from ..entity.tipo_uva import TipoUva
from ..entity.vino import Vino
from ..interfaces.ISujetoNotificacion import ISujetoNotificacion
from ..interfaces.IObservadorNotificaciones import IObservadorNotificaciones
from ...models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.join('../ppai/settings.py'))
django.setup()


class GestorImportadorBodega(ISujetoNotificacion):
    def __init__(self, bodega_elegida=None, bodegas=None, enofilos_seguidores_bodega=None,
                 informacion_vinos_importada=None, maridajes=None, tipos_uva=None):
        super().__init__()
        if bodegas is None:
            bodegas = []
        self.bodega_elegida = bodega_elegida
        self.periodo_actualizacion = None
        self.bodegas = bodegas
        self.enofilos_seguidores_bodega = enofilos_seguidores_bodega
        self.informacion_vinos_importada: List[str] = informacion_vinos_importada
        self.maridajes = maridajes
        self.tipos_uva = tipos_uva

    def notificar(self):
        for obs in self.observadores:
            obs.actualizar(
                nombreBodega=self.bodega_elegida,
                infoVinosImportados=self.informacion_vinos_importada,
                periodoActualizacion=self.periodo_actualizacion
            )

    def suscribir(self, observador: List[IObservadorNotificaciones]):
        if observador:
            for obs in observador:
                self.observadores.append(obs)

    def quitar(self, observador: List[IObservadorNotificaciones]):
        for obs in observador:
            self.observadores.remove(obs)

    def buscar_bodegas_actualizar(self):
        self.bodegas = []
        # obtenemos todas las bodegas mediante orm django
        bodegas_query = BodegaModel.objects.all()
        # instanciamos objetos bodega con datos de la base de datos
        for bodega in bodegas_query:
            bodega = Bodega(
                coordenadas_ubicacion=bodega.coordenadas_ubicacion,
                descripcion=bodega.descripcion,
                fecha_ultima_actualizacion=bodega.fecha_ultima_actualizacion,
                historia=bodega.historia,
                nombre=bodega.nombre,
                periodo_actualizacion=bodega.periodo_actualizacion,
            )
            # agregamos a la lista de bodegas del gestor cada uno de los objetos bodega
            self.bodegas.append(bodega)

        bodegas_actualizar = []
        fecha_actual = self.obtener_fecha_actual()
        for bodega in self.bodegas:
            if bodega.esta_para_actualizar_novedades_vino(fecha_actual):
                bodegas_actualizar.append(bodega.get_nombre())
        return bodegas_actualizar

    def tomar_seleccion_bodega(self, bodega_elegida):
        bodega_elegida_db = BodegaModel.objects.get(nombre=bodega_elegida)
        self.bodega_elegida = Bodega(
            coordenadas_ubicacion=bodega_elegida_db.coordenadas_ubicacion,
            descripcion=bodega_elegida_db.descripcion,
            fecha_ultima_actualizacion=bodega_elegida_db.fecha_ultima_actualizacion,
            historia=bodega_elegida_db.historia,
            nombre=bodega_elegida_db.nombre,
            periodo_actualizacion=bodega_elegida_db.periodo_actualizacion,
        )

    def determinar_vinos_actualizar(self):
        # obtenemos todos los vinos de la bodega, los instanciamos y los agregamos a un array de vinos el cual es
        # atributo de bodega
        bodega_elegida_db = BodegaModel.objects.get(nombre=self.bodega_elegida.nombre)
        vinos_query = VinoModel.objects.filter(bodega=bodega_elegida_db)
        self.bodega_elegida.vinos = []
        for vino in vinos_query:
            vino_obj = Vino(
                añada=vino.aniada,
                fecha_actualizacion=vino.fecha_actualizacion,
                imagen_etiqueta=vino.imagen_etiqueta,
                nombre=vino.nombre,
                nota_cata_bodega=vino.nota_cata_bodega,
                precio_ars=vino.precio_ars,
                bodega=vino.bodega.nombre
            )
            self.bodega_elegida.vinos.append(vino_obj)

        # guardamos objetos vinos con datos provenientes de api en un array(tanto para crear como para actualizar)
        vinos_sistema_bodega_obj = []
        actualizaciones_vinos_de_sistema_bodega = self.obtener_actualizacion_vinos_bodega()
        if actualizaciones_vinos_de_sistema_bodega == 400:
            return 400
        for key, value in actualizaciones_vinos_de_sistema_bodega.items():
            vino_act = Vino(
                añada=value["aniada"],
                fecha_actualizacion=value["fechaActualizacion"],
                imagen_etiqueta=value["imagenEtiqueta"],
                nombre=value["nombre"],
                nota_cata_bodega=value["notaDeCataBodega"],
                precio_ars=value["precioARS"],
            )
            try:
                vino_act.tipo_uva = value["tipoUva"]
                vino_act.maridaje = value["maridaje"]
                vino_act.varietal = value["varietal"]
            except KeyError:
                pass
            vinos_sistema_bodega_obj.append(vino_act)

        # determinamos que vinos son para actualizar y cuales son para crear y los guardamos en un diccionario
        result = {"actualizar": [], "crear": []}
        for vino in vinos_sistema_bodega_obj:
            if self.bodega_elegida.tenes_este_vino(vino):
                result["actualizar"].append(vino)
            else:
                result["crear"].append(vino)
        return result

    def actualizar_o_crear_vinos(self, vinos_clasificados: dict):
        id_vinos_creados_actualizados = {"actualizados": [], "creados": []}
        if vinos_clasificados["actualizar"]:
            for vino_actualizar in vinos_clasificados["actualizar"]:
                id_vinos_creados_actualizados["actualizados"].append(self.actualizar_caracteristicas_vino_existente(
                    vino_actualizar)
                )
        if vinos_clasificados["crear"]:
            for vino_a_crear in vinos_clasificados["crear"]:
                id_vinos_creados_actualizados["creados"].append(self.crear_vino(vino_a_crear))
        return id_vinos_creados_actualizados

    def actualizar_caracteristicas_vino_existente(self, datos_vino_act):
        return self.bodega_elegida.actualizar_datos_vino(datos_vino_act)

    def crear_vino(self, vino_a_crear):
        # buscamos y obtenemos maridaje, tipo de uva y bodega de la base de datos para guardarlos a la hora de crear
        # el vino, el cual tiene foreign key a esos modelos
        maridaje_db = self.buscar_maridaje(vino_a_crear.maridaje)
        tipo_uva_db = self.buscar_tipo_uva(vino_a_crear.tipo_uva)
        bodega_db = BodegaModel.objects.get(nombre=self.bodega_elegida.nombre)
        return vino_a_crear.new(tipo_uva_db, maridaje_db, bodega_db)

    @staticmethod
    def buscar_maridaje(maridaje_vino_a_crear):
        for maridaje in MaridajeModel.objects.all():
            maridaje_obj = Maridaje(
                nombre=maridaje.nombre,
                descripcion=maridaje.descripcion
            )
            if maridaje_obj.sos_maridaje(maridaje_vino_a_crear):
                return maridaje
        return None

    @staticmethod
    def buscar_tipo_uva(tipo_uva_vino_a_crear):
        # aprovechamos la base de datos y utilizamos una query para obtener el tipo de uva
        for tipo_uva in TipoUvaModel.objects.all():
            tipo_uva_obj = TipoUva(
                nombre=tipo_uva.nombre,
                descripcion=tipo_uva.descripcion
            )
            if tipo_uva_obj.sos_tipo_uva(tipo_uva_vino_a_crear):
                return tipo_uva
        return None

    def buscar_seguidores_bodega(self):
        enofilo_db_list = EnofiloModel.objects.all()
        self.enofilos_seguidores_bodega = []
        for enofilo_db in enofilo_db_list:
            enofilo_obj = Enofilo(
                apellido=enofilo_db.apellido,
                nombre=enofilo_db.nombre,
                imagen_perfil=enofilo_db.imagen_perfil,
                enofilo_db=enofilo_db
            )
            if enofilo_obj.seguis_a_bodega(self.bodega_elegida):
                self.enofilos_seguidores_bodega.append(enofilo_db)

    def fin_caso_uso(self):
        ...

    def get_fecha_hora_actual(self):
        ...

    def opcion_importar_actualizacion_vinos(self):
        ...

    @staticmethod
    def obtener_fecha_actual():
        return datetime.date.today()

    # api
    @staticmethod
    def obtener_actualizacion_vinos_bodega():
        return {
            "1": {
                "maridaje": "Asado",
                "tipoUva": "Bonarda",
                "aniada": 2010,
                "fechaActualizacion": "23-01-2024",
                "imagenEtiqueta": "imageTrumpeter.jpg",
                "nombre": "Chardonnay",
                "notaDeCataBodega": "Presenta un color rojo profundo con matices violáceos. La claridad y brillo \
                    del vino destacan en la copa, indicando su juventud y frescura.",
                "precioARS": 1101010,
                "varietal": {
                    "descripcion": "Descripcion varietal",
                    "porcentaje_composicion": "73%"
                }
            },
            "2": {
                "maridaje": "Queso",
                "tipoUva": "Malbec",
                "aniada": 2010,
                "fechaActualizacion": "23-01-2024",
                "imagenEtiqueta": "imageTrumpeter.jpg",
                "nombre": "Trumpeter",
                "notaDeCataBodega": "Presenta un color rojo profundo con matices violáceos. La claridad y brillo \
                    del vino destacan en la copa, indicando su juventud y frescura.",
                "precioARS": 1010,
                "varietal": {
                    "descripcion": "malbec",
                    "porcentaje_composicion": "73%"
                }
            },
            "3": {
                "maridaje": "Carnes Rojas",
                "tipoUva": "Malbec",
                "aniada": 2012,
                "fechaActualizacion": "15-02-2024",
                "imagenEtiqueta": "imageCatena.jpg",
                "nombre": "Catena zapata",
                "notaDeCataBodega": "Se presenta con un intenso color púrpura y aromas de frutas rojas maduras,\
                 como cerezas y ciruelas, acompañados por sutiles notas de vainilla y especias.",
                "precioARS": 2000,
                "varietal": {
                    "descripcion": "malbec",
                    "porcentaje_composicion": "85%"
                }
            }
        }
# return 400
