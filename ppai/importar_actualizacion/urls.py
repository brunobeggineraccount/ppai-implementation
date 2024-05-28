from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("actualizar/", views.importar_actualizacion, name="importar-actualizacion"),
    path("actualizar/tomar-seleccion/", views.importar_actualizacion, name="tomar-seleccion")
]
