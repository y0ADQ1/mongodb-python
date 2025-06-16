from arreglo import Arreglo
import os
import json

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, especialidad=None):
        # Si no recibo datos, es un arreglo de maestros
        if nombre is None and apellido is None and edad is None and matricula is None and especialidad is None:
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            # Si recibo datos, es un maestro individual
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.especialidad = especialidad
            self.es_arreglo = False

    def to_json(self, archivo="maestros.json"):
        # Guarda el maestro o arreglo de maestros en un archivo JSON
        with open(archivo, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    def read_json(self, archivo="maestros.json"):
        # Lee el archivo JSON y convierte los datos a objetos usando _dict_to_object
        if not os.path.exists(archivo):
            return Maestro()
        with open(archivo, 'r') as file:
            data = json.load(file)
            return self._dict_to_object(data)

    def _dict_to_object(self, data):
        """
        Convierte un diccionario o una lista de diccionarios a objetos Maestro.
        Si data es una lista, crea un arreglo de maestros.
        Si data es un diccionario, crea un maestro individual.
        """
        if not data:
            return Maestro()
        if isinstance(data, list):
            maestro_arreglo = Maestro()
            for item in data:
                maestro = self._dict_to_object(item)
                maestro_arreglo.agregar(maestro)
            return maestro_arreglo
        else:
            return Maestro(
                data.get('nombre'),
                data.get('apellido'),
                data.get('edad'),
                data.get('matricula'),
                data.get('especialidad')
            )

    def to_dict(self):
        """
        Convierte el maestro o el arreglo de maestros a diccionario/lista de diccionarios.
        Si es arreglo, regresa una lista de diccionarios.
        Si es maestro, regresa un diccionario con sus atributos.
        """
        if hasattr(self, 'es_arreglo') and self.es_arreglo:
            return [item.to_dict() for item in self.items] if self.items else []
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'matricula': self.matricula,
            'especialidad': self.especialidad
        }

    def cambiarEspecialidad(self, especialidad):
        # Cambia la especialidad del maestro
        self.especialidad = especialidad

    def __str__(self):
        # Representación en texto del maestro o el arreglo de maestros
        if hasattr(self, 'es_arreglo') and self.es_arreglo:
            if not self.items:
                return "No hay maestros."
            return "\n".join(str(maestro) for maestro in self.items)
        return (f"Maestro: {self.nombre} {self.apellido}, {self.edad} años, "
                f"Matrícula: {self.matricula}, Especialidad: {self.especialidad}")

if __name__ == "__main__":
    # Ejemplo de uso: guardar y recuperar maestros desde JSON
    MAESTRO1 = Maestro("Ramiro", "Esquivel", 40, "1", "Android")
    MAESTRO2 = Maestro("Jesus", "Burciaga", 40, "2", "iOS")
    MAESTRO3 = Maestro("Juan", "Perez", 20, "23170120", "Web")

    print("\n=== Lista de Maestros ===")
    maestros = Maestro()
    maestros.agregar(MAESTRO1, MAESTRO2, MAESTRO3)
    print(maestros)

    maestros.to_json()

    print("\n=== Maestros Recuperados ===")
    maestros_recuperados = Maestro().read_json()
    print(maestros_recuperados)