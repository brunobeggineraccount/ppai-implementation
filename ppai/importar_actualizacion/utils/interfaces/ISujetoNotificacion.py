from abc import ABC
from abc import abstractmethod
from typing import List

from importar_actualizacion.utils.interfaces.IObservadorNotificaciones import IObservadorNotificaciones


class ISujetoNotificacion(ABC):

    def __init__(self):
        self.observadores: List[IObservadorNotificaciones] = []

    @staticmethod
    @abstractmethod
    def notificar():
        ...

    @staticmethod
    @abstractmethod
    def suscribir(observador: List[IObservadorNotificaciones]):
        ...

    @staticmethod
    @abstractmethod
    def quitar(observador: List[IObservadorNotificaciones]):
        ...
