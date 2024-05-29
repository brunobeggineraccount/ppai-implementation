import datetime
from typing import Union
import json
import os
import django
from .models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.join('../ppai/settings.py'))
django.setup()


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
        for key, value in self.obtener_actualizacion_vinos_bodega().items():
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
        ...

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
                "maridaje": "Queso",
                "tipoUva": "Bonarda",
                "aniada": 2010,
                "fechaActualizacion": "23-01-2024",
                "imagenEtiqueta": "imageTrumpeter.jpg",
                "nombre": "Alejandro",
                "notaDeCataBodega": "TP PPAI",
                "precioARS": 0,
                "varietal": {
                    "descripcion": "Descripcion varietal",
                    "porcentaje_composicion": "73%"
                }
            },
            "2": {
                "maridaje": "Pasta",
                "tipoUva": "Syrah",
                "aniada": 2010,
                "fechaActualizacion": "23-01-2024",
                "imagenEtiqueta": "imageTrumpeter.jpg",
                "nombre": "Hola como andas",
                "notaDeCataBodega": "efoiweljfweñlf",
                "precioARS": 0,
                "varietal": {
                    "descripcion": "Nico",
                    "porcentaje_composicion": "73%"
                }
            }
        }


class Bodega:
    def __init__(self, coordenadas_ubicacion, descripcion, fecha_ultima_actualizacion, historia, nombre,
                 periodo_actualizacion, vinos=None):
        self.coordenadas_ubicacion = coordenadas_ubicacion
        self.descripcion = descripcion
        self.fecha_ultima_actualizacion = fecha_ultima_actualizacion
        self.historia = historia
        self.nombre = nombre
        self.periodo_actualizacion = periodo_actualizacion
        self.vinos = vinos

    def tenes_este_vino(self, vino_actualizacion: list):
        for mi_vino in self.vinos:
            if mi_vino.sos_este_vino(vino_actualizacion.nombre):
                return True
        return False

    def esta_para_actualizar_novedades_vino(self, fecha):
        diferencia_dias = (fecha - self.fecha_ultima_actualizacion).days
        if diferencia_dias > 60:
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

    # def sos_este_vino(self, vino):
    #     ...


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

    def sos_maridaje(self, maridaje_vino_a_crear):
        if self.nombre == maridaje_vino_a_crear:
            return True
        return False


class Varietal:
    def __init__(self, descripcion=None, porcentaje_composicion=None, tipo_uva=None):
        self.descripcion = descripcion
        self.porcentaje_composicion = porcentaje_composicion
        self.tipo_uva = tipo_uva

    def new(self):
        varietal = VarietalModel.objects.get_or_create(
            descripcion=self.descripcion,
            porcentaje_composicion=self.porcentaje_composicion,
            tipo_uva=self.tipo_uva
        )
        return varietal


class TipoUva:
    def __init__(self, descripcion, nombre):
        self.descripcion = descripcion
        self.nombre = nombre

    def sos_tipo_uva(self, tipo_uva_a_crear):
        if self.nombre == tipo_uva_a_crear:
            return True
        return False


class Siguiendo:
    def __init__(self, fecha_inicio, fecha_fin=None):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
