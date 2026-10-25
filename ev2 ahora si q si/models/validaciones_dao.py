"""
Validaciones y utilidades comunes de los DAO.

- Las validaciones comprueban los datos antes de escribir, para dar un mensaje claro
  en lugar de un error genérico de SQLite.
- consultar() ejecuta lecturas y cierra la conexión.
- Solo se usan las tablas y columnas de las listas permitidas, así que un nombre de
  tabla nunca viene de un dato del usuario.
"""
from __future__ import annotations

from datetime import date

from config.database import Database
from models.validaciones import validar_texto

TABLAS_PERMITIDAS = {
    "persona", "usuario", "empleado", "departamento", "proyecto",
    "empleado_proyecto", "registro_tiempo", "informe",
}
COLUMNAS_PERMITIDAS = {
    "id_persona", "id_usuario", "nombre_usuario", "id_empleado", "id_departamento",
    "id_proyecto", "id_registro", "id_informe",
}


def validar_id(valor, campo: str) -> str:
    """Devuelve el id sin espacios y en mayúsculas, igual que normalizan los modelos."""
    return validar_texto(valor, campo).upper()


def fecha_a_texto(fecha: date) -> str:
    """Convierte una fecha a texto ISO (AAAA-MM-DD) para guardarla en SQLite."""
    return fecha.isoformat()


def texto_a_fecha(texto: str, campo: str) -> date:
    """Convierte el texto ISO de la base de datos en un objeto date."""
    try:
        return date.fromisoformat(texto)
    except (TypeError, ValueError):
        raise ValueError(f"'{campo}' no es una fecha válida: {texto!r}.")


def marcas(valores) -> str:
    """Genera los signos de interrogación para una cláusula IN, por ejemplo '?, ?, ?'."""
    return ", ".join("?" for _ in valores)


def consultar(sql: str, params: tuple = ()) -> list:
    """Ejecuta una consulta de lectura y devuelve todas sus filas, cerrando la conexión."""
    conn = Database().get_connection()
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def existe(tabla: str, columna: str, valor) -> bool:
    """Indica si hay al menos un registro con ese valor en esa columna."""
    if tabla not in TABLAS_PERMITIDAS or columna not in COLUMNAS_PERMITIDAS:
        raise ValueError(f"Tabla o columna no permitida: {tabla}.{columna}")
    return len(consultar(f"SELECT 1 FROM {tabla} WHERE {columna} = ? LIMIT 1", (valor,))) > 0


def validar_existe(tabla: str, columna: str, valor, campo: str) -> None:
    if not existe(tabla, columna, valor):
        raise ValueError(f"'{campo}' no existe: no hay ningún registro con {columna} = '{valor}' en {tabla}.")


def validar_no_existe(tabla: str, columna: str, valor, campo: str) -> None:
    if existe(tabla, columna, valor):
        raise ValueError(f"'{campo}' ya existe: hay un registro con {columna} = '{valor}' en {tabla}.")


def generar_id(prefijo: str, tabla: str, columna: str) -> str:
    """Devuelve un id nuevo y libre con formato PREFIJO-0001 (asignación automática)."""
    if tabla not in TABLAS_PERMITIDAS or columna not in COLUMNAS_PERMITIDAS:
        raise ValueError(f"Tabla o columna no permitida: {tabla}.{columna}")
    n = len(consultar(f"SELECT {columna} FROM {tabla}")) + 1
    while existe(tabla, columna, f"{prefijo}-{n:04d}"):
        n += 1
    return f"{prefijo}-{n:04d}"


def validar_asignacion(id_empleado: str, id_proyecto: str) -> None:
    """Un registro de tiempo solo puede existir si el empleado está asignado al proyecto."""
    filas = consultar(
        "SELECT 1 FROM empleado_proyecto WHERE id_empleado = ? AND id_proyecto = ?",
        (id_empleado, id_proyecto)
    )
    if not filas:
        raise ValueError(f"El empleado {id_empleado} no está asignado al proyecto {id_proyecto}.")
