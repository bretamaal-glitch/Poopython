import sqlite3

from config.database import Database
from controllers.main_controller import MainController


def main() -> None:
    print("Inicializando sistema...")
    try:
        Database().init_db()
    except sqlite3.Error as e:
        print(f"No se pudo preparar la base de datos: {e}")
        return

    app = MainController()
    try:
        app.ejecutar()
    except (KeyboardInterrupt, EOFError):
        print("\nSesión finalizada.")


if __name__ == "__main__":
    main()
