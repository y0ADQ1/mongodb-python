from crud import CRUD
from alumno import Alumno
from mongo_utils import MongoSyncUtils

class InterfazAlumno:
    def __init__(self):
        self.crud = CRUD(Alumno, "alumnos.json")
        self.offline_file = "alumnos_offline.json"
        self.alumnos_offline = MongoSyncUtils.cargar_offline(self.offline_file, Alumno)

    def menu(self):
        while True:
            print("\n--- Menú de Alumnos ---")
            print("1. Ver alumnos")
            print("2. Agregar alumno")
            print("3. Actualizar alumno")
            print("4. Eliminar alumno")
            print("5. Sincronizar datos offline a Mongo")
            print("6. Salir")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._ver_alumnos()
            elif opcion == "2":
                self._agregar_alumno()
            elif opcion == "3":
                self._actualizar_alumno()
            elif opcion == "4":
                self._eliminar_alumno()
            elif opcion == "5":
                MongoSyncUtils.sincronizar_offline(self.alumnos_offline, "python-mongo", "alumnos", self.offline_file)
            elif opcion == "6":
                print("Saliendo del menú de alumnos.")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")



                

    def _ver_alumnos(self):
        alumnos = self.crud.leer_todos()
        print("\n=== Lista de Alumnos ===")
        print(alumnos if alumnos and alumnos.items else "No hay alumnos registrados.")




    def _agregar_alumno(self):
        print("\n--- Agregar Alumno ---")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        try:

            edad = int(input("Edad: ").strip())
        except ValueError:
            print("Edad inválida.")
            return
        matricula = input("Matrícula: ").strip()
        try:
            promedio = float(input("Promedio: ").strip())
        except ValueError:
            print("Promedio inválido.")
            return
        nuevo_alumno = Alumno(nombre, apellido, edad, matricula, promedio)
        
        #con esto va aintentar guardar en Mongo directo si hay conexion
        if MongoSyncUtils.guardar_en_mongo_conexion(nuevo_alumno, "python-mongo", "alumnos"):
            print("Alumno agregado correctamente en Mongo")
        else: 
            #si no hay conexion guarda offline
            self.alumnos_offline.agregar(nuevo_alumno)
            MongoSyncUtils.guardar_offline(self.alumnos_offline, self.offline_file)
            print("No hubo conexion. El alumno se guardo offline")
        self.crud.crear(nuevo_alumno)








    def _actualizar_alumno(self):
        alumnos = self.crud.leer_todos()
        if not alumnos or not alumnos.items:
            print("No hay alumnos para modificar.")
            return
        print("\n=== Alumnos ===")
        for idx, alumno in enumerate(alumnos.items):
            print(f"{idx+1}. {alumno.nombre} {alumno.apellido} - Matrícula: {alumno.matricula}")
        try:
            seleccion = int(input("Selecciona el número del alumno a modificar: ")) - 1
            if seleccion < 0 or seleccion >= len(alumnos.items):
                print("Selección inválida.")
                return
        except ValueError:
            print("Entrada inválida.")
            return
        alumno = alumnos.items[seleccion]
        print(f"Modificando a {alumno.nombre} {alumno.apellido}")
        nuevo_nombre = input(f"Nuevo nombre ({alumno.nombre}): ").strip() or alumno.nombre
        nuevo_apellido = input(f"Nuevo apellido ({alumno.apellido}): ").strip() or alumno.apellido
        try:
            nueva_edad = input(f"Nueva edad ({alumno.edad}): ").strip()
            nueva_edad = int(nueva_edad) if nueva_edad else alumno.edad
        except ValueError:
            print("Edad inválida.")
            return
        nueva_matricula = input(f"Nueva matrícula ({alumno.matricula}): ").strip() or alumno.matricula
        try:
            nuevo_promedio = input(f"Nuevo promedio ({alumno.promedio}): ").strip()
            nuevo_promedio = float(nuevo_promedio) if nuevo_promedio else alumno.promedio
        except ValueError:
            print("Promedio inválido.")
            return
        nuevos_datos = {
            "nombre": nuevo_nombre,
            "apellido": nuevo_apellido,
            "edad": nueva_edad,
            "matricula": nueva_matricula,
            "promedio": nuevo_promedio
        }
        self.crud.actualizar(seleccion, nuevos_datos)
        print("Alumno modificado correctamente.")




    def _eliminar_alumno(self):
        alumnos = self.crud.leer_todos()
        if not alumnos or not alumnos.items:
            print("No hay alumnos para eliminar.")
            return
        print("\n=== Alumnos ===")
        for idx, alumno in enumerate(alumnos.items):
            print(f"{idx+1}. {alumno.nombre} {alumno.apellido} - Matrícula: {alumno.matricula}")
        try:
            seleccion = int(input("Selecciona el número del alumno a eliminar: ")) - 1
            if seleccion < 0 or seleccion >= len(alumnos.items):
                print("Selección inválida.")
                return
        except ValueError:
            print("Entrada inválida.")
            return
        self.crud.eliminar(seleccion)
        print("Alumno eliminado correctamente.")



if __name__ == "__main__":
    interfaz = InterfazAlumno()
    interfaz.menu()