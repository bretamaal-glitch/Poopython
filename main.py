from paciente import Paciente
from typing import Optional
pacientes: list[Paciente] = [Paciente("12345678-9", "Robert Pattinson", 40, "Fonasa"), Paciente("98765432-1", "Kristen Stewart", 33, "Isapre")]
PREVISION_ACTUALIZADA = "Previsión actualizada"

def leer_numero(mensaje: str) -> int:
    while True:
        try:
            numero = int(input(mensaje))
            return numero
        except ValueError:
            print("Error: Debe ingresar un número entero.")
            

def menu():
    print("="*20)
    print("Menú Clínica")
    print("1. Agregar paciente")
    print("2. Editar paciente")
    print("3. Eliminar paciente")
    print("4. Mostrar un paciente")
    print("5. Mostrar todos los pacientes")
    print("0. Salir")
    op=leer_numero("Ingrese una opción: ")
    print("="*20)
    return op

def agregar_paciente()-> None:
    rut = input("Ingrese el RUT del paciente: ")
    nombre = input("Ingrese el nombre del paciente: ")
    edad = leer_numero("Ingrese la edad del paciente: ")
    print("Tipo de previsión del paciente:")
    print("1. Fonasa")
    print("2. Isapre")
    print("3. Particular")
    print("4. Otro")
    op=leer_numero("Seleccione una previsión del paciente: ")
    if op == 1:
        prevision = "Fonasa"
    elif op == 2:
        prevision = "Isapre"
    elif op == 3:
        prevision = "Particular"
    elif op == 4:
        prevision = "Otro"
    else:
        print("Opción de previsión no válida.")
        return

    paciente = Paciente(rut, nombre, edad, prevision)
    pacientes.append(paciente)
    print("Paciente agregado exitosamente.")
    print(f"Total de pacientes: {len(pacientes)}")

def imprimir_pacientes() -> None:
    if len(pacientes) == 0:
        print("No hay pacientes registrados")
    else: 
        for paciente in pacientes:
            print(paciente)
            print("-"*20)

def buscar_paciente() -> Optional[Paciente]:
    rut = input("Ingrese el RUT del paciente: ")
    for p in pacientes:
        if p.rut == rut:
            return p
    return None


def imprimir_paciente() -> None:
    paciente=buscar_paciente()
    if paciente:
        print(paciente)
    else:
        print("No se pudo mostrar el paciente.")

def eliminar_paciente() -> None:
    paciente = buscar_paciente()
    if paciente:
        pacientes.remove(paciente)
        print("Paciente eliminado")
    else:
        print("No se encontró el paciente.")

def editar_paciente() -> None:
    paciente=buscar_paciente()
    if paciente:
        print(paciente)
        print("Menú de edición:")
        print("1. Editar nombre")
        print("2. Editar edad")
        print("3. Editar previsión")
        print("0. Salir")
        op=leer_numero("Ingrese una opción: ")
        if op==1:
            nuevo_nombre=input("Ingrese el nuevo nombre: ")
            paciente.nombre=nuevo_nombre
            print("Nombre actualizado")
        elif op==2:
            nueva_edad=leer_numero("Ingrese la nueva edad: ")
            paciente.edad=nueva_edad
            print("Edad actualizada")
        elif op==3:
            print("Tipos de previsión")
            print("1. Fonasa")
            print("2. Isapre")
            print("3. Particular")
            print("4. Otro")
            op=leer_numero("Seleccione una previsión del paciente: ")
            if op == 1:
                paciente.prevision = "Fonasa"
                print(PREVISION_ACTUALIZADA)
            elif op == 2:
                paciente.prevision = "Isapre"
                print(PREVISION_ACTUALIZADA)
            elif op == 3:
                paciente.prevision = "Particular"
                print(PREVISION_ACTUALIZADA)
            elif op == 4:
                paciente.prevision = "Otro"
                print(PREVISION_ACTUALIZADA)
            else:
                print("Opción de previsión no válida.")              
    else: 
        print("No se encontró el paciente.")


def main():
    while True:
        opcion = menu()
        if opcion == 1:
            agregar_paciente()
        elif opcion == 2:
            print("Editar paciente")
            editar_paciente()
        elif opcion == 3:
            print("Eliminar paciente")
            eliminar_paciente()
        elif opcion == 4:
            print("Mostrar un paciente")
            imprimir_paciente()
        elif opcion == 5:
            print("Mostrar todos los pacientes")
            imprimir_pacientes()
        elif opcion == 0:
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, ingrese una opción válida.")





if __name__ == "__main__":
    main()

