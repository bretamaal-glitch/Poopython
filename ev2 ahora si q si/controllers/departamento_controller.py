from controllers.base_controller import ControladorBase
from models.departamento import Departamento
from models.departamento_dao import DepartamentoDAO
from models.empleado_dao import EmpleadoDAO
from models.validaciones_dao import generar_id


class DepartamentoController(ControladorBase):
    

    def __init__(self):
        super().__init__("Departamentos", [
            ("Crear departamento", self._crear),
            ("Listar departamentos", self._listar),
            ("Buscar por nombre", self._buscar),
            ("Actualizar departamento", self._actualizar),
            ("Eliminar departamento", self._eliminar),
            ("Ver empleados del departamento", self._ver_miembros),
        ])

    def _pedir_departamento(self) -> Departamento | None:
        id_departamento = self.view.pedir_texto("ID del departamento")
        departamento = DepartamentoDAO.obtener_por_id(id_departamento)
        if departamento is None:
            self.view.mostrar_mensaje(f"No existe un departamento con ID {id_departamento}.")
        return departamento

    def _crear(self) -> None:
        nombre = self.view.pedir_texto("Nombre del departamento")
        id_gerente = self.view.pedir_texto("ID del empleado gerente")
        gerente = EmpleadoDAO.obtener_por_id(id_gerente)
        if gerente is None:
            self.view.mostrar_mensaje(f"No existe un empleado con ID {id_gerente}.")
            return
        departamento = Departamento(generar_id("D", "departamento", "id_departamento"), nombre, gerente)
        if DepartamentoDAO.crear(departamento):
            self.view.mostrar_mensaje(f"Departamento creado con ID {departamento.id_departamento}.")
        else:
            self.view.mostrar_mensaje("No se pudo crear el departamento. Revise el mensaje anterior.")

    def _mostrar(self, titulo: str, departamentos: list[Departamento]) -> None:
        lineas = [
            f"{d.id_departamento} | {d.nombre} | Gerente: {d.gerente.nombre if d.gerente else 'Ninguno'} | "
            f"Empleados: {len(d.empleados)}"
            for d in departamentos
        ]
        self.view.mostrar_lista(titulo, lineas)

    def _listar(self) -> None:
        self._mostrar("Todos los departamentos", DepartamentoDAO.obtener_todos())

    def _buscar(self) -> None:
        texto = self.view.pedir_texto("Nombre a buscar")
        self._mostrar(f"Resultados para '{texto}'", DepartamentoDAO.buscar_por_nombre(texto))

    def _actualizar(self) -> None:
        departamento = self._pedir_departamento()
        if departamento is None:
            return
        nombre = self.view.pedir_texto("Nombre", actual=departamento.nombre)
        id_gerente = self.view.pedir_texto("ID del nuevo gerente",
                                           actual=departamento.gerente.id_empleado)
        if nombre is not None:
            departamento.nombre = nombre
        if id_gerente is not None and id_gerente.upper() != departamento.gerente.id_empleado:
            nuevo_gerente = EmpleadoDAO.obtener_por_id(id_gerente)
            if nuevo_gerente is None:
                self.view.mostrar_mensaje(f"No existe un empleado con ID {id_gerente}.")
                return
            departamento.gerente = nuevo_gerente   
        if DepartamentoDAO.actualizar(departamento):
            self.view.mostrar_mensaje("Departamento actualizado.")
        else:
            self.view.mostrar_mensaje("No se pudo actualizar el departamento.")

    def _eliminar(self) -> None:
        id_departamento = self.view.pedir_texto("ID del departamento a eliminar")
        if not self.view.confirmar(f"¿Eliminar el departamento {id_departamento}? Sus empleados quedan sin departamento"):
            return
        if DepartamentoDAO.eliminar(id_departamento):
            self.view.mostrar_mensaje("Departamento eliminado.")
        else:
            self.view.mostrar_mensaje("No se eliminó. Puede que no exista.")

    def _ver_miembros(self) -> None:
        departamento = self._pedir_departamento()
        if departamento is None:
            return
        lineas = [
            f"{e.id_empleado} | {e.nombre}" + (" (gerente)" if e is departamento.gerente else "")
            for e in departamento.empleados
        ]
        self.view.mostrar_lista(f"Empleados de {departamento.nombre}", lineas)
