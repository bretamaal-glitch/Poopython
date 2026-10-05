from paciente import Paciente
from typing import Optional
from departamento import Departamento
from typing import Optional

departamentos: list[Departamento] = [Departamento(1, "Cardiología", 2), Departamento(2, "Neurología", 3)]
pacientes: list[Paciente] = [Paciente("12345678-9", "Robert Pattinson", 40, "Fonasa"), Paciente("98765432-1", "Kristen Stewart", 33, "Isapre")]
PREVISION_ACTUALIZADA = "Previsión actualizada"
MENSAJE_OPCION = "Ingrese una opción: "
OPCION_SALIR = "0. Salir"

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
    print("6. Agregar departamento")
    print("7. Editar departamento")
    print("8. Eliminar departamento")
    print("9. Mostrar un departamento")
    print("10. Mostrar todos los departamentos")
    print(OPCION_SALIR)
    op=leer_numero(MENSAJE_OPCION)
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

    try:
        paciente = Paciente(rut, nombre, edad, prevision)
    except (ValueError, TypeError) as e:
        print(f"Error al agregar paciente: {e}")
        return
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
    paciente = buscar_paciente()
    if not paciente:
        print("No se encontró el paciente.")
        return

    print(paciente)
    print("Menú de edición:")
    print("1. Editar nombre")
    print("2. Editar edad")
    print("3. Editar previsión")
    print(OPCION_SALIR)
    op = leer_numero(MENSAJE_OPCION)

    if op == 1:
        nuevo_nombre = input("Ingrese el nuevo nombre: ")
        try:
            paciente.nombre = nuevo_nombre
        except ValueError as e:
            print(f"Error al actualizar el nombre: {e}")
            return
        print("Nombre actualizado")
        return

    if op == 2:
        nueva_edad = leer_numero("Ingrese la nueva edad: ")
        try:
            paciente.edad = nueva_edad
        except (ValueError, TypeError) as e:
            print(f"Error al actualizar la edad: {e}")
            return
        print("Edad actualizada")
        return

    if op == 3:
        print("Tipos de previsión")
        print("1. Fonasa")
        print("2. Isapre")
        print("3. Particular")
        print("4. Otro")

        opciones_prevision = {
            1: "Fonasa",
            2: "Isapre",
            3: "Particular",
            4: "Otro",
        }
        op_prevision = leer_numero("Seleccione una previsión del paciente: ")

        if op_prevision in opciones_prevision:
            paciente.prevision = opciones_prevision[op_prevision]
            print(PREVISION_ACTUALIZADA)
            return

        print("Opción de previsión no válida.")


def agregar_departamento()-> None:
    id_departamento = leer_numero("Ingrese el ID del departamento: ")
    nombre = input("Ingrese el nombre del departamento: ")
    piso = leer_numero("Ingrese el piso del departamento: ")
    departamento = Departamento(id_departamento, nombre, piso)
    departamentos.append(departamento)
    print("Departamento agregado exitosamente.")

def imprimir_departamentos() -> None:
    if len(departamentos) == 0:
        print("No hay departamentos registrados")
    else: 
        for departamento in departamentos:
            print(departamento)
            print("-"*20)

def buscar_departamento() -> Optional[Departamento]:
    id_departamento = leer_numero("Ingrese el ID del departamento: ")
    for d in departamentos:
        if d.id_departamento == id_departamento:
            return d
    return None


def imprimir_departamento() -> None:
    departamento=buscar_departamento()
    if departamento:
        print(departamento)
    else:
        print("No se pudo mostrar el departamento.")

def eliminar_departamento() -> None:
    departamento= buscar_departamento()
    if departamento:
        departamentos.remove(departamento)
        print("Departamento eliminado")
    else:
        print("No se encontró el departamento")

def editar_departamento() -> None:
    departamento=buscar_departamento()
    if departamento:
        print(departamento)
        print("Menú de edición")
        print("1. Editar nombre")
        print("2. Editar piso")
        print(OPCION_SALIR)
        op=leer_numero("Ingrese una opción: ")
        if op==1:
            nuevo_nombre=input("Ingrese el nuevo nombre: ")
            departamento.nombre=nuevo_nombre
            print("Nombre actualizado")
        elif op==2:
            nuevo_piso=leer_numero("Ingrese el nuevo piso: ")
            departamento.piso=nuevo_piso
            print("Piso actualizado")

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
        elif opcion == 6:
            print("Agregar departamento")
            agregar_departamento()
        elif opcion == 7:
            print("Editar departamento")
            editar_departamento()
        elif opcion == 8:
            print("Eliminar departamento")
            eliminar_departamento()
        elif opcion == 9:
            print("Mostrar un departamento")
            imprimir_departamento()
        elif opcion == 10:
            print("Mostrar todos los departamentos")
            imprimir_departamentos()
        elif opcion == 0:
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, ingrese una opción válida.")


if __name__ == "__main__":
    main()





