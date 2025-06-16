from crud import CRUD
from maestro import Maestro

class InterfazMaestro:
    def __init__(self):
        self.crud = CRUD(Maestro, "maestros.json")

    def menu(self):
        while True:
            print("\n--- Menú de Maestros ---")
            print("1. Ver maestros")
            print("2. Agregar maestro")
            print("3. Actualizar maestro")
            print("4. Eliminar maestro")
            print("5. Salir")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._ver_maestros()
            elif opcion == "2":
                self._agregar_maestro()
            elif opcion == "3":
                self._actualizar_maestro()
            elif opcion == "4":
                self._eliminar_maestro()
            elif opcion == "5":
                print("Saliendo del menú de maestros.")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")

    def _ver_maestros(self):
        maestros = self.crud.leer_todos()
        print("\n=== Lista de Maestros ===")
        print(maestros if maestros and maestros.items else "No hay maestros registrados.")

    def _agregar_maestro(self):
        print("\n--- Agregar Maestro ---")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        try:
            edad = int(input("Edad: ").strip())
        except ValueError:
            print("Edad inválida.")
            return
        matricula = input("Matrícula: ").strip()
        especialidad = input("Especialidad: ").strip()
        nuevo_maestro = Maestro(nombre, apellido, edad, matricula, especialidad)
        if self.crud.crear(nuevo_maestro):
            print("Maestro añadido correctamente.")

    def _actualizar_maestro(self):
        maestros = self.crud.leer_todos()
        if not maestros or not maestros.items:
            print("No hay maestros para modificar.")
            return
        print("\n=== Maestros ===")
        for idx, maestro in enumerate(maestros.items):
            print(f"{idx+1}. {maestro.nombre} {maestro.apellido} - Matrícula: {maestro.matricula}")
        try:
            seleccion = int(input("Selecciona el número del maestro a modificar: ")) - 1
            if seleccion < 0 or seleccion >= len(maestros.items):
                print("Selección inválida.")
                return
        except ValueError:
            print("Entrada inválida.")
            return
        maestro = maestros.items[seleccion]
        print(f"Modificando a {maestro.nombre} {maestro.apellido}")
        nuevo_nombre = input(f"Nuevo nombre ({maestro.nombre}): ").strip() or maestro.nombre
        nuevo_apellido = input(f"Nuevo apellido ({maestro.apellido}): ").strip() or maestro.apellido
        try:
            nueva_edad = input(f"Nueva edad ({maestro.edad}): ").strip()
            nueva_edad = int(nueva_edad) if nueva_edad else maestro.edad
        except ValueError:
            print("Edad inválida.")
            return
        nueva_matricula = input(f"Nueva matrícula ({maestro.matricula}): ").strip() or maestro.matricula
        nueva_especialidad = input(f"Nueva especialidad ({maestro.especialidad}): ").strip() or maestro.especialidad
        nuevos_datos = {
            "nombre": nuevo_nombre,
            "apellido": nuevo_apellido,
            "edad": nueva_edad,
            "matricula": nueva_matricula,
            "especialidad": nueva_especialidad
        }
        self.crud.actualizar(seleccion, nuevos_datos)
        print("Maestro modificado correctamente.")

    def _eliminar_maestro(self):
        maestros = self.crud.leer_todos()
        if not maestros or not maestros.items:
            print("No hay maestros para eliminar.")
            return
        print("\n=== Maestros ===")
        for idx, maestro in enumerate(maestros.items):
            print(f"{idx+1}. {maestro.nombre} {maestro.apellido} - Matrícula: {maestro.matricula}")
        try:
            seleccion = int(input("Selecciona el número del maestro a eliminar: ")) - 1
            if seleccion < 0 or seleccion >= len(maestros.items):
                print("Selección inválida.")
                return
        except ValueError:
            print("Entrada inválida.")
            return
        self.crud.eliminar(seleccion)
        print("Maestro eliminado correctamente.")

if __name__ == "__main__":
    interfaz = InterfazMaestro()
    interfaz.menu()