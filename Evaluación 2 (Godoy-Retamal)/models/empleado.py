from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from models.persona import Persona
from models.proyecto import Proyecto
from models.registro_tiempo import RegistroTiempo
from models.validaciones import validar_fecha, validar_numero, validar_texto

if TYPE_CHECKING:
    from models.departamento import Departamento


class Empleado(Persona):
    
    ESTADOS: set[str] = {"Activo", "Inactivo"}

    def __init__(self, id_persona: str, nombre: str, email: str, telefono: str, direccion: str,
                 id_empleado: str, fecha_contrato: date, salario: float):
        super().__init__(id_persona, nombre, email, telefono, direccion)
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

    @fecha_contrato.setter
    def fecha_contrato(self, fecha: date) -> None:
        self._fecha_contrato = validar_fecha(fecha, "fecha_contrato")

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
            opciones = ", ".join(sorted(self.ESTADOS))
            raise ValueError(f"Estado '{nuevo_estado}' no válido. Opciones permitidas: {opciones}.")
        self._estado = nuevo_estado

    def asignar_proyecto(self, proyecto: Proyecto) -> None:
        if not isinstance(proyecto, Proyecto):
            raise TypeError("El proyecto debe ser una instancia de la clase Proyecto.")
        if proyecto in self._proyectos:
            return
        self._proyectos.append(proyecto)
        proyecto._agregar_empleado(self)

    def desasignar_proyecto(self, proyecto: Proyecto) -> None:
        """Quita al empleado de un proyecto. No se permite si tiene registros en él."""
        if proyecto not in self._proyectos:
            raise ValueError("El empleado no está asignado a ese proyecto.")
        if any(r.proyecto is proyecto for r in self._registros):
            raise ValueError("No se puede desasignar: el empleado tiene registros de tiempo en ese proyecto.")
        self._proyectos.remove(proyecto)
        proyecto._quitar_empleado(self)

    def registrar_horas(self, id_registro: str, fecha: date, horas: float,
                        descripcion: str, proyecto: Proyecto) -> RegistroTiempo:
        """Crea el registro validando estado, asignación y fechas."""
        if self._estado != "Activo":
            raise ValueError("Un empleado inactivo no puede registrar horas.")
        if proyecto not in self._proyectos:
            raise ValueError("Solo se pueden registrar horas en proyectos asignados.")
        registro = RegistroTiempo(id_registro, fecha, horas, proyecto, descripcion)
        if registro.fecha < self._fecha_contrato:
            raise ValueError("La fecha del registro es anterior al contrato del empleado.")
        if registro.fecha < proyecto.fecha_inicio:
            raise ValueError("La fecha del registro es anterior al inicio del proyecto.")
        registro._set_empleado(self)
        registro.registrar()
        self._registros.append(registro)
        return registro

    def _restaurar_registro(self, registro: RegistroTiempo) -> None:
        """Vuelve a vincular un registro que ya existe en la base (no valida ni crea nada)."""
        if registro not in self._registros:
            self._registros.append(registro)
            registro._set_empleado(self)
            registro.proyecto._agregar_registro(registro)

    def _set_departamento(self, departamento: Departamento | None) -> None:
        self._departamento = departamento

    def __str__(self) -> str:
        depto = self.departamento.nombre if self.departamento else "Sin departamento"
        return (f"Empleado | ID: {self.id_empleado} | Nombre: {self.nombre} | "
                f"Estado: {self.estado} | Departamento: {depto}")

    def __repr__(self) -> str:
        return (f"Empleado(id_empleado='{self.id_empleado}', nombre='{self.nombre}', "
                f"salario={self.salario}, estado='{self.estado}')")
