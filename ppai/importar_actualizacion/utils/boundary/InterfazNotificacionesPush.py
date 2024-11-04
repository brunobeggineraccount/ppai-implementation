from typing import List

from ..interfaces.IObservadorNotificaciones import IObservadorNotificaciones


class InterfazNotificacionesPush(IObservadorNotificaciones):

    def actualizar(self, nombreBodega: str, infoVinosImportados: List[str], periodoActualizacion: int):
        print(f"Observador actualizado {nombreBodega}, {infoVinosImportados}, {periodoActualizacion}")
        self.notificarNovedadVinoParaBodega()

    @staticmethod
    def notificarNovedadVinoParaBodega():
        ...
