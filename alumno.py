from arreglo import Arreglo
import json
import os

class Alumno(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, promedio=None):
        # Si no recibo datos, es un arreglo de alumnos
        if nombre is None and apellido is None and edad is None and matricula is None and promedio is None:
            super().__init__()
            self.es_arreglo = True
        else:
            # Si recibo datos, es un alumno individual
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.promedio = promedio
            self.es_arreglo = False

    def to_json(self, archivo="alumnos.json"):
        with open(archivo, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    def read_json(self, archivo="alumnos.json"):
        if not os.path.exists(archivo):
            return Alumno()
        with open(archivo, 'r') as file:
            data = json.load(file)
            return self._dict_to_object(data)

    def _dict_to_object(self, data):
        """
        Convierte un diccionario o una lista de diccionarios a objetos Alumno.
        Si data es una lista, crea un arreglo de alumnos.
        Si data es un diccionario, crea un alumno individual.
        """
        if not data:
            return Alumno()
        if isinstance(data, list):
            alumno_arreglo = Alumno()
            for item in data:
                alumno = self._dict_to_object(item)
                alumno_arreglo.agregar(alumno)
            return alumno_arreglo
        else:
            return Alumno(
                data.get('nombre'),
                data.get('apellido'),
                data.get('edad'),
                data.get('matricula'),
                data.get('promedio')
            )

    def to_dict(self):
        """
        Convierte el alumno o el arreglo de alumnos a diccionario/lista de diccionarios.
        Si es arreglo, regresa una lista de diccionarios.
        Si es alumno, regresa un diccionario con sus atributos.
        """
        if hasattr(self, 'es_arreglo') and self.es_arreglo:
            return [item.to_dict() for item in self.items] if self.items else []
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'matricula': self.matricula,
            'promedio': self.promedio
        }

    def actualizarPromedio(self, promedio):
        # Actualiza el promedio del alumno
        self.promedio = promedio

    def __str__(self):
        # Representación en texto del alumno o el arreglo de alumnos
        if hasattr(self, 'es_arreglo') and self.es_arreglo:
            if not self.items:
                return "No hay alumnos."
            return "\n".join(str(alumno) for alumno in self.items)
        return (f"Alumno: {self.nombre} {self.apellido}, {self.edad} años, "
                f"Matrícula: {self.matricula}, Promedio: {self.promedio}")