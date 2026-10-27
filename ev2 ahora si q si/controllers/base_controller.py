import sqlite3

from views.main_view import MainView


class ControladorBase:
    

    def __init__(self, titulo: str, acciones: list[tuple[str, callable]]):
        self.view = MainView()
        self.titulo = titulo
        self.acciones = acciones   

    def ejecutar(self) -> None:
        textos = [texto for texto, _ in self.acciones]
        while True:
            opcion = self.view.mostrar_submenu(self.titulo, textos)
            if opcion == 0:
                break
            _, accion = self.acciones[opcion - 1]
            try:
                accion()
            except (ValueError, TypeError) as e:
                self.view.mostrar_mensaje(f"Dato no válido: {e}")
            except sqlite3.Error as e:
                self.view.mostrar_mensaje(f"Error de base de datos: {e}")
