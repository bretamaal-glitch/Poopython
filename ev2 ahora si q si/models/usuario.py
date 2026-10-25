from models.validaciones import validar_texto
from models.persona import Persona


class Usuario:
    
    ROLES: dict[str, set[str]] = {
        "administrador": {"consultar", "crear", "editar", "eliminar"},
        "empleado": {"consultar"},
    }
    LONGITUD_MINIMA_CLAVE = 8
    ITERACIONES_HASH = 200_000

    def __init__(self, id_usuario: str, nombre_usuario: str, contrasena: str,
                 rol: str, persona: Persona):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.rol = rol
        self.persona = persona
        self.contrasena = contrasena


    @property
    def id_usuario(self) -> str:
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, id_usuario: str) -> None:
        self._id_usuario = validar_texto(id_usuario, "id_usuario")

    @property
    def nombre_usuario(self) -> str:
        return self._nombre_usuario

    @nombre_usuario.setter
    def nombre_usuario(self, nombre_usuario: str) -> None:
        self._nombre_usuario = validar_texto(nombre_usuario, "nombre_usuario")

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, rol: str) -> None:
        if rol not in self.ROLES:
            opciones = ", ".join(self.ROLES)
            raise ValueError(f"Rol '{rol}' no válido. Opciones permitidas: {opciones}.")
        self._rol = rol

    @property
    def persona(self) -> Persona:
        return self._persona

    @persona.setter
    def persona(self, persona: Persona) -> None:
        if not isinstance(persona, Persona):
            raise TypeError("La persona debe ser una instancia de la clase Persona.")
        self._persona = persona

    @classmethod
    def _validar_clave(cls, clave: str) -> str:
        if not isinstance(clave, str) or len(clave) < cls.LONGITUD_MINIMA_CLAVE:
            raise ValueError(
                f"La contraseña debe tener al menos {cls.LONGITUD_MINIMA_CLAVE} caracteres.")
        return clave

    def autenticar(self, clave: str) -> bool:
        if not isinstance(clave, str):
            return False
        return self.contrasena == clave

    def verificar_permiso(self, permiso: str) -> bool:
        return permiso in self.ROLES[self.rol]

    def __str__(self) -> str:
        return (f"Usuario | ID: {self.id_usuario} | Nombre: {self.nombre_usuario} | "
                f"Rol: {self.rol} | Persona: {self.persona.nombre}")

    def __repr__(self) -> str:
        return (f"Usuario(id_usuario='{self.id_usuario}', nombre_usuario='{self.nombre_usuario}', "
                f"rol='{self.rol}', persona={repr(self.persona)})")
