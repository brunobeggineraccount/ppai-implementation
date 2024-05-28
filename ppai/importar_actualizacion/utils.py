import datetime
from typing import Union
import json

class GestorImportadorBodega:
    def __init__(self, bodega_elegida=None, bodegas=None, enofilos_seguidores_bodega=None,
                 informacion_vinos_importada=None, maridajes=None,
                 tipos_uva=None):
        if bodegas is None:
            bodegas = []
        self.bodega_elegida = bodega_elegida
        self.bodegas = bodegas
        self.enofilos_seguidores_bodega = enofilos_seguidores_bodega
        self.informacion_vinos_importada = informacion_vinos_importada
        self.maridajes = maridajes
        self.tipos_uva = tipos_uva

    def buscar_bodegas_actualizar(self):
        bodegas_actualizar = []
        for bodega in self.bodegas:
            if bodega.esta_para_actualizar_novedades_vino():
                bodegas_actualizar.append(bodega.nombre)
        return bodegas_actualizar

    def tomar_seleccion_bodega(self, bodega_elegida_query):
        self.bodega_elegida = Bodega(
            coordenadas_ubicacion=bodega_elegida_query.coordenadas_ubicacion,
            descripcion=bodega_elegida_query.descripcion,
            fecha_ultima_actualizacion=bodega_elegida_query.fecha_ultima_actualizacion,
            historia=bodega_elegida_query.historia,
            nombre=bodega_elegida_query.nombre,
            periodo_actualizacion=bodega_elegida_query.periodo_actualizacion,
        )
        return True

    def determinar_vinos_actualizar(self, vinos_todos: list):

        vinos_sistema_bodega_obj = []
        for key,value in self.obtener_actualizacion_vinos_bodega().items():
            vino_act = Vino(
                añada=value["aniada"],
                fecha_actualizacion=value["fechaActualizacion"],
                imagen_etiqueta=value["imagenEtiqueta"],
                nombre=value["nombre"],
                nota_cata_bodega=value["notaDeCataBodega"],
                precio_ars=value["precioARS"]
                )
            print(vino_act)
# self.bodega_elegida.tenes_este_vino()

    def actualizar_caracteristicas_vino_existente(self):
        ...

    def actualizar_o_crear_vinos(self):
        ...

    def buscar_maridaje(self):
        ...

    def buscar_seguidores_bodega(self):
        ...

    def buscar_tipo_uva(self):
        ...

    def crear_vino(self):
        ...

    def fin_caso_uso(self):
        ...

    def get_fecha_hora_actual(self):
        ...

    def opcion_importar_actualizacion_vinos(self):
        ...

    @staticmethod
    def obtener_actualizacion_vinos_bodega():
        return {
            "1": {
                "aniada": 2010,
                "fechaActualizacion": "23-01-2024",
                "imagenEtiqueta": "imageTrumpeter.jpg",
                "nombre": "Trumpeter",
                "notaDeCataBodega": "Notas de frutilla, con un final de vainilla y roble.",
                "precioARS": 1200
            },
            "2": {
                "aniada": 2021,
                "fechaActualizacion": "23-05-2024",
                "imagenEtiqueta": "imagenChardonnay.jpg",
                "nombre": "Chardonnay",
                "notaDeCataBodega": "Aromas de manzana y pera, con un toque de cítricos y pomelo.",
                "precioARS": 850
            }
        }
    # @staticmethod
    # def obtener_fecha_actual():
    #     return datetime.date.today()


class Bodega:
    def __init__(self, coordenadas_ubicacion, descripcion, fecha_ultima_actualizacion, historia, nombre,
                 periodo_actualizacion):
        self.coordenadas_ubicacion = coordenadas_ubicacion
        self.descripcion = descripcion
        self.fecha_ultima_actualizacion = fecha_ultima_actualizacion
        self.historia = historia
        self.nombre = nombre
        self.periodo_actualizacion = periodo_actualizacion

    def tenes_este_vino(self):
        ...

    def esta_para_actualizar_novedades_vino(self):
        hoy = datetime.date.today()
        diferencia_dias = (hoy - self.fecha_ultima_actualizacion).days
        if diferencia_dias > 60:
            return True

    def get_nombre(self):
        return self.nombre

    def set_fecha_ultima_actualizacion(self):
        ...

    def actualizar_datos_vino(self):
        ...

    def __str__(self):
        return 'Bodega: ' + self.nombre


class Vino:
    def __init__(self, añada, fecha_actualizacion, imagen_etiqueta, nombre, nota_cata_bodega, precio_ars):
        self.añada = añada
        self.fecha_actualizacion = fecha_actualizacion
        self.imagen_etiqueta = imagen_etiqueta
        self.nombre = nombre
        self.nota_cata_bodega = nota_cata_bodega
        self.precio_ars = precio_ars

    def crear_varietal(self):
        ...

    def set_fecha_actualizacion(self, fecha: datetime.date):
        self.fecha_actualizacion = fecha

    def set_imagen_atiqueta(self, imagen):
        self.imagen_etiqueta = imagen
        # ?

    def set_nota_cata(self, nota_cata: str):
        self.nota_cata_bodega = nota_cata

    def set_precio(self, precio: Union[int, float]):
        self.precio_ars = precio

    def sos_este_vino(self, vino):
        ...

    def sos_vino_actualizar(self):
        ...


class Enofilo:
    def __init__(self, apellido, imagen_perfil, nombre):
        self.apellido = apellido
        self.imagen_perfil = imagen_perfil
        self.nombre = nombre

    def get_nombre_usuario(self):
        ...

    def seguis_a_bodega(self):
        ...


class Maridaje:

    def __init__(self, descripcion, nombre):
        self.descripcion = descripcion
        self.nombre = nombre


class Varietal:
    def __init__(self, descripcion, porcentaje_composicion):
        self.descripcion = descripcion
        self.porcentaje_composicion = porcentaje_composicion


class TipoUva:
    def __init__(self, descripcion, nombre):
        self.descripcion = descripcion
        self.nombre = nombre

    def sos_tipo_uva(self):
        ...


class Siguiendo:
    def __init__(self, fecha_inicio, fecha_fin=None):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
