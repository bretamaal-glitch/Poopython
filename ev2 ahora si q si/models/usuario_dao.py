from __future__ import annotations

import sqlite3
from sqlite3 import Cursor

from config.database import Database
from models.persona_dao import PersonaDAO
from models.usuario import Usuario
from models.validaciones import validar_texto
from models.validaciones_dao import consultar, existe, validar_no_existe


class UsuarioDAO:
    @staticmethod
    def crear(usuario: Usuario) -> bool:
        conn = Database().get_connection()
        try:
            validar_no_existe("usuario", "id_usuario", usuario.id_usuario, "id_usuario")
            validar_no_existe("usuario", "nombre_usuario", usuario.nombre_usuario, "nombre_usuario")
            validar_no_existe("usuario", "id_persona", usuario.persona.id_persona, "persona")
            persona_nueva = not existe("persona", "id_persona", usuario.persona.id_persona)
            cursor: Cursor = conn.cursor()
            if persona_nueva:
                PersonaDAO._insertar(cursor, usuario.persona)
            cursor.execute(
                "INSERT INTO usuario (id_usuario, nombre_usuario, contrasena, rol, id_persona) "
                "VALUES (?, ?, ?, ?, ?)",
                (usuario.id_usuario, usuario.nombre_usuario, usuario.contrasena,
                 usuario.rol, usuario.persona.id_persona)
            )
            conn.commit()
            return True
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al crear usuario en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def _construir(fila) -> Usuario:
        persona = PersonaDAO.obtener_por_id(fila["id_persona"])
        return Usuario(fila["id_usuario"], fila["nombre_usuario"], fila["contrasena"], fila["rol"], persona)

    @staticmethod
    def obtener_todos() -> list[Usuario]:
        usuarios = []
        try:
            for fila in consultar("SELECT * FROM usuario"):
                usuarios.append(UsuarioDAO._construir(fila))
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener usuarios: {e}")
        return usuarios

    @staticmethod
    def obtener_por_id(id_usuario: str) -> Usuario | None:
        try:
            filas = consultar("SELECT * FROM usuario WHERE id_usuario = ?",
                              (validar_texto(id_usuario, "id_usuario"),))
            return UsuarioDAO._construir(filas[0]) if filas else None
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener el usuario: {e}")
            return None

    @staticmethod
    def obtener_por_nombre(nombre_usuario: str) -> Usuario | None:
        """Se usa para iniciar sesión: luego se llama a Usuario.autenticar()."""
        try:
            filas = consultar("SELECT * FROM usuario WHERE nombre_usuario = ?", (nombre_usuario,))
            return UsuarioDAO._construir(filas[0]) if filas else None
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener el usuario por nombre: {e}")
            return None

    @staticmethod
    def actualizar(usuario: Usuario) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuario SET nombre_usuario = ?, contrasena = ?, rol = ? WHERE id_usuario = ?",
                (usuario.nombre_usuario, usuario.contrasena, usuario.rol, usuario.id_usuario)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_usuario: str) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (validar_texto(id_usuario, "id_usuario"),))
            conn.commit()
            return cursor.rowcount > 0
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            conn.close()
