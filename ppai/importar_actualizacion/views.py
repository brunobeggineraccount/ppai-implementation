from typing import List

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .utils.control.gestor import GestorImportadorBodega
from .models import *
from .utils.entity.vino import Vino
from .utils.interfaces.IObservadorNotificaciones import IObservadorNotificaciones


# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, template_name='./importar_actualizacion/presentacion.html')

    if request.method == "POST":
        ...


def importar_actualizacion(request):
    if request.method == "GET":
        gestor = GestorImportadorBodega()

        bodegas_para_actualizar = gestor.buscar_bodegas_actualizar()

        if len(bodegas_para_actualizar) == 0:
            bodegas_para_actualizar = 0

        context = {"bodegas_para_actualizar": bodegas_para_actualizar}
        return render(request,
                      template_name='./importar_actualizacion/importar_actualizacion.html',
                      context=context)

    if request.method == "POST":
        gestor = GestorImportadorBodega()

        bodega_elegida_nombre = request.POST.get('bodega_elegida')

        gestor.tomar_seleccion_bodega(bodega_elegida_nombre)

        vinos_clasificados = gestor.determinar_vinos_actualizar()
        if vinos_clasificados == 400:
            request.session["status"] = {"status": 400}
            return redirect(reverse('tomar-seleccion'))
        else:
            request.session["status"] = {"status": 200}

        id_vinos = gestor.actualizar_o_crear_vinos(vinos_clasificados)

        request.session["contexto"] = id_vinos
        request.session["bodega"] = {"bodega": gestor.bodega_elegida.nombre}
        gestor.bodega_elegida.set_fecha_ultima_actualizacion()

        return redirect(reverse('tomar-seleccion'))


def resumen(request):
    if request.method == "GET":
        from importar_actualizacion.utils.boundary.InterfazNotificacionesPush import InterfazNotificacionesPush
        from .models import BodegaModel
        observers: List[IObservadorNotificaciones] = []
        interfazNotificacionPush = InterfazNotificacionesPush()
        observers.append(interfazNotificacionPush)
        if request.session.get('status')["status"] == 400:
            return render(request,
                              template_name='./importar_actualizacion/resumen.html',
                              context={"error": 400})

        context = request.session.get('contexto')
        bodega_elegida = request.session.get("bodega")["bodega"]
        per = BodegaModel.objects.get(nombre=bodega_elegida).periodo_actualizacion

        creados, actualizados = [], []
        vinos: List[str] = []
        for vino_id in context["creados"]:
            vino_model = VinoModel.objects.get(id=vino_id)
            vinos.append(vino_model.nombre)
            creados.append(vino_model)
        for vino_id in context["actualizados"]:
            vino_model = VinoModel.objects.get(id=vino_id)
            vinos.append(vino_model.nombre)
            actualizados.append(vino_model)

        context = {"creados": creados, "actualizados": actualizados}
        if not context["creados"]:
            context["creados"] = 0
        if not context["actualizados"]:
            context["actualizados"] = 0

        gestor = GestorImportadorBodega()
        gestor.periodo_actualizacion = per
        gestor.informacion_vinos_importada = vinos
        gestor.bodega_elegida = bodega_elegida
        gestor.buscar_seguidores_bodega()
        gestor.suscribir(observers)
        gestor.notificar()
        context["seguidores"] = gestor.enofilos_seguidores_bodega
        if not context["seguidores"]:
            context["seguidores"] = 0

        context["patron_cumplido"] = int(gestor.patron_cumplido)

        return render(request,
                      template_name='./importar_actualizacion/resumen.html',
                      context=context)

    if request.method == "POST":
        ...
