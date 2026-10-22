import re
"""preguntarle al profe si esto es necesario junto con IF TYPE_CHECKING"""
from validaciones import validar_texto


class Persona:
    """
    Modelo (DTO) para la entidad Persona.
    Tabla: persona (id_persona, nombre, email, telefono).
    """
    PATRON_EMAIL = re.compile(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")
    PATRON_TELEFONO = re.compile(r"^\+?[0-9 ]{7,15}$")

    def __init__(self, id_persona: str, nombre: str, email: str, telefono: str):
        self.id_persona = id_persona
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def id_persona(self) -> str:
        return self._id_persona

    @id_persona.setter
    def id_persona(self, id_persona: str) -> None:
        self._id_persona = validar_texto(id_persona, "id_persona").upper()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        self._nombre = nombre.strip().title()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        email = validar_texto(email, "email").lower()
        if not self.PATRON_EMAIL.match(email):
            raise ValueError("El email no tiene un formato válido.")
        self._email = email

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, telefono: str) -> None:
        telefono = validar_texto(telefono, "telefono")
        if not self.PATRON_TELEFONO.match(telefono):
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos y puede empezar con +.")
        self._telefono = telefono

    def actualizar_datos(self, nombre: str | None = None, email: str | None = None,
                         telefono: str | None = None) -> None:
        """Actualiza solo los datos que se entregan."""
        if nombre is not None:
            self.nombre = nombre
        if email is not None:
            self.email = email
        if telefono is not None:
            self.telefono = telefono

    def __str__(self) -> str:
        return (f"Persona | ID: {self.id_persona} | Nombre: {self.nombre} | "
                f"Email: {self.email} | Teléfono: {self.telefono}")

    def __repr__(self) -> str:
        return (f"Persona(id_persona='{self.id_persona}', nombre='{self.nombre}', "
                f"email='{self.email}', telefono='{self.telefono}')")
