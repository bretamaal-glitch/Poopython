from __future__ import annotations

import sqlite3
from sqlite3 import Cursor

from config.database import Database
from models.departamento import Departamento
from models.validaciones_dao import (
    consultar, existe, marcas, validar_existe, validar_id, validar_no_existe,
)


class DepartamentoDAO:
    """
    Data Access Object para la entidad Departamento.
    El gerente es un empleado y debe existir en la base antes de guardar el departamento.
    Los miembros se actualizan aquí solo si ya existen; los demás se guardan al crearse.
    """
    @staticmethod
    def _cargar(id_departamento: str, cache: dict) -> Departamento | None:
        clave = ("departamento", id_departamento)
        if clave in cache:
            return cache[clave]
        filas = consultar("SELECT * FROM departamento WHERE id_departamento = ?", (id_departamento,))
        if not filas:
            return None
        fila = filas[0]

        from models.empleado_dao import EmpleadoDAO   # importación local (evita ciclo)

        # Mientras se construye, el gerente no vuelve a pedir este departamento.
        en_construccion = ("en_construccion", "departamento", id_departamento)
        cache[en_construccion] = True
        gerente = EmpleadoDAO._cargar(fila["id_gerente"], cache)
        departamento = Departamento(fila["id_departamento"], fila["nombre"], gerente)
        cache[clave] = departamento
        del cache[en_construccion]

        for f in consultar("SELECT id_empleado FROM empleado WHERE id_departamento = ?", (id_departamento,)):
            miembro = EmpleadoDAO._cargar(f["id_empleado"], cache)
            departamento.asignar_empleado(miembro)   # no hace nada si ya es miembro
        return departamento

    @staticmethod
    def obtener_todos() -> list[Departamento]:
        departamentos = []
        cache: dict = {}
        try:
            for fila in consultar("SELECT id_departamento FROM departamento"):
                departamentos.append(DepartamentoDAO._cargar(fila["id_departamento"], cache))
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener departamentos: {e}")
        return departamentos

    @staticmethod
    def obtener_por_id(id_departamento: str) -> Departamento | None:
        try:
            return DepartamentoDAO._cargar(validar_id(id_departamento, "id_departamento"), {})
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener el departamento: {e}")
            return None

    @staticmethod
    def buscar_por_nombre(texto: str) -> list[Departamento]:
        departamentos = []
        cache: dict = {}
        try:
            for fila in consultar("SELECT id_departamento FROM departamento WHERE nombre LIKE ? ORDER BY nombre",
                                  (f"%{texto.strip()}%",)):
                departamentos.append(DepartamentoDAO._cargar(fila["id_departamento"], cache))
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al buscar departamentos: {e}")
        return departamentos

    @staticmethod
    def crear(departamento: Departamento) -> bool:
        conn = Database().get_connection()
        try:
            validar_no_existe("departamento", "id_departamento", departamento.id_departamento, "id_departamento")
            validar_existe("empleado", "id_empleado", departamento.gerente.id_empleado, "gerente")
            ids = [e.id_empleado for e in departamento.empleados
                   if existe("empleado", "id_empleado", e.id_empleado)]

            cursor: Cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO departamento (id_departamento, nombre, id_gerente) VALUES (?, ?, ?)",
                (departamento.id_departamento, departamento.nombre, departamento.gerente.id_empleado)
            )
            if ids:
                cursor.execute(
                    f"UPDATE empleado SET id_departamento = ? WHERE id_empleado IN ({marcas(ids)})",
                    (departamento.id_departamento, *ids)
                )
            conn.commit()
            return True
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al crear departamento en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar(departamento: Departamento) -> bool:
        conn = Database().get_connection()
        try:
            validar_existe("empleado", "id_empleado", departamento.gerente.id_empleado, "gerente")
            ids = [e.id_empleado for e in departamento.empleados
                   if existe("empleado", "id_empleado", e.id_empleado)]

            cursor: Cursor = conn.cursor()
            cursor.execute(
                "UPDATE departamento SET nombre = ?, id_gerente = ? WHERE id_departamento = ?",
                (departamento.nombre, departamento.gerente.id_empleado, departamento.id_departamento)
            )
            actualizado = cursor.rowcount > 0

            # Quien ya no es miembro queda sin departamento; los miembros actuales se asignan.
            if ids:
                cursor.execute(
                    f"UPDATE empleado SET id_departamento = NULL "
                    f"WHERE id_departamento = ? AND id_empleado NOT IN ({marcas(ids)})",
                    (departamento.id_departamento, *ids)
                )
                cursor.execute(
                    f"UPDATE empleado SET id_departamento = ? WHERE id_empleado IN ({marcas(ids)})",
                    (departamento.id_departamento, *ids)
                )
            else:
                cursor.execute(
                    "UPDATE empleado SET id_departamento = NULL WHERE id_departamento = ?",
                    (departamento.id_departamento,)
                )
            conn.commit()
            return actualizado
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al actualizar departamento: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_departamento: str) -> bool:
        """Los empleados del departamento quedan sin departamento (SET NULL)."""
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM departamento WHERE id_departamento = ?",
                           (validar_id(id_departamento, "id_departamento"),))
            conn.commit()
            return cursor.rowcount > 0
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al eliminar departamento: {e}")
            return False
        finally:
            conn.close()
