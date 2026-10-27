from __future__ import annotations
from datetime import date
from models.proyecto import Proyecto
from models.validaciones import validar_fecha, validar_numero, validar_texto


class RegistroTiempo:
    horas_maximas_dia = 24

    def __init__(self, id_registro: str, fecha: date, horas_trabajadas: float,
                 proyecto: Proyecto, descripcion: str):
        self.id_registro = id_registro
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.proyecto = proyecto
        self.descripcion = descripcion
        self._empleado = None

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
        valor = validar_numero(horas, "horas_trabajadas")
        if not 0 < valor <= self.horas_maximas_dia:
            raise ValueError(f"Las horas trabajadas deben estar entre 0 y {self.horas_maximas_dia}.")
        self._horas_trabajadas = valor

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion: str) -> None:
        self._descripcion = validar_texto(descripcion, "descripcion")

    @property
    def proyecto(self) -> Proyecto:
        return self._proyecto

    @proyecto.setter
    def proyecto(self, proyecto: Proyecto) -> None:
        if not isinstance(proyecto, Proyecto):
            raise TypeError("El proyecto debe ser una instancia de la clase Proyecto.")
        self._proyecto = proyecto

    @property
    def empleado(self):
        """Empleado al que pertenece el registro (se asigna al crearlo desde Empleado)."""
        return self._empleado

    @property
    def id_empleado(self) -> str | None:
        return self._empleado.id_empleado if self._empleado is not None else None

    def _set_empleado(self, empleado) -> None:
        self._empleado = empleado

    def registrar(self) -> None:
        """Vincula el registro con su proyecto. Lo llama Empleado.registrar_horas."""
        if self._empleado is None:
            raise ValueError("El registro debe pertenecer a un empleado.")
        self.proyecto._agregar_registro(self)

    def __str__(self) -> str:
        return (f"RegistroTiempo | ID: {self.id_registro} | Fecha: {self.fecha.strftime('%d-%m-%Y')} | "
                f"Horas: {self.horas_trabajadas} | Proyecto: {self.proyecto.id_proyecto}")

    def __repr__(self) -> str:
        return (f"RegistroTiempo(id_registro='{self.id_registro}', fecha={self.fecha!r}, "
                f"horas_trabajadas={self.horas_trabajadas}, proyecto={repr(self.proyecto)})")
