from datetime import date


def validar_texto(valor, campo: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"'{campo}' no puede estar vacío.")
    return valor.strip()


def validar_fecha(valor, campo: str) -> date:
    if not isinstance(valor, date):
        raise TypeError(f"'{campo}' debe ser una fecha (datetime.date).")
    return valor


def validar_numero(valor, campo: str) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"'{campo}' debe ser un número.")
    return float(valor)
