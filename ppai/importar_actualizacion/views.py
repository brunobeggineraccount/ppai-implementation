from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .utils import *


# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, template_name='./importar_actualizacion/base.html')

    if request.method == "post":
        ...


def importar_actualizacion(request):
    if request.method == "GET":
        gestor = GestorImportadorBodega()
        gestor.bodegas = []
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
            gestor.bodegas.append(bodega)
        bodegas_para_actualizar = gestor.buscar_bodegas_actualizar()
        context = {"bodegas_para_actualizar": bodegas_para_actualizar}

        return render(request,
                      template_name='./importar_actualizacion/importar_actualizacion.html',
                      context=context)

    if request.method == "POST":
        gestor = GestorImportadorBodega()
        bodega_elegida_nombre = request.POST.get('bodega_elegida')
        bodega_elegida_query = BodegaModel.objects.get(nombre=bodega_elegida_nombre)
        if gestor.tomar_seleccion_bodega(bodega_elegida_query):
            vinos_query = VinoModel.objects.all()
            vinos_obj = []
            for vino in vinos_query:
                vino_obj = Vino(
                    añada=vino.aniada,
                    fecha_actualizacion=vino.fecha_actualizacion,
                    imagen_etiqueta=vino.imagen_etiqueta,
                    nombre=vino.nombre,
                    nota_cata_bodega=vino.nota_cata_bodega,
                    precio_ars=vino.precio_ars
                )
                vinos_obj.append(vino)
            gestor.determinar_vinos_actualizar(vinos_obj)
            return HttpResponse(reverse('tomar-seleccion'))
        else:
            return HttpResponse("Ha ocurrido un error al tomar la bodega seleccionada")


def tomar_seleccion_bodega(request):
    if request.method == "GET":
        return render(request,
                      template_name='./importar_actualizacion/tomar_seleccion_bodega.html')

    if request.method == "POST":
        ...
