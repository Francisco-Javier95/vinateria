class Proveedor:

    # constructor
    def __init__(self, proveedor_id, proveedor_proveedor, proveedor_apaterno, proveedor_amaterno, proveedor_telefono, proveedor_direccion, proveedor_correo):
        self.proveedor_id = proveedor_id
        self.proveedor_proveedor = proveedor_proveedor
        self.proveedor_apaterno = proveedor_apaterno
        self.proveedor_amaterno = proveedor_amaterno
        self.proveedor_telefono = proveedor_telefono
        self.proveedor_direccion = proveedor_direccion
        self.proveedor_correo = proveedor_correo

    def mostrar_info (self):
        return f"Nombre: {self.proveedor_proveedor}, Apellido paterno: {self.proveedor_apaterno}, Apellido materno: {self.proveedor_amaterno}, Telefóno: {self.proveedor_telefono}, Dirección: {self.proveedor_direccion}, Correo: {self.proveedor_correo}"
    
class Proveedor_eliminar:
    # Constructor
    def __init__(self, proveedor_id):
        self.proveedor_id = proveedor_id

class Proveedor_nombre:
    # Constructor
    def __init__(self, proveedor_proveedor):
        self.proveedor_proveedor = proveedor_proveedor