import sqlite3
from sqlite3 import Connection, Cursor

class Database:
    """clase que gestiona la conexion a la base de datos implementando el patron singleton
    para evitar multiples instancias inncesesarias"""
    _instance = None
    _db_path = "clinica.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def get_connection(self) -> Connection:
        """ retorna una conexion a la base de datos"""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row  # permite acceder a las columnas por nombre
        return conn

    def init_db(self) -> None:
        """inicializa la base de datos creando las tablas necesarias"""
        conn = self.get_connection()
        try:
            cursor: Cursor = conn.cursor()

            # tabla departamento
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS departamento(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    piso INTEGER NOT NULL
                )
                """
            )

            # tabla paciente
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS paciente(
                    rut TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    edad INTEGER NOT NULL,
                    prevision TEXT NOT NULL,
                    id_departamento INTEGER,
                    FOREIGN KEY (id_departamento) REFERENCES departamento(id) ON DELETE SET NULL
                )
                """
            )

            conn.commit()
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
        finally:
            conn.close()




    