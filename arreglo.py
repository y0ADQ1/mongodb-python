class Arreglo:
    def __init__(self):
        self.items = []
        self.es_arreglo = True
    
    def agregar (self, *items):
        for item in items:
            self.items.append(item)
    def eliminar (self, item=None, indice=None):
        try:
            if indice is not None:
                 del self.items.remove[item]
            else:
                self.items.remove(item)
            return True
        except (IndexError, ValueError):
            return False
    
    def actualizar (self, objeto, atributo, nuevo_valor):
        for elem in self.items:
            if elem == objeto:
                if hasattr(elem, atributo):
                    setattr(elem, atributo, nuevo_valor)
                    return True
        return False
    
    def __str__(self):
        if not self.items:
            return "Arreglo vacío"
        return str(len(self.items))