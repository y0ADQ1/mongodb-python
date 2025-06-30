from alumno import Alumno
from arreglo import Arreglo
from maestro import Maestro
import os
import json

class Grupo(Arreglo):
    def __init__(self, nombre=None, maestro=None):
        #si no recibo el nombre ni el maestro, entonces va a ser un arreglo
        if nombre is None and maestro is None: 
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            #y si recibe nombre y maestro, entonces es un objeto o un grupo individual
            self.nombre = nombre
            self.maestro = maestro
            self.alumnos = Alumno()
            self.es_arreglo = False

    def to_json(self, archivo):
        import json
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in self.items], f, indent=4, ensure_ascii=False)

    def read_json(self):
        #aqui leo el archivo jason y convierto los objetos desde el diccionario/lista
        with open("grupos.json", 'r') as file:
            data = json.load(file)
            return self._dict_to_object(data)

    def _dict_to_object(self, data):
        #aqui convierto un diccionario o una lista de diccionarios a objetos osea el grupo/maestro/alumno
        if not data:
            return None

        if isinstance(data, list):
            #si es una lista, entonces creo un arreglo de grupos
            grupo_arreglo = Grupo()
            for item in data:
                grupo = grupo_arreglo._dict_to_object(item)                
                grupo_arreglo.agregar(grupo)
            return grupo_arreglo
        else:
            #si es un diccionario, entonces se crea un grupo individual
            maestro_data = data.get('maestro')
            maestro = None
            if maestro_data:
                maestro = Maestro(
                    maestro_data['nombre'],
                    maestro_data['apellido'],
                    maestro_data['edad'],
                    maestro_data['matricula'],
                    maestro_data['especialidad']
                )
            
            grupo = Grupo(data['nombre'], maestro)
            
            alumnos_data = data.get('alumnos', [])
            if alumnos_data:
                alumnos = Alumno()
                alumnos._dict_to_object(alumnos_data)
                """
                if isinstance(alumnos_data, list):
                    for alumno_data in alumnos_data:
                        alumno = Alumno(
                            alumno_data['nombre'],
                            alumno_data['apellido'],
                            alumno_data['edad'],
                            alumno_data['matricula'],
                            alumno_data['promedio']
                        )
                        alumnos.agregar(alumno)
                """
            print("len(alumnos_data)>0",len(alumnos_data)>0,"alumnos_data:",alumnos_data)
            #si hay alumnos, entonces los convierto a objetos Alumno y los asigno al grupo
            if len(alumnos_data)>0:
                        alumnos=Alumno()
                        alumnos=alumnos._dict_to_object(alumnos_data)
                        grupo.alumnos=alumnos
                        grupo.alumnos = alumnos
            
            return grupo

    def to_dict(self):
        #convierte el grupo o el arreglo de grupos a diccionario/lista de diccionarios
        if self.es_arreglo:
                return  [item.to_dict() for item in self.items] if self.items else []
        return {
            'tipo': 'grupo','nombre': self.nombre,
            'maestro': self.maestro.to_dict()if self.maestro 
              else None,'alumnos': self.alumnos.to_dict()
        }

    def asignar_maestro(self, maestro):
        #asigna un maestro al grupo
        self.maestro = maestro

    def cambiarNombre(self, nombre):
        #cambia el nombre del grupo
        self.nombre = nombre

    def __str__(self):
        #y ya con esto hago la representacion con tecto del grupo o el arreglo de grupos
        if self.es_arreglo:
            return f"Total de grupos: {len(self.items)}"

        maestro_info = f"{self.maestro.nombre} {self.maestro.apellido}" if self.maestro else "Falta asignar"

        return (
            f"Grupo: {self.nombre}\n"
            f"Maestro: {maestro_info}\n"
            f"Total de alumnos: {str(self.alumnos)}\n"
        )


if __name__ == "__main__":
    """
    ALUMNO1 = Alumno("Juan", "Deras", 19, "23170072", 8)
    ALUMNO2 = Alumno("Jesus", "De la rosa", 19, "23170119", 10)
    ALUMNO3 = Alumno("Emilio", "Olvera", 21, "23170120", 9)
    ALUMNO4 = Alumno("Aza", "Garcia", 19, "23170121", 10)
    ALUMNO5 = Alumno("Saul", "Sanchez", 20, "23170122", 9.9)

    MAESTRO1 = Maestro("Ramiro", "Esquivel", 40, "1", "Android")
    MAESTRO2 = Maestro("Adrian", "Burciaga", 40, "2", "iOS")

    GRUPO1 = Grupo("Desarrollo Movil", MAESTRO1)
    GRUPO1.alumnos.agregar(ALUMNO1, ALUMNO2, ALUMNO3)

    GRUPO2 = Grupo("Desarrollo iOS", MAESTRO2)
    GRUPO2.alumnos.agregar(ALUMNO4, ALUMNO5)

    grupos = Grupo()
    grupos.agregar(GRUPO1, GRUPO2) 
    
    grupos.to_json()

    
    print("\n=== Grupos Recuperados ===")
    grupo_recuperado = Grupo().read_json()
    if grupo_recuperado.es_arreglo:
        for g in grupo_recuperado.items:
            print(f"\nNombre: {g.nombre}")
            print(f"Maestro: {g.maestro.nombre} {g.maestro.apellido}")
            print("Alumnos:")
            for alumno in g.alumnos.items:
                print(f"- {alumno.nombre} {alumno.matricula}")
    else:
        print(f"\nNombre: {grupo_recuperado.nombre}")
        print(f"Maestro: {grupo_recuperado.maestro.nombre} {grupo_recuperado.maestro.apellido}")
        print("Alumnos:")
        for alumno in grupo_recuperado.alumnos.items:
            print(f"- {alumno.nombre} {alumno.matricula}")"""
    grupo = Grupo()
    grupo_recuperado = grupo.read_json()
    grupo = grupo_recuperado
    grupo.to_json()

  
  