from __future__ import annotations

import sqlite3
from sqlite3 import Cursor

from config.database import Database
from models.informe import Informe
from models.validaciones_dao import consultar, validar_id, validar_no_existe


class InformeDAO:

    @staticmethod
    def crear(informe: Informe) -> bool:
        conn = Database().get_connection()
        try:
            validar_no_existe("informe", "id_informe", informe.id_informe, "id_informe")
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO informe (id_informe, tipo, formato, contenido) VALUES (?, ?, ?, ?)",
                (informe.id_informe, informe.tipo, informe.formato, informe.contenido)
            )
            conn.commit()
            return True
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al crear informe en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def _construir(fila) -> Informe:
        return Informe(fila["id_informe"], fila["tipo"], fila["formato"], fila["contenido"])

    @staticmethod
    def obtener_todos() -> list[Informe]:
        informes = []
        try:
            for fila in consultar("SELECT * FROM informe"):
                informes.append(InformeDAO._construir(fila))
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al obtener informes: {e}")
        return informes

    @staticmethod
    def obtener_por_id(id_informe: str) -> Informe | None:
        try:
            filas = consultar("SELECT * FROM informe WHERE id_informe = ?",
                              (validar_id(id_informe, "id_informe"),))
            return InformeDAO._construir(filas[0]) if filas else None
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al obtener el informe: {e}")
            return None

    @staticmethod
    def actualizar(informe: Informe) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "UPDATE informe SET tipo = ?, formato = ?, contenido = ? WHERE id_informe = ?",
                (informe.tipo, informe.formato, informe.contenido, informe.id_informe)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar informe: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_informe: str) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM informe WHERE id_informe = ?", (validar_id(id_informe, "id_informe"),))
            conn.commit()
            return cursor.rowcount > 0
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al eliminar informe: {e}")
            return False
        finally:
            conn.close()
