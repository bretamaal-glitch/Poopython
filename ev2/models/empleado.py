from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
"""preguntale al profe si esto es necesario junto con IF TYPE_CHECKING"""
from validaciones import validar_fecha, validar_numero, validar_texto
from persona import Persona
from proyecto import Proyecto
from registro_tiempo import RegistroTiempo

if TYPE_CHECKING:
    from departamento import Departamento
"""ESTO!! la ia dice que es para evitar importaciones circulares, pero no entiendo como funciona"""

class Empleado(Persona):
    ESTADOS: set[str] = {"Activo", "Inactivo"}

    def __init__(self, id_persona: str, nombre: str, email: str, telefono: str,
                 id_empleado: str, fecha_contrato: date, salario: float):
        super().__init__(id_persona, nombre, email, telefono)
        self._id_empleado = validar_texto(id_empleado, "id_empleado").upper()
        self._fecha_contrato = validar_fecha(fecha_contrato, "fecha_contrato")
        self.salario = salario
        self._estado = "Activo"
        self._departamento: Departamento | None = None
        self._proyectos: list[Proyecto] = []
        self._registros: list[RegistroTiempo] = []

    @property
    def id_empleado(self) -> str:
        return self._id_empleado

    @property
    def fecha_contrato(self) -> date:
        return self._fecha_contrato

    @property
    def salario(self) -> float:
        return self._salario

    @salario.setter
    def salario(self, salario: float) -> None:
        valor = validar_numero(salario, "salario")
        if valor < 0:
            raise ValueError("El salario no puede ser negativo.")
        self._salario = valor

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def departamento(self) -> Departamento | None:
        return self._departamento

    @property
    def proyectos(self) -> tuple[Proyecto, ...]:
        return tuple(self._proyectos)

    @property
    def registros(self) -> tuple[RegistroTiempo, ...]:
        return tuple(self._registros)

    def cambiar_estado(self, nuevo_estado: str) -> None:
        if nuevo_estado not in self.ESTADOS:
            opciones = ", ".join(self.ESTADOS)
            raise ValueError(f"Estado '{nuevo_estado}' no válido. Opciones permitidas: {opciones}.")
        self._estado = nuevo_estado

    def asignar_proyecto(self, proyecto: Proyecto) -> None:
        if not isinstance(proyecto, Proyecto):
            raise TypeError("El proyecto debe ser una instancia de la clase Proyecto.")
        if proyecto in self._proyectos:
            return
        self._proyectos.append(proyecto)
        proyecto._agregar_empleado(self)

    def registrar_horas(self, id_registro: str, fecha: date, horas: float,
                        proyecto: Proyecto) -> RegistroTiempo:
        """Crea el registro validando estado, asignación y fechas."""
        if self._estado != "Activo":
            raise ValueError("Un empleado inactivo no puede registrar horas.")
        if proyecto not in self._proyectos:
            raise ValueError("Solo se pueden registrar horas en proyectos asignados.")
        registro = RegistroTiempo(id_registro, fecha, horas, proyecto)
        if registro.fecha < self._fecha_contrato:
            raise ValueError("La fecha del registro es anterior al contrato del empleado.")
        if registro.fecha < proyecto.fecha_inicio:
            raise ValueError("La fecha del registro es anterior al inicio del proyecto.")
        registro.registrar()
        self._registros.append(registro)
        return registro

    def _set_departamento(self, departamento: Departamento | None) -> None:
        self._departamento = departamento

    def __str__(self) -> str:
        depto = self.departamento.nombre if self.departamento else "Sin departamento"
        return (f"Empleado | ID: {self.id_empleado} | Nombre: {self.nombre} | "
                f"Estado: {self.estado} | Departamento: {depto}")

    def __repr__(self) -> str:
        return (f"Empleado(id_empleado='{self.id_empleado}', nombre='{self.nombre}', "
                f"salario={self.salario}, estado='{self.estado}')")
