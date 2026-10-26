from controllers.base_controller import ControladorBase
from models.proyecto import Proyecto
from models.proyecto_dao import ProyectoDAO
from models.validaciones_dao import generar_id


class ProyectoController(ControladorBase):
    """Operaciones de la pantalla de proyectos (CRUD, búsqueda y empleados asignados)."""

    def __init__(self):
        super().__init__("Proyectos", [
            ("Crear proyecto", self._crear),
            ("Listar proyectos", self._listar),
            ("Buscar por nombre", self._buscar),
            ("Actualizar proyecto", self._actualizar),
            ("Eliminar proyecto", self._eliminar),
            ("Ver empleados del proyecto", self._ver_empleados),
        ])

    def _pedir_proyecto(self) -> Proyecto | None:
        id_proyecto = self.view.pedir_texto("ID del proyecto")
        proyecto = ProyectoDAO.obtener_por_id(id_proyecto)
        if proyecto is None:
            self.view.mostrar_mensaje(f"No existe un proyecto con ID {id_proyecto}.")
        return proyecto

    def _crear(self) -> None:
        v = self.view
        nombre = v.pedir_texto("Nombre")
        descripcion = v.pedir_texto("Descripción")
        fecha = v.pedir_fecha("Fecha de inicio")
        proyecto = Proyecto(generar_id("PR", "proyecto", "id_proyecto"), nombre, descripcion, fecha)
        if ProyectoDAO.crear(proyecto):
            v.mostrar_mensaje(f"Proyecto creado con ID {proyecto.id_proyecto}.")
        else:
            v.mostrar_mensaje("No se pudo crear el proyecto. Revise el mensaje anterior.")

    def _mostrar(self, titulo: str, proyectos: list[Proyecto]) -> None:
        lineas = [
            f"{p.id_proyecto} | {p.nombre} | Inicio: {p.fecha_inicio.isoformat()} | Empleados: {len(p.empleados)}"
            for p in proyectos
        ]
        self.view.mostrar_lista(titulo, lineas)

    def _listar(self) -> None:
        self._mostrar("Todos los proyectos", ProyectoDAO.obtener_todos())

    def _buscar(self) -> None:
        texto = self.view.pedir_texto("Nombre a buscar")
        self._mostrar(f"Resultados para '{texto}'", ProyectoDAO.buscar_por_nombre(texto))

    def _actualizar(self) -> None:
        v = self.view
        proyecto = self._pedir_proyecto()
        if proyecto is None:
            return
        nombre = v.pedir_texto("Nombre", actual=proyecto.nombre)
        descripcion = v.pedir_texto("Descripción", actual=proyecto.descripcion)
        fecha = v.pedir_fecha("Fecha de inicio", actual=proyecto.fecha_inicio)
        if nombre is not None:
            proyecto.nombre = nombre
        if descripcion is not None:
            proyecto.descripcion = descripcion
        if fecha is not None:
            proyecto.fecha_inicio = fecha
        if ProyectoDAO.actualizar(proyecto):
            v.mostrar_mensaje("Proyecto actualizado.")
        else:
            v.mostrar_mensaje("No se pudo actualizar el proyecto.")

    def _eliminar(self) -> None:
        id_proyecto = self.view.pedir_texto("ID del proyecto a eliminar")
        if not self.view.confirmar(f"¿Eliminar el proyecto {id_proyecto}?"):
            return
        if ProyectoDAO.eliminar(id_proyecto):
            self.view.mostrar_mensaje("Proyecto eliminado.")
        else:
            self.view.mostrar_mensaje("No se eliminó. Puede que no exista o que tenga registros de tiempo.")

    def _ver_empleados(self) -> None:
        proyecto = self._pedir_proyecto()
        if proyecto is None:
            return
        lineas = [f"{e.id_empleado} | {e.nombre}" for e in proyecto.empleados]
        self.view.mostrar_lista(f"Empleados en {proyecto.nombre}", lineas)
