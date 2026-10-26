from __future__ import annotations

import sqlite3
from sqlite3 import Cursor

from config.database import Database
from models.empleado import Empleado
from models.persona_dao import PersonaDAO
from models.validaciones_dao import (
    consultar, existe, fecha_a_texto, marcas, texto_a_fecha, validar_id, validar_no_existe,
)


class EmpleadoDAO:
    """
    Data Access Object para la entidad Empleado (hereda de Persona).
    Un empleado se guarda en dos tablas: persona (datos personales) y empleado (datos laborales).

    Al guardar, las relaciones solo se escriben si el otro lado ya existe en la base:
    - departamento: se guarda aquí si ya existe; si no, lo guarda DepartamentoDAO.crear.
    - proyectos: cada asignación se guarda aquí si el proyecto ya existe; si no, la guarda ProyectoDAO.crear.

    Al leer, cada objeto se construye una sola vez por consulta (caché), así el gerente de un
    departamento es el mismo objeto que el empleado que se pidió.
    """

    SQL_LECTURA = """
        SELECT e.id_empleado, e.id_persona, e.fecha_contrato, e.salario, e.estado,
               p.nombre, p.email, p.telefono, p.direccion
        FROM empleado e
        JOIN persona p ON p.id_persona = e.id_persona
    """

    @staticmethod
    def _cargar(id_empleado: str, cache: dict) -> Empleado | None:
        clave = ("empleado", id_empleado)
        if clave in cache:
            return cache[clave]
        filas = consultar(EmpleadoDAO.SQL_LECTURA + " WHERE e.id_empleado = ?", (id_empleado,))
        if not filas:
            return None
        fila = filas[0]
        empleado = Empleado(fila["id_persona"], fila["nombre"], fila["email"], fila["telefono"], fila["direccion"],
                            fila["id_empleado"],
                            texto_a_fecha(fila["fecha_contrato"], "fecha_contrato"),
                            fila["salario"])
        if fila["estado"] != "Activo":
            empleado.cambiar_estado(fila["estado"])
        cache[clave] = empleado          # se registra antes de completarlo: evita ciclos
        EmpleadoDAO._completar(empleado, cache)
        return empleado

    @staticmethod
    def _completar(empleado: Empleado, cache: dict) -> None:
        """Carga departamento, proyectos y registros del empleado (una sola vez)."""
        marca = ("completo", "empleado", empleado.id_empleado)
        if marca in cache:
            return
        cache[marca] = True

        # Importaciones locales: los DAO se referencian entre sí y así evitamos el ciclo.
        from models.departamento_dao import DepartamentoDAO
        from models.proyecto_dao import ProyectoDAO
        from models.registro_tiempo_dao import RegistroTiempoDAO

        id_depto = consultar(
            "SELECT id_departamento FROM empleado WHERE id_empleado = ?", (empleado.id_empleado,)
        )[0]["id_departamento"]
        # Si el departamento se está construyendo (este empleado es su gerente o está en
        # proceso), el propio departamento lo asigna al terminar.
        if id_depto is not None and ("en_construccion", "departamento", id_depto) not in cache:
            departamento = DepartamentoDAO._cargar(id_depto, cache)
            departamento.asignar_empleado(empleado)   # no hace nada si ya es miembro

        for fila in consultar("SELECT id_proyecto FROM empleado_proyecto WHERE id_empleado = ?",
                              (empleado.id_empleado,)):
            proyecto = ProyectoDAO._cargar(fila["id_proyecto"], cache)
            empleado.asignar_proyecto(proyecto)

        for fila in consultar("SELECT id_registro FROM registro_tiempo WHERE id_empleado = ?",
                              (empleado.id_empleado,)):
            RegistroTiempoDAO._cargar(fila["id_registro"], cache)   # se vincula solo

    @staticmethod
    def obtener_todos() -> list[Empleado]:
        empleados = []
        cache: dict = {}
        try:
            for fila in consultar("SELECT id_empleado FROM empleado"):
                empleados.append(EmpleadoDAO._cargar(fila["id_empleado"], cache))
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener empleados: {e}")
        return empleados

    @staticmethod
    def obtener_por_id(id_empleado: str) -> Empleado | None:
        try:
            return EmpleadoDAO._cargar(validar_id(id_empleado, "id_empleado"), {})
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al obtener el empleado: {e}")
            return None

    @staticmethod
    def buscar_por_nombre(texto: str) -> list[Empleado]:
        """Empleados cuyo nombre contiene el texto (no distingue mayúsculas en ASCII)."""
        empleados = []
        cache: dict = {}
        try:
            filas = consultar(
                "SELECT e.id_empleado FROM empleado e JOIN persona p ON p.id_persona = e.id_persona "
                "WHERE p.nombre LIKE ? ORDER BY p.nombre", (f"%{texto.strip()}%",))
            for fila in filas:
                empleados.append(EmpleadoDAO._cargar(fila["id_empleado"], cache))
        except (ValueError, TypeError, sqlite3.Error) as e:
            print(f"Error al buscar empleados: {e}")
        return empleados
    
    @staticmethod
    def crear(empleado: Empleado) -> bool:
        conn = Database().get_connection()
        try:
            validar_no_existe("empleado", "id_empleado", empleado.id_empleado, "id_empleado")
            validar_no_existe("empleado", "id_persona", empleado.id_persona, "id_persona")
            persona_nueva = not existe("persona", "id_persona", empleado.id_persona)

            depto = empleado.departamento
            id_depto = (depto.id_departamento
                        if depto is not None and existe("departamento", "id_departamento", depto.id_departamento)
                        else None)
            ids_proyectos = [p.id_proyecto for p in empleado.proyectos
                             if existe("proyecto", "id_proyecto", p.id_proyecto)]

            cursor: Cursor = conn.cursor()
            if persona_nueva:
                PersonaDAO._insertar(cursor, empleado)
            cursor.execute(
                "INSERT INTO empleado (id_empleado, id_persona, fecha_contrato, salario, estado, id_departamento) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (empleado.id_empleado, empleado.id_persona, fecha_a_texto(empleado.fecha_contrato),
                 empleado.salario, empleado.estado, id_depto)
            )
            for id_proyecto in ids_proyectos:
                cursor.execute(
                    "INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (?, ?)",
                    (empleado.id_empleado, id_proyecto)
                )
            conn.commit()
            return True
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al crear empleado en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar(empleado: Empleado) -> bool:
        conn = Database().get_connection()
        try:
            depto = empleado.departamento
            id_depto = (depto.id_departamento
                        if depto is not None and existe("departamento", "id_departamento", depto.id_departamento)
                        else None)
            ids_proyectos = [p.id_proyecto for p in empleado.proyectos
                             if existe("proyecto", "id_proyecto", p.id_proyecto)]

            cursor: Cursor = conn.cursor()
            cursor.execute(
                "UPDATE persona SET nombre = ?, email = ?, telefono = ?, direccion = ? WHERE id_persona = ?",
                (empleado.nombre, empleado.email, empleado.telefono, empleado.direccion, empleado.id_persona)
            )
            cursor.execute(
                "UPDATE empleado SET fecha_contrato = ?, salario = ?, estado = ?, id_departamento = ? "
                "WHERE id_empleado = ?",
                (fecha_a_texto(empleado.fecha_contrato), empleado.salario, empleado.estado,
                 id_depto, empleado.id_empleado)
            )
            actualizado = cursor.rowcount > 0

            # Sincroniza las asignaciones. Si se quita una que tiene registros, SQLite lo impide.
            if ids_proyectos:
                cursor.execute(
                    f"DELETE FROM empleado_proyecto WHERE id_empleado = ? AND id_proyecto NOT IN ({marcas(ids_proyectos)})",
                    (empleado.id_empleado, *ids_proyectos)
                )
            else:
                cursor.execute("DELETE FROM empleado_proyecto WHERE id_empleado = ?", (empleado.id_empleado,))
            for id_proyecto in ids_proyectos:
                cursor.execute(
                    "INSERT OR IGNORE INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (?, ?)",
                    (empleado.id_empleado, id_proyecto)
                )
            conn.commit()
            return actualizado
        except sqlite3.Error as e:
            print(f"Error al actualizar empleado: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_empleado: str) -> bool:
        """
        Borra la fila de empleado. Sus registros y asignaciones se borran en cascada.
        La persona se conserva. Falla si el empleado es gerente de un departamento (RESTRICT).
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM empleado WHERE id_empleado = ?", (validar_id(id_empleado, "id_empleado"),))
            conn.commit()
            return cursor.rowcount > 0
        except (ValueError, sqlite3.Error) as e:
            print(f"Error al eliminar empleado: {e}")
            return False
        finally:
            conn.close()
