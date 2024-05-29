from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .utils import *


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

        id_vinos = gestor.actualizar_o_crear_vinos(vinos_clasificados)

        request.session["contexto"] = id_vinos

        gestor.bodega_elegida.set_fecha_ultima_actualizacion()

        return redirect(reverse('tomar-seleccion'))


def tomar_seleccion_bodega(request):
    if request.method == "GET":
        context = request.session.get('contexto')
        creados = []
        actualizados = []
        for vino_id in context["creados"]:
            creados.append(VinoModel.objects.get(id=vino_id))
        for vino_id in context["actualizados"]:
            actualizados.append(VinoModel.objects.get(id=vino_id))
        context = {"creados": creados, "actualizados": actualizados}
        return render(request,
                      template_name='./importar_actualizacion/tomar_seleccion_bodega.html',
                      context=context)

    if request.method == "POST":
        ...
