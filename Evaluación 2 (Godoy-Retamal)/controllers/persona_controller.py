from controllers.base_controller import ControladorBase
from models.persona import Persona
from models.persona_dao import PersonaDAO
from models.validaciones_dao import generar_id


class PersonaController(ControladorBase):
    

    def __init__(self):
        super().__init__("Personas", [
            ("Registrar persona", self._crear),
            ("Listar personas", self._listar),
            ("Actualizar persona", self._actualizar),
            ("Eliminar persona", self._eliminar),
        ])

    def _crear(self) -> None:
        v = self.view
        nombre = v.pedir_texto("Nombre")
        email = v.pedir_texto("Email")
        telefono = v.pedir_texto("Teléfono")
        direccion = v.pedir_texto("Dirección")
        persona = Persona(generar_id("P", "persona", "id_persona"), nombre, email, telefono, direccion)
        if PersonaDAO.crear(persona):
            v.mostrar_mensaje(f"Persona registrada con ID {persona.id_persona}.")
        else:
            v.mostrar_mensaje("No se pudo registrar la persona. Revise el mensaje anterior.")

    def _listar(self) -> None:
        lineas = [f"{p.id_persona} | {p.nombre} | {p.email} | {p.telefono} | {p.direccion}"
                  for p in PersonaDAO.obtener_todos()]
        self.view.mostrar_lista("Todas las personas", lineas)

    def _actualizar(self) -> None:
        v = self.view
        id_persona = v.pedir_texto("ID de la persona")
        persona = PersonaDAO.obtener_por_id(id_persona)
        if persona is None:
            v.mostrar_mensaje(f"No existe una persona con ID {id_persona}.")
            return
        nombre = v.pedir_texto("Nombre", actual=persona.nombre)
        email = v.pedir_texto("Email", actual=persona.email)
        telefono = v.pedir_texto("Teléfono", actual=persona.telefono)
        direccion = v.pedir_texto("Dirección", actual=persona.direccion)
        persona.actualizar_datos(nombre=nombre, email=email, telefono=telefono, direccion=direccion)
        if PersonaDAO.actualizar(persona):
            v.mostrar_mensaje("Persona actualizada.")
        else:
            v.mostrar_mensaje("No se pudo actualizar la persona.")

    def _eliminar(self) -> None:
        v = self.view
        id_persona = v.pedir_texto("ID de la persona a eliminar")
        if not v.confirmar(f"¿Eliminar a {id_persona}? Si es empleado, se borran también el empleado y sus registros"):
            return
        if PersonaDAO.eliminar(id_persona):
            v.mostrar_mensaje("Persona eliminada.")
        else:
            v.mostrar_mensaje("No se eliminó. Puede que no exista o que tenga un usuario asociado.")
