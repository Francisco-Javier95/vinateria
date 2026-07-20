class Categoria:

    # constructor
    def __init__(self, categoria_id, categoria_categoria, categoria_tipo, categoria_descripcion):
        self.categoria_id = categoria_id
        self.categoria_categoria = categoria_categoria
        self.categoria_tipo = categoria_tipo
        self.categoria_descripcion = categoria_descripcion

    def mostrar_info(self):
        return f"Nombre: {self.categoria_categoria}, Tipo: {self.categoria_tipo}, Descripción: {self.categoria_descripcion}"
    
class Categoria_eliminar:
    # Constructor
    def __init__(self, categoria_id):
        self.categoria_id = categoria_id

class Categoria_nombre:
    # Constructor
    def __init__(self, categoria_categoria):
        self.categoria_categoria = categoria_categoria