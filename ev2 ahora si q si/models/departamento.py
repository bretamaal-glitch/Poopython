from __future__ import annotations
"""usamos future para que las anotaciones de tipos se evaluen más tarde"""
from models.validaciones import validar_texto
from models.empleado import Empleado


class Departamento:

    def __init__(self, id_departamento: str, nombre: str, gerente: Empleado):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self._empleados: list[Empleado] = []
        self._gerente: Empleado | None = None
        self.gerente = gerente

    @classmethod
    def crear_departamento(cls, id_departamento: str, nombre: str,
                           gerente: Empleado) -> Departamento:
        return cls(id_departamento, nombre, gerente)

    @property
    def id_departamento(self) -> str:
        return self._id_departamento

    @id_departamento.setter
    def id_departamento(self, id_departamento: str) -> None:
        self._id_departamento = validar_texto(id_departamento, "id_departamento").upper()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        self._nombre = validar_texto(nombre, "nombre")

    @property
    def gerente(self) -> Empleado | None:
        return self._gerente

    @gerente.setter
    def gerente(self, gerente: Empleado) -> None:
        if not isinstance(gerente, Empleado):
            raise TypeError("El gerente debe ser una instancia de la clase Empleado.")
        self.asignar_empleado(gerente)  # el gerente siempre pertenece al departamento
        self._gerente = gerente

    @property
    def empleados(self) -> tuple[Empleado, ...]:
        return tuple(self._empleados)

    def asignar_empleado(self, empleado: Empleado) -> None:
        """Un empleado pertenece a un solo departamento: si cambia, se retira del anterior."""
        if not isinstance(empleado, Empleado):
            raise TypeError("El empleado debe ser una instancia de la clase Empleado.")
        if empleado in self._empleados:
            return
        anterior = empleado.departamento
        if anterior is not None:
            anterior._quitar_empleado(empleado)
        self._empleados.append(empleado)
        empleado._set_departamento(self)

    def _quitar_empleado(self, empleado: Empleado) -> None:
        if empleado is self._gerente:
            raise ValueError("No se puede retirar al gerente sin asignar antes otro gerente.")
        self._empleados.remove(empleado)
        empleado._set_departamento(None)

    def __str__(self) -> str:
        return (f"Departamento | ID: {self.id_departamento} | Nombre: {self.nombre} | "
                f"Gerente: {self.gerente.nombre if self.gerente else 'Ninguno'} | "
                f"Empleados: {len(self._empleados)}")

    def __repr__(self) -> str:
        return (f"Departamento(id_departamento='{self.id_departamento}', nombre='{self.nombre}', "
                f"gerente={repr(self.gerente)})")
