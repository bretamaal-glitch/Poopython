from controllers.base_controller import ControladorBase
from models.empleado_dao import EmpleadoDAO
from models.registro_tiempo import RegistroTiempo
from models.registro_tiempo_dao import RegistroTiempoDAO
from models.validaciones_dao import generar_id


class RegistroTiempoController(ControladorBase):
    

    def __init__(self):
        super().__init__("Registros de tiempo", [
            ("Registrar horas", self._registrar),
            ("Listar todos los registros", self._listar),
            ("Listar registros de un empleado", self._listar_por_empleado),
            ("Actualizar registro", self._actualizar),
            ("Eliminar registro", self._eliminar),
        ])

    def _mostrar(self, titulo: str, registros: list[RegistroTiempo]) -> None:
        lineas = [
            f"{r.id_registro} | {r.fecha.strftime('%d-%m-%Y')} | {r.horas_trabajadas} h | "
            f"Empleado: {r.id_empleado} | Proyecto: {r.proyecto.id_proyecto} | {r.descripcion}"
            for r in registros
        ]
        self.view.mostrar_lista(titulo, lineas)

    def _registrar(self) -> None:
        v = self.view
        id_empleado = v.pedir_texto("ID del empleado")
        empleado = EmpleadoDAO.obtener_por_id(id_empleado)
        if empleado is None:
            v.mostrar_mensaje(f"No existe un empleado con ID {id_empleado}.")
            return
        if not empleado.proyectos:
            v.mostrar_mensaje("El empleado no está asignado a ningún proyecto.")
            return
        self._mostrar_proyectos(empleado)
        id_proyecto = v.pedir_texto("ID del proyecto")
        proyecto = next((p for p in empleado.proyectos if p.id_proyecto == id_proyecto.upper()), None)
        if proyecto is None:
            v.mostrar_mensaje("El empleado no está asignado a ese proyecto.")
            return
        fecha = v.pedir_fecha("Fecha del trabajo")
        horas = v.pedir_numero("Horas trabajadas (entre 0 y 24)", minimo=0, maximo=24)
        descripcion = v.pedir_texto("Descripción de las tareas")
        
        registro = empleado.registrar_horas(generar_id("R", "registro_tiempo", "id_registro"),
                                            fecha, horas, descripcion, proyecto)
        if RegistroTiempoDAO.crear(registro):
            v.mostrar_mensaje(f"Registro guardado con ID {registro.id_registro}.")
        else:
            v.mostrar_mensaje("No se pudo guardar el registro. Revise el mensaje anterior.")

    def _mostrar_proyectos(self, empleado) -> None:
        lineas = [f"{p.id_proyecto} | {p.nombre}" for p in empleado.proyectos]
        self.view.mostrar_lista("Proyectos asignados", lineas)

    def _listar(self) -> None:
        self._mostrar("Todos los registros", RegistroTiempoDAO.obtener_todos())

    def _listar_por_empleado(self) -> None:
        id_empleado = self.view.pedir_texto("ID del empleado")
        empleado = EmpleadoDAO.obtener_por_id(id_empleado)
        if empleado is None:
            self.view.mostrar_mensaje(f"No existe un empleado con ID {id_empleado}.")
            return
        self._mostrar(f"Registros de {empleado.nombre}", list(empleado.registros))

    def _actualizar(self) -> None:
        v = self.view
        id_registro = v.pedir_texto("ID del registro")
        registro = RegistroTiempoDAO.obtener_por_id(id_registro)
        if registro is None:
            v.mostrar_mensaje(f"No existe un registro con ID {id_registro}.")
            return
        fecha = v.pedir_fecha("Fecha", actual=registro.fecha)
        horas = v.pedir_numero("Horas trabajadas (entre 0 y 24)", minimo=0, maximo=24,
                               actual=registro.horas_trabajadas)
        descripcion = v.pedir_texto("Descripción", actual=registro.descripcion)
        if fecha is not None:
            registro.fecha = fecha
        if horas is not None:
            registro.horas_trabajadas = horas   
        if descripcion is not None:
            registro.descripcion = descripcion
        if RegistroTiempoDAO.actualizar(registro):
            v.mostrar_mensaje("Registro actualizado.")
        else:
            v.mostrar_mensaje("No se pudo actualizar el registro.")

    def _eliminar(self) -> None:
        id_registro = self.view.pedir_texto("ID del registro a eliminar")
        if not self.view.confirmar(f"¿Eliminar el registro {id_registro}?"):
            return
        if RegistroTiempoDAO.eliminar(id_registro):
            self.view.mostrar_mensaje("Registro eliminado.")
        else:
            self.view.mostrar_mensaje("No se eliminó. Puede que no exista.")
