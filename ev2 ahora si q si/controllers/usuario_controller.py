from controllers.base_controller import ControladorBase
from models.persona_dao import PersonaDAO
from models.usuario import Usuario
from models.usuario_dao import UsuarioDAO
from models.validaciones_dao import generar_id


class UsuarioController(ControladorBase):
    

    def __init__(self):
        super().__init__("Usuarios", [
            ("Crear usuario", self._crear),
            ("Listar usuarios", self._listar),
            ("Actualizar usuario", self._actualizar),
            ("Eliminar usuario", self._eliminar),
        ])

    def _crear(self) -> None:
        v = self.view
        id_persona = v.pedir_texto("ID de la persona")
        persona = PersonaDAO.obtener_por_id(id_persona)
        if persona is None:
            v.mostrar_mensaje("No existe esa persona. Regístrela primero en la sección Personas.")
            return
        nombre_usuario = v.pedir_texto("Nombre de usuario")
        contrasena = v.pedir_texto("Contraseña")
        rol = v.pedir_texto("Rol (administrador / empleado)")
        usuario = Usuario(generar_id("U", "usuario", "id_usuario"), nombre_usuario, "", rol, persona)
        usuario.establecer_contrasena(contrasena)
        if UsuarioDAO.crear(usuario):
            v.mostrar_mensaje(f"Usuario creado con ID {usuario.id_usuario}.")
        else:
            v.mostrar_mensaje("No se pudo crear el usuario. Revise el mensaje anterior.")

    def _listar(self) -> None:
        lineas = [f"{u.id_usuario} | {u.nombre_usuario} | {u.rol} | Persona: {u.persona.nombre}"
                  for u in UsuarioDAO.obtener_todos()]
        self.view.mostrar_lista("Todos los usuarios", lineas)

    def _actualizar(self) -> None:
        v = self.view
        id_usuario = v.pedir_texto("ID del usuario")
        usuario = UsuarioDAO.obtener_por_id(id_usuario)
        if usuario is None:
            v.mostrar_mensaje(f"No existe un usuario con ID {id_usuario}.")
            return
        nombre_usuario = v.pedir_texto("Nombre de usuario", actual=usuario.nombre_usuario)
        contrasena = v.pedir_texto("Nueva contraseña", actual="(sin cambios)")
        rol = v.pedir_texto("Rol (administrador / empleado)", actual=usuario.rol)
        if nombre_usuario is not None:
            usuario.nombre_usuario = nombre_usuario
        if contrasena is not None:
            usuario.establecer_contrasena(contrasena)
        if rol is not None:
            usuario.rol = rol
        if UsuarioDAO.actualizar(usuario):
            v.mostrar_mensaje("Usuario actualizado.")
        else:
            v.mostrar_mensaje("No se pudo actualizar el usuario.")

    def _eliminar(self) -> None:
        v = self.view
        id_usuario = v.pedir_texto("ID del usuario a eliminar")
        if not v.confirmar(f"¿Eliminar el usuario {id_usuario}? La persona se conserva"):
            return
        if UsuarioDAO.eliminar(id_usuario):
            v.mostrar_mensaje("Usuario eliminado.")
        else:
            v.mostrar_mensaje("No se eliminó. Puede que no exista.")
