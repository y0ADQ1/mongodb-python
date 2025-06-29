from grupo import Grupo
from maestro import Maestro
from interfaz_maestro import InterfazMaestro
from interfaz_alumno import InterfazAlumno
import json
import os

class InterfazGrupo:
    def __init__(self, grupos=None, archivo="grupos.json"):
        self.archivo = archivo
        self.guardar = False

        # Cargar grupos desde objeto o archivo, o crear vacío
        if grupos is not None and hasattr(grupos, 'items') and len(grupos.items) > 0:
            self.grupos = grupos
            print("Usando clase Grupo.")
        elif archivo and os.path.exists(archivo):
            print(f"Cargando grupos desde archivo '{archivo}'.")
            self.grupos = Grupo().read_json()
            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.grupos = Grupo()

        self.interfaz_maestro = InterfazMaestro()
        self.interfaz_alumno = InterfazAlumno()

    def menu(self):
        while True:
            print("\n--- Menú de Grupos ---")
            print("1. Mostrar grupos")
            print("2. Agregar grupo")
            print("3. Eliminar grupo")
            print("4. Actualizar grupo")
            print("5. Salir")

            opcion = input("Seleccione una opción: ").strip()
            if opcion == "1":
                self.mostrar_grupos()
            elif opcion == "2":
                self.agregar_grupo()
            elif opcion == "3":
                self.eliminar_grupo()
            elif opcion == "4":
                self.actualizar_grupo()
            elif opcion == "5":
                print("Saliendo.")
                if self.guardar:
                    self.grupos.to_json(self.archivo)
                break
            else:
                print("Opción no válida.")

    def mostrar_grupos(self):
        if not self.grupos.items:
            print("No hay grupos registrados.")
            return
        for idx, grupo in enumerate(self.grupos.items):
            print(f"\n--- Grupo #{idx} ---")
            print(grupo)

    def agregar_grupo(self):
        nombre = input("Nombre del grupo: ").strip()

        print("\n--- Asignar maestro al grupo ---")
        self.interfaz_maestro._agregar_maestro()
        if hasattr(self.interfaz_maestro.crud.leer_todos(), 'items') and len(self.interfaz_maestro.crud.leer_todos().items) > 0:
            maestro = self.interfaz_maestro.crud.leer_todos().items[-1]
        else:
            print("No se pudo crear el maestro.")
            return

        grupo = Grupo(nombre, maestro)

        agregar_mas = input("¿Deseas agregar alumnos? (s/n): ").lower()
        if agregar_mas == "s":
            
            interfaz_alumno=InterfazAlumno(grupo.alumnos)
            
            grupo.alumnos = interfaz_alumno.alumnos

        self.grupos.agregar(grupo)

        if self.guardar:
            self.grupos.to_json(self.archivo)
            print("Grupo agregado y guardado en archivo.")
        else:
            print("Grupo agregado (modo objeto).")

    def eliminar_grupo(self):
        if not self.grupos.items:
            print("No hay grupos para eliminar.")
            return
        try:
            for idx, grupo in enumerate(self.grupos.items):
                print(f"{idx}. {grupo.nombre}")
            indice = int(input("Índice del grupo a eliminar: "))
            if self.grupos.eliminar(indice=indice):
                if self.guardar:
                    self.grupos.to_json(self.archivo)
                print("Grupo eliminado.")
            else:
                print("No se pudo eliminar el grupo.")
        except ValueError:
            print("Índice inválido.")

    def actualizar_grupo(self):
        if not self.grupos.items:
            print("No hay grupos para actualizar.")
            return
        try:
            for idx, grupo in enumerate(self.grupos.items):
                print(f"{idx}. {grupo.nombre}")
            indice = int(input("Índice del grupo a actualizar: "))
            if 0 <= indice < len(self.grupos.items):
                grupo = self.grupos.items[indice]
                print("Deja en blanco si no deseas cambiar un campo.")

                nombre = input(f"Nombre ({grupo.nombre}): ").strip() or grupo.nombre
                grupo.nombre = nombre

                actualizar_maestro = input("¿Deseas actualizar al maestro? (s/n): ").lower()
                if actualizar_maestro == "s":
                    print("\n--- Actualizando maestro ---")
                    self.interfaz_maestro._actualizar_maestro()
                    if hasattr(self.interfaz_maestro.crud.leer_todos(), 'items') and len(self.interfaz_maestro.crud.leer_todos().items) > 0:
                        grupo.maestro = self.interfaz_maestro.crud.leer_todos().items[-1]
                    else:
                        print("No se pudo actualizar el maestro, manteniendo el original.")

                actualizar_alumnos = input("¿Deseas gestionar los alumnos del grupo? (s/n): ").lower()
                if actualizar_alumnos == "s":
                    print("\n--- Gestionando alumnos del grupo ---")
                    self.interfaz_alumno._actualizar_alumno()
                    if hasattr(self.interfaz_alumno.crud.leer_todos(), 'items') and len(self.interfaz_alumno.crud.leer_todos().items) > 0:
                        grupo.alumnos = self.interfaz_alumno.crud.leer_todos()

                if self.guardar:
                    self.grupos.to_json(self.archivo)
                print("Grupo actualizado.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

if __name__ == "__main__":
    interfaz = InterfazGrupo()
    interfaz.menu()