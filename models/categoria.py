class Categoria:

    # constructor
    def __init__(self, categoria_id, categoria_nombre, categoria_tipo, categoria_descripcion):
        self.categoria_id = categoria_id
        self.categoria_nombre = categoria_nombre
        self.categoria_tipo = categoria_tipo
        self.categoria_descripcion = categoria_descripcion

    def mostrar_info(self):
        return f"Nombre: {self.categoria_nombre}, Tipo: {self.categoria_tipo}, Descripción: {self.categoria_descripcion}"