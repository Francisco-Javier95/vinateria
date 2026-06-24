class Proveedor:

    # constructor
    def __init__(self, proveedor_id, proveedor_proveedor, proveedor_aPaterno, proveedor_aMaterno, proveedor_telefono, proveedor_direccion, proveedor_correo):
        self.proveedor_id = proveedor_id
        self.proveedor_proveedor = proveedor_proveedor
        self.proveedor_aPaterno = proveedor_aPaterno
        self.proveedor_aMaterno = proveedor_aMaterno
        self.proveedor_telefono = proveedor_telefono
        self.proveedor_direccion = proveedor_direccion
        self.proveedor_correo = proveedor_correo

    def mostrar_info (self):
        return f"Nombre: {self.proveedor_proveedor}, Apellido paterno: {self.proveedor_aPaterno}, Apellido materno: {self.proveedor_aMaterno}, Telefóno: {self.proveedor_telefono}, Dirección: {self.proveedor_direccion}, Correo: {self.proveedor_correo}"