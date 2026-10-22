import sqlite3
from sqlite3 import Connection, Cursor

class Database:
    _instance = None
    _db_path = "ecotech.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def get_connection(self) -> Connection:
        
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row  
    
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self) -> None:
        conn = self.get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS persona (
                    id_persona TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    telefono TEXT NOT NULL
                )
            """)

        
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario TEXT PRIMARY KEY,
                    nombre_usuario TEXT NOT NULL UNIQUE,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL CHECK (rol IN ('administrador', 'empleado')),
                    id_persona TEXT NOT NULL UNIQUE,
                    FOREIGN KEY(id_persona) REFERENCES persona(id_persona) ON DELETE RESTRICT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleado (
                    id_empleado TEXT PRIMARY KEY,
                    id_persona TEXT NOT NULL UNIQUE,
                    fecha_contrato TEXT NOT NULL,
                    salario REAL NOT NULL CHECK (salario >= 0),
                    estado TEXT NOT NULL DEFAULT 'Activo' CHECK (estado IN ('Activo', 'Inactivo')),
                    id_departamento TEXT,
                    FOREIGN KEY(id_persona) REFERENCES persona(id_persona) ON DELETE CASCADE,
                    FOREIGN KEY(id_departamento) REFERENCES departamento(id_departamento) ON DELETE SET NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamento (
                    id_departamento TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    id_gerente TEXT NOT NULL,
                    FOREIGN KEY(id_gerente) REFERENCES empleado(id_empleado) ON DELETE RESTRICT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proyecto (
                    id_proyecto TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    fecha_inicio TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleado_proyecto (
                    id_empleado TEXT NOT NULL,
                    id_proyecto TEXT NOT NULL,
                    PRIMARY KEY (id_empleado, id_proyecto),
                    FOREIGN KEY(id_empleado) REFERENCES empleado(id_empleado) ON DELETE CASCADE,
                    FOREIGN KEY(id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS registro_tiempo (
                    id_registro TEXT PRIMARY KEY,
                    id_empleado TEXT NOT NULL,
                    id_proyecto TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    horas_trabajadas REAL NOT NULL CHECK (horas_trabajadas > 0 AND horas_trabajadas <= 24),
                    FOREIGN KEY(id_empleado) REFERENCES empleado(id_empleado) ON DELETE CASCADE,
                    FOREIGN KEY(id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE RESTRICT,
                    FOREIGN KEY(id_empleado, id_proyecto)
                        REFERENCES empleado_proyecto(id_empleado, id_proyecto)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS informe (
                    id_informe TEXT PRIMARY KEY,
                    tipo TEXT NOT NULL CHECK (tipo IN ('empleado', 'proyecto', 'registro_tiempo')),
                    formato TEXT NOT NULL DEFAULT 'PDF',
                    contenido TEXT
                )
            """)

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_empleado_departamento ON empleado(id_departamento)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_registro_empleado ON registro_tiempo(id_empleado)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_registro_proyecto ON registro_tiempo(id_proyecto)")

            conn.commit()
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    db = Database()
    db.init_db()
    print("Base de datos inicializada correctamente.")