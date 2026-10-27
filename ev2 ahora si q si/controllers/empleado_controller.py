from controllers.base_controller import ControladorBase
from models.departamento_dao import DepartamentoDAO
from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from models.proyecto_dao import ProyectoDAO
from models.validaciones_dao import generar_id


class EmpleadoController(ControladorBase):
    

    def __init__(self):
        super().__init__("Empleados", [
            ("Registrar empleado", self._crear),
            ("Listar empleados", self._listar),
            ("Buscar por nombre", self._buscar),
            ("Actualizar empleado", self._actualizar),
            ("Eliminar empleado", self._eliminar),
            ("Asignar a departamento", self._asignar_departamento),
            ("Asignar a proyecto", self._asignar_proyecto),
            ("Desasignar de proyecto", self._desasignar_proyecto),
        ])

    def _pedir_empleado(self) -> Empleado | None:
        id_empleado = self.view.pedir_texto("ID del empleado")
        empleado = EmpleadoDAO.obtener_por_id(id_empleado)
        if empleado is None:
            self.view.mostrar_mensaje(f"No existe un empleado con ID {id_empleado}.")
        return empleado

    def _crear(self) -> None:
        v = self.view
        nombre = v.pedir_texto("Nombre")
        email = v.pedir_texto("Email")
        telefono = v.pedir_texto("Teléfono")
        direccion = v.pedir_texto("Dirección")
        fecha = v.pedir_fecha("Fecha de inicio de contrato")
        salario = v.pedir_numero("Salario", minimo=0)
        empleado = Empleado(generar_id("P", "persona", "id_persona"), nombre, email, telefono,
                            direccion, generar_id("E", "empleado", "id_empleado"), fecha, salario)
        if EmpleadoDAO.crear(empleado):
            v.mostrar_mensaje(f"Empleado registrado con ID {empleado.id_empleado}.")
        else:
            v.mostrar_mensaje("No se pudo registrar el empleado. Revise el mensaje anterior.")

    def _mostrar(self, titulo: str, empleados: list[Empleado]) -> None:
        lineas = [
            f"{e.id_empleado} | {e.nombre} | {e.email} | {e.estado} | "
            f"Depto: {e.departamento.nombre if e.departamento else 'Sin departamento'} | "
            f"Proyectos: {len(e.proyectos)}"
            for e in empleados
        ]
        self.view.mostrar_lista(titulo, lineas)

    def _listar(self) -> None:
        self._mostrar("Todos los empleados", EmpleadoDAO.obtener_todos())

    def _buscar(self) -> None:
        texto = self.view.pedir_texto("Nombre a buscar")
        self._mostrar(f"Resultados para '{texto}'", EmpleadoDAO.buscar_por_nombre(texto))

    def _actualizar(self) -> None:
        v = self.view
        empleado = self._pedir_empleado()
        if empleado is None:
            return
        nombre = v.pedir_texto("Nombre", actual=empleado.nombre)
        email = v.pedir_texto("Email", actual=empleado.email)
        telefono = v.pedir_texto("Teléfono", actual=empleado.telefono)
        direccion = v.pedir_texto("Dirección", actual=empleado.direccion)
        fecha = v.pedir_fecha("Fecha de inicio de contrato", actual=empleado.fecha_contrato)
        salario = v.pedir_numero("Salario", minimo=0, actual=empleado.salario)
        estado = v.pedir_texto("Estado (Activo/Inactivo)", actual=empleado.estado)

        empleado.actualizar_datos(nombre=nombre, email=email, telefono=telefono, direccion=direccion)
        if fecha is not None:
            empleado.fecha_contrato = fecha
        if salario is not None:
            empleado.salario = salario
        if estado is not None:
            empleado.cambiar_estado(estado)

        if EmpleadoDAO.actualizar(empleado):
            v.mostrar_mensaje("Empleado actualizado.")
        else:
            v.mostrar_mensaje("No se pudo actualizar el empleado.")

    def _eliminar(self) -> None:
        id_empleado = self.view.pedir_texto("ID del empleado a eliminar")
        if not self.view.confirmar(f"¿Eliminar al empleado {id_empleado}? Se borran sus registros de tiempo"):
            return
        if EmpleadoDAO.eliminar(id_empleado):
            self.view.mostrar_mensaje("Empleado eliminado.")
        else:
            self.view.mostrar_mensaje("No se eliminó. Puede que no exista o que sea gerente de un departamento.")

    def _asignar_departamento(self) -> None:
        empleado = self._pedir_empleado()
        if empleado is None:
            return
        id_departamento = self.view.pedir_texto("ID del departamento")
        departamento = DepartamentoDAO.obtener_por_id(id_departamento)
        if departamento is None:
            self.view.mostrar_mensaje(f"No existe un departamento con ID {id_departamento}.")
            return
        departamento.asignar_empleado(empleado)   
        if DepartamentoDAO.actualizar(departamento):
            self.view.mostrar_mensaje(f"Empleado asignado a {departamento.nombre}.")
        else:
            self.view.mostrar_mensaje("No se pudo realizar la asignación.")

    def _asignar_proyecto(self) -> None:
        empleado = self._pedir_empleado()
        if empleado is None:
            return
        id_proyecto = self.view.pedir_texto("ID del proyecto")
        proyecto = ProyectoDAO.obtener_por_id(id_proyecto)
        if proyecto is None:
            self.view.mostrar_mensaje(f"No existe un proyecto con ID {id_proyecto}.")
            return
        empleado.asignar_proyecto(proyecto)
        if EmpleadoDAO.actualizar(empleado):
            self.view.mostrar_mensaje(f"Empleado asignado al proyecto {proyecto.nombre}.")
        else:
            self.view.mostrar_mensaje("No se pudo realizar la asignación.")

    def _desasignar_proyecto(self) -> None:
        empleado = self._pedir_empleado()
        if empleado is None:
            return
        id_proyecto = self.view.pedir_texto("ID del proyecto")
        proyecto = next((p for p in empleado.proyectos if p.id_proyecto == id_proyecto.upper()), None)
        if proyecto is None:
            self.view.mostrar_mensaje("El empleado no está asignado a ese proyecto.")
            return
        empleado.desasignar_proyecto(proyecto)  
        if EmpleadoDAO.actualizar(empleado):
            self.view.mostrar_mensaje(f"Empleado desasignado de {proyecto.nombre}.")
        else:
            self.view.mostrar_mensaje("No se pudo realizar la desasignación.")
