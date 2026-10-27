from controllers.departamento_controller import DepartamentoController
from controllers.empleado_controller import EmpleadoController
from controllers.informe_controller import InformeController
from controllers.proyecto_controller import ProyectoController
from controllers.registro_tiempo_controller import RegistroTiempoController
from views.main_view import MainView


class MainController:
    

    def __init__(self):
        self.view = MainView()
        self.empleado_controller = EmpleadoController()
        self.departamento_controller = DepartamentoController()
        self.proyecto_controller = ProyectoController()
        self.registro_controller = RegistroTiempoController()
        self.informe_controller = InformeController()

    def ejecutar(self) -> None:
        controladores = {
            1: self.empleado_controller,
            2: self.departamento_controller,
            3: self.proyecto_controller,
            4: self.registro_controller,
            5: self.informe_controller,
        }
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 0:
                self.view.mostrar_mensaje("Gracias por usar el sistema de EcoTech Solutions. ¡Hasta luego!")
                break
            controladores[opcion].ejecutar()
