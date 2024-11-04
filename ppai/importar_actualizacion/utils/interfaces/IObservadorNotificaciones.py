from abc import ABC
from abc import abstractmethod
from typing import List

class IObservadorNotificaciones(ABC):

    @staticmethod
    @abstractmethod
    def actualizar(nombreBodega: str, infoVinosImportados: List[str], periodoActualizacion: int):
        ...




