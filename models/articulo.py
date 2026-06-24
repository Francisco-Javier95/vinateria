class Articulo:
    # constructor
    def __init__(self, articulo_id, articulo_articulo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor):
        self.articulo_id = articulo_id
        self.articulo_articulo = articulo_articulo
        self.articulo_categoria = articulo_categoria
        self.articulo_imagen = articulo_imagen
        self.articulo_precio = articulo_precio
        self.articulo_stock = articulo_stock
        self.articulo_proveedor = articulo_proveedor

    def mostrar_info (self):
        return f"Nombre: {self.articulo_articulo}, Categoría: {self.articulo_categoria}, Imagen: {self.articulo_imagen}, Precio: {self.articulo_precio}, Stock: {self.articulo_stock}, Proveedor: {self.articulo_proveedor}"
    
class Articulo_eliminar:
    # Constructor
    def __init__(self, articulo_id):
        self.articulo_id = articulo_id