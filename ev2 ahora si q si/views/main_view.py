from datetime import date

class MainView:
    """
    Interfaz de consola. Muestra menús y pide datos. Cada entrada se valida
    y se vuelve a pedir si no es correcta, para que el programa no se interrumpa.
    """

    MENU_PRINCIPAL = [
        "Empleados",
        "Departamentos",
        "Proyectos",
        "Registros de tiempo",
        "Informes",
    ]

    def mostrar_menu(self) -> int:
        print("\n=== Sistema de Gestión EcoTech Solutions ===")
        for i, nombre in enumerate(self.MENU_PRINCIPAL, start=1):
            print(f"{i}. {nombre}")
        print("0. Salir")
        return self.pedir_entero("Seleccione una opción", 0, len(self.MENU_PRINCIPAL))

    def mostrar_submenu(self, titulo: str, opciones: list[str]) -> int:
        print(f"\n--- {titulo} ---")
        for i, nombre in enumerate(opciones, start=1):
            print(f"{i}. {nombre}")
        print("0. Volver")
        return self.pedir_entero("Seleccione una opción", 0, len(opciones))

    def mostrar_mensaje(self, mensaje: str) -> None:
        print(mensaje)

    def mostrar_lista(self, titulo: str, lineas: list[str]) -> None:
        print(f"\n{titulo}")
        if not lineas:
            print("  (sin resultados)")
        for linea in lineas:
            print(f"  - {linea}")

    def confirmar(self, pregunta: str) -> bool:
        return input(f"{pregunta} (s/n): ").strip().lower() == "s"

    def pedir_texto(self, etiqueta: str, actual: str | None = None) -> str | None:
        """
        Pide un texto obligatorio. Si se pasa 'actual', un Enter vacío devuelve None
        (significa que se conserva el valor actual).
        """
        sufijo = f" [{actual}]" if actual is not None else ""
        while True:
            valor = input(f"{etiqueta}{sufijo}: ").strip()
            if valor:
                return valor
            if actual is not None:
                return None
            print("  Este campo es obligatorio.")

    def pedir_fecha(self, etiqueta: str, actual: date | None = None) -> date | None:
        while True:
            texto = self.pedir_texto(f"{etiqueta} (AAAA-MM-DD)",
                                     actual=actual.isoformat() if actual else None)
            if texto is None:
                return None
            try:
                return date.fromisoformat(texto)
            except ValueError:
                print("  Fecha no válida. Use el formato AAAA-MM-DD.")

    def pedir_numero(self, etiqueta: str, minimo: float | None = None,
                     maximo: float | None = None, actual: float | None = None) -> float | None:
        while True:
            texto = self.pedir_texto(etiqueta, actual=str(actual) if actual is not None else None)
            if texto is None:
                return None
            try:
                valor = float(texto.replace(",", "."))
            except ValueError:
                print("  Ingrese un número válido.")
                continue
            if minimo is not None and valor < minimo:
                print(f"  El valor debe ser mayor o igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  El valor debe ser menor o igual a {maximo}.")
                continue
            return valor

    def pedir_entero(self, etiqueta: str, minimo: int, maximo: int) -> int:
        while True:
            texto = input(f"{etiqueta} ({minimo}-{maximo}): ").strip()
            if texto.isdigit() and minimo <= int(texto) <= maximo:
                return int(texto)
            print("  Opción no válida. Intente nuevamente.")
