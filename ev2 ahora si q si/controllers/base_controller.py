import sqlite3

from views.main_view import MainView


class ControladorBase:
    """
    Base común de los controladores: recorre un submenú y ejecuta la acción elegida.
    Cualquier error de validación o de base de datos se muestra y el menú sigue funcionando.
    """

    def __init__(self, titulo: str, acciones: list[tuple[str, callable]]):
        self.view = MainView()
        self.titulo = titulo
        self.acciones = acciones   # lista de (texto del menú, método a ejecutar)

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
