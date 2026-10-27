from __future__ import annotations

import sqlite3
from sqlite3 import Cursor

from config.database import Database
from models.persona import Persona
from models.validaciones_dao import consultar, validar_id, validar_no_existe


class PersonaDAO:
    
    @staticmethod
    def crear(persona: Persona) -> bool:
        conn = Database().get_connection()
        try:
            validar_no_existe("persona", "id_persona", persona.id_persona, "id_persona")
            cursor: Cursor = conn.cursor()
            PersonaDAO._insertar(cursor, persona)
            conn.commit()
            return True
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al crear persona en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def _insertar(cursor: Cursor, persona: Persona) -> None:
        """Inserta solo la fila de persona. La usan EmpleadoDAO y UsuarioDAO."""
        cursor.execute(
            "INSERT INTO persona (id_persona, nombre, email, telefono, direccion) VALUES (?, ?, ?, ?, ?)",
            (persona.id_persona, persona.nombre, persona.email, persona.telefono, persona.direccion)
        )

    @staticmethod
    def _construir(fila) -> Persona:
        return Persona(fila["id_persona"], fila["nombre"], fila["email"], fila["telefono"], fila["direccion"])

    @staticmethod
    def obtener_todos() -> list[Persona]:
        personas = []
        try:
            for fila in consultar("SELECT * FROM persona"):
                personas.append(PersonaDAO._construir(fila))
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al obtener personas: {e}")
        return personas

    @staticmethod
    def obtener_por_id(id_persona: str) -> Persona | None:
        try:
            filas = consultar(
                "SELECT * FROM persona WHERE id_persona = ?",
                (validar_id(id_persona, "id_persona"),)
            )
            return PersonaDAO._construir(filas[0]) if filas else None
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al obtener la persona: {e}")
            return None

    @staticmethod
    def actualizar(persona: Persona) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "UPDATE persona SET nombre = ?, email = ?, telefono = ?, direccion = ? WHERE id_persona = ?",
                (persona.nombre, persona.email, persona.telefono, persona.direccion, persona.id_persona)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar persona: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_persona: str) -> bool:
        """Falla si la persona tiene un usuario (RESTRICT). Si es empleado, se borra en cascada."""
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM persona WHERE id_persona = ?", (validar_id(id_persona, "id_persona"),))
            conn.commit()
            return cursor.rowcount > 0
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al eliminar persona: {e}")
            return False
        finally:
            conn.close()
