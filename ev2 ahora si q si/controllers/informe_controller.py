from controllers.base_controller import ControladorBase
from models.departamento_dao import DepartamentoDAO
from models.empleado_dao import EmpleadoDAO
from models.informe import Informe
from models.proyecto_dao import ProyectoDAO
from models.registro_tiempo_dao import RegistroTiempoDAO
from models.validaciones_dao import generar_id


class InformeController(ControladorBase):
    """Genera informes con los datos del sistema y los exporta a CSV (abre en Excel)."""

    TIPOS = [
        ("Empleados", "empleado"),
        ("Proyectos", "proyecto"),
        ("Departamentos", "departamento"),
        ("Registros de tiempo", "registro_tiempo"),
    ]

    def __init__(self):
        super().__init__("Informes", [
            ("Generar informe", self._generar),
        ])

    def _generar(self) -> None:
        v = self.view
        v.mostrar_lista("Tipo de informe", [f"{i}. {nombre}" for i, (nombre, _) in enumerate(self.TIPOS, 1)])
        opcion = v.pedir_entero("Seleccione el tipo", 1, len(self.TIPOS))
        tipo = self.TIPOS[opcion - 1][1]

        informe = Informe(generar_id("I", "informe", "id_informe"), tipo)
        if tipo == "empleado":
            informe.generar(empleados=EmpleadoDAO.obtener_todos())
        elif tipo == "proyecto":
            informe.generar(proyectos=ProyectoDAO.obtener_todos())
        elif tipo == "departamento":
            informe.generar(departamentos=DepartamentoDAO.obtener_todos())
        else:
            informe.generar(registros=RegistroTiempoDAO.obtener_todos())

        ruta = v.pedir_texto("Archivo de salida", actual=f"informe_{tipo}.csv") or f"informe_{tipo}.csv"
        informe.exportar(ruta)
        v.mostrar_mensaje(f"Informe guardado en {ruta}.")
