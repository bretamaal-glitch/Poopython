from __future__ import annotations

from datetime import date

from validaciones import validar_fecha, validar_numero, validar_texto
from proyecto import Proyecto


class RegistroTiempo:

    HORAS_MAXIMAS_DIA = 24

    def __init__(self, id_registro: str, fecha: date, horas_trabajadas: float,
                 proyecto: Proyecto):
        self.id_registro = id_registro
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.proyecto = proyecto

    @property
    def id_registro(self) -> str:
        return self._id_registro

    @id_registro.setter
    def id_registro(self, id_registro: str) -> None:
        self._id_registro = validar_texto(id_registro, "id_registro").upper()

    @property
    def fecha(self) -> date:
        return self._fecha

    @fecha.setter
    def fecha(self, fecha: date) -> None:
        self._fecha = validar_fecha(fecha, "fecha")

    @property
    def horas_trabajadas(self) -> float:
        return self._horas_trabajadas

    @horas_trabajadas.setter
    def horas_trabajadas(self, horas: float) -> None:
        self._horas_trabajadas = validar_numero(horas, "horas_trabajadas")

    @property
    def proyecto(self) -> Proyecto:
        return self._proyecto

    @proyecto.setter
    def proyecto(self, proyecto: Proyecto) -> None:
        if not isinstance(proyecto, Proyecto):
            raise TypeError("El proyecto debe ser una instancia de la clase Proyecto.")
        self._proyecto = proyecto

    def validar_horas(self) -> bool:
        # Igual al CHECK de la tabla: mayor que 0 y menor o igual a 24
        return 0 < self.horas_trabajadas <= self.HORAS_MAXIMAS_DIA

    def registrar(self) -> None:
        if not self.validar_horas():
            raise ValueError(
                f"Las horas trabajadas deben estar entre 0 y {self.HORAS_MAXIMAS_DIA}.")
        self.proyecto._agregar_registro(self)

    def __str__(self) -> str:
        return (f"RegistroTiempo | ID: {self.id_registro} | Fecha: {self.fecha.isoformat()} | "
                f"Horas: {self.horas_trabajadas} | Proyecto: {self.proyecto.id_proyecto}")

    def __repr__(self) -> str:
        return (f"RegistroTiempo(id_registro='{self.id_registro}', fecha={self.fecha!r}, "
                f"horas_trabajadas={self.horas_trabajadas}, proyecto={repr(self.proyecto)})")
