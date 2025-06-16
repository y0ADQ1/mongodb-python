class CRUD:
    def __init__(self, clase, archivo):
        # clase es la clase sobre la que se harán las operaciones (por ejemplo, Alumno)
        self.clase = clase
        self.archivo = archivo

    def crear(self, objeto):
        # Agrega un objeto al arreglo y lo guarda en el archivo json
        arreglo = self.clase().read_json(self.archivo)
        if arreglo is None or not hasattr(arreglo, 'items'):
            arreglo = self.clase()
        arreglo.agregar(objeto)
        arreglo.to_json(self.archivo)
        return True

    def leer_todos(self):
        # Lee todos los objetos del archivo JSON
        arreglo = self.clase().read_json(self.archivo)
        return arreglo

    def actualizar(self, indice, nuevos_datos):
        # Actualiza el objeto en la posición 'indice' con 'nuevos_datos'
        arreglo = self.clase().read_json(self.archivo)
        if not arreglo or not arreglo.items or indice < 0 or indice >= len(arreglo.items):
            return False
        for key, value in nuevos_datos.items():
            setattr(arreglo.items[indice], key, value)
        arreglo.to_json(self.archivo)
        return True

    def eliminar(self, indice):
        # Elimina el objeto en la posición 'indice'
        arreglo = self.clase().read_json(self.archivo)
        if not arreglo or not arreglo.items or indice < 0 or indice >= len(arreglo.items):
            return False
        arreglo.items.pop(indice)
        arreglo.to_json(self.archivo)
        return True