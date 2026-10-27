from __future__ import annotations

import sqlite3
from sqlite3 import Cursor

from config.database import Database
from models.registro_tiempo import RegistroTiempo
from models.validaciones_dao import (
    consultar, fecha_a_texto, texto_a_fecha, validar_asignacion, validar_existe, validar_id,
    validar_no_existe,
)


class RegistroTiempoDAO:

    @staticmethod
    def _cargar(id_registro: str, cache: dict) -> RegistroTiempo | None:
        clave = ("registro", id_registro)
        if clave in cache:
            return cache[clave]
        filas = consultar("SELECT * FROM registro_tiempo WHERE id_registro = ?", (id_registro,))
        if not filas:
            return None
        fila = filas[0]

        from models.empleado_dao import EmpleadoDAO      
        from models.proyecto_dao import ProyectoDAO

        proyecto = ProyectoDAO._cargar(fila["id_proyecto"], cache)
        
        if clave in cache:
            return cache[clave]

        registro = RegistroTiempo(fila["id_registro"], texto_a_fecha(fila["fecha"], "fecha"),
                                  fila["horas_trabajadas"], proyecto, fila["descripcion"])
        cache[clave] = registro
        empleado = EmpleadoDAO._cargar(fila["id_empleado"], cache)
        empleado._restaurar_registro(registro)   
        return registro

    @staticmethod
    def obtener_todos() -> list[RegistroTiempo]:
        registros = []
        cache: dict = {}
        try:
            for fila in consultar("SELECT id_registro FROM registro_tiempo"):
                registros.append(RegistroTiempoDAO._cargar(fila["id_registro"], cache))
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener registros de tiempo: {e}")
        return registros

    @staticmethod
    def obtener_por_id(id_registro: str) -> RegistroTiempo | None:
        try:
            return RegistroTiempoDAO._cargar(validar_id(id_registro, "id_registro"), {})
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener el registro de tiempo: {e}")
            return None

    @staticmethod
    def crear(registro: RegistroTiempo) -> bool:
        conn = Database().get_connection()
        try:
            if registro.empleado is None:
                raise ValueError("El registro debe pertenecer a un empleado.")
            validar_no_existe("registro_tiempo", "id_registro", registro.id_registro, "id_registro")
            validar_existe("empleado", "id_empleado", registro.id_empleado, "empleado")
            validar_existe("proyecto", "id_proyecto", registro.proyecto.id_proyecto, "proyecto")
            validar_asignacion(registro.id_empleado, registro.proyecto.id_proyecto)

            cursor: Cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO registro_tiempo (id_registro, id_empleado, id_proyecto, fecha, horas_trabajadas, descripcion) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (registro.id_registro, registro.id_empleado, registro.proyecto.id_proyecto,
                 fecha_a_texto(registro.fecha), registro.horas_trabajadas, registro.descripcion)
            )
            conn.commit()
            return True
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al crear registro de tiempo en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar(registro: RegistroTiempo) -> bool:
        """Cambia fecha, horas y descripción. Empleado y proyecto no se modifican."""
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "UPDATE registro_tiempo SET fecha = ?, horas_trabajadas = ?, descripcion = ? WHERE id_registro = ?",
                (fecha_a_texto(registro.fecha), registro.horas_trabajadas, registro.descripcion, registro.id_registro)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar registro de tiempo: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_registro: str) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM registro_tiempo WHERE id_registro = ?",
                           (validar_id(id_registro, "id_registro"),))
            conn.commit()
            return cursor.rowcount > 0
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al eliminar registro de tiempo: {e}")
            return False
        finally:
            conn.close()
            
