from __future__ import annotations

import sqlite3
from sqlite3 import Cursor

from config.database import Database
from models.proyecto import Proyecto
from models.validaciones_dao import (
    consultar, existe, fecha_a_texto, marcas, texto_a_fecha, validar_id, validar_no_existe,
)


class ProyectoDAO:
    @staticmethod
    def _cargar(id_proyecto: str, cache: dict) -> Proyecto | None:
        clave = ("proyecto", id_proyecto)
        if clave in cache:
            return cache[clave]
        filas = consultar("SELECT * FROM proyecto WHERE id_proyecto = ?", (id_proyecto,))
        if not filas:
            return None
        fila = filas[0]
        proyecto = Proyecto(fila["id_proyecto"], fila["nombre"],
                            texto_a_fecha(fila["fecha_inicio"], "fecha_inicio"))
        cache[clave] = proyecto          # se registra antes de completarlo: evita ciclos
        ProyectoDAO._completar(proyecto, cache)
        return proyecto

    @staticmethod
    def _completar(proyecto: Proyecto, cache: dict) -> None:
        marca = ("completo", "proyecto", proyecto.id_proyecto)
        if marca in cache:
            return
        cache[marca] = True

        from models.empleado_dao import EmpleadoDAO        
        from models.registro_tiempo_dao import RegistroTiempoDAO

        for fila in consultar("SELECT id_empleado FROM empleado_proyecto WHERE id_proyecto = ?",
                              (proyecto.id_proyecto,)):
            empleado = EmpleadoDAO._cargar(fila["id_empleado"], cache)
            empleado.asignar_proyecto(proyecto)              

        for fila in consultar("SELECT id_registro FROM registro_tiempo WHERE id_proyecto = ?",
                              (proyecto.id_proyecto,)):
            RegistroTiempoDAO._cargar(fila["id_registro"], cache)

    @staticmethod
    def obtener_todos() -> list[Proyecto]:
        proyectos = []
        cache: dict = {}
        try:
            for fila in consultar("SELECT id_proyecto FROM proyecto"):
                proyectos.append(ProyectoDAO._cargar(fila["id_proyecto"], cache))
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener proyectos: {e}")
        return proyectos

    @staticmethod
    def obtener_por_id(id_proyecto: str) -> Proyecto | None:
        try:
            return ProyectoDAO._cargar(validar_id(id_proyecto, "id_proyecto"), {})
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener el proyecto: {e}")
            return None

    @staticmethod
    def crear(proyecto: Proyecto) -> bool:
        conn = Database().get_connection()
        try:
            validar_no_existe("proyecto", "id_proyecto", proyecto.id_proyecto, "id_proyecto")
            ids_empleados = [e.id_empleado for e in proyecto.empleados
                             if existe("empleado", "id_empleado", e.id_empleado)]

            cursor: Cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO proyecto (id_proyecto, nombre, fecha_inicio) VALUES (?, ?, ?)",
                (proyecto.id_proyecto, proyecto.nombre, fecha_a_texto(proyecto.fecha_inicio))
            )
            for id_empleado in ids_empleados:
                cursor.execute(
                    "INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (?, ?)",
                    (id_empleado, proyecto.id_proyecto)
                )
            conn.commit()
            return True
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al crear proyecto en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar(proyecto: Proyecto) -> bool:
        conn = Database().get_connection()
        try:
            ids_empleados = [e.id_empleado for e in proyecto.empleados
                             if existe("empleado", "id_empleado", e.id_empleado)]

            cursor: Cursor = conn.cursor()
            cursor.execute(
                "UPDATE proyecto SET nombre = ?, fecha_inicio = ? WHERE id_proyecto = ?",
                (proyecto.nombre, fecha_a_texto(proyecto.fecha_inicio), proyecto.id_proyecto)
            )
            actualizado = cursor.rowcount > 0

            if ids_empleados:
                cursor.execute(
                    f"DELETE FROM empleado_proyecto WHERE id_proyecto = ? AND id_empleado NOT IN ({marcas(ids_empleados)})",
                    (proyecto.id_proyecto, *ids_empleados)
                )
            else:
                cursor.execute("DELETE FROM empleado_proyecto WHERE id_proyecto = ?", (proyecto.id_proyecto,))
            for id_empleado in ids_empleados:
                cursor.execute(
                    "INSERT OR IGNORE INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (?, ?)",
                    (id_empleado, proyecto.id_proyecto)
                )
            conn.commit()
            return actualizado
        except sqlite3.Error as e:
            print(f"Error al actualizar proyecto: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_proyecto: str) -> bool:
        """Falla si el proyecto tiene registros de tiempo (RESTRICT)."""
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM proyecto WHERE id_proyecto = ?", (validar_id(id_proyecto, "id_proyecto"),))
            conn.commit()
            return cursor.rowcount > 0
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al eliminar proyecto: {e}")
            return False
        finally:
            conn.close()
