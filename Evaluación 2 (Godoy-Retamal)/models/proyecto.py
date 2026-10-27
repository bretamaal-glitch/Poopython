from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from models.validaciones import validar_fecha, validar_texto

if TYPE_CHECKING:
    from models.empleado import Empleado
    from models.registro_tiempo import RegistroTiempo


class Proyecto:
    

    def __init__(self, id_proyecto: str, nombre: str, descripcion: str, fecha_inicio: date):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self._empleados: list[Empleado] = []
        self._registros: list[RegistroTiempo] = []

    @property
    def id_proyecto(self) -> str:
        return self._id_proyecto

    @id_proyecto.setter
    def id_proyecto(self, id_proyecto: str) -> None:
        self._id_proyecto = validar_texto(id_proyecto, "id_proyecto").upper()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        self._nombre = validar_texto(nombre, "nombre")

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion: str) -> None:
        self._descripcion = validar_texto(descripcion, "descripcion")

    @property
    def fecha_inicio(self) -> date:
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, fecha_inicio: date) -> None:
        self._fecha_inicio = validar_fecha(fecha_inicio, "fecha_inicio")

    @property
    def empleados(self) -> tuple[Empleado, ...]:
        return tuple(self._empleados)

    @property
    def registros(self) -> tuple[RegistroTiempo, ...]:
        return tuple(self._registros)

    def asignar_empleado(self, empleado: Empleado) -> None:
        
        from models.empleado import Empleado
        if not isinstance(empleado, Empleado):
            raise TypeError("El empleado debe ser una instancia de la clase Empleado.")
        empleado.asignar_proyecto(self)   

    def _agregar_empleado(self, empleado: Empleado) -> None:
        if empleado not in self._empleados:
            self._empleados.append(empleado)

    def _quitar_empleado(self, empleado: Empleado) -> None:
        if empleado in self._empleados:
            self._empleados.remove(empleado)

    def _agregar_registro(self, registro: RegistroTiempo) -> None:
        if registro not in self._registros:
            self._registros.append(registro)

    def __str__(self) -> str:
        return (f"Proyecto | ID: {self.id_proyecto} | Nombre: {self.nombre} | "
                f"Inicio: {self.fecha_inicio.strftime('%d-%m-%Y')} | Empleados: {len(self._empleados)}")

    def __repr__(self) -> str:
        return (f"Proyecto(id_proyecto='{self.id_proyecto}', nombre='{self.nombre}', "
                f"fecha_inicio={self.fecha_inicio!r})")
