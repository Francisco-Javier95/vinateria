class Venta:
    # Constructor
    def __init__(self, venta_id, venta_venta, venta_fecha, venta_ganancia, venta_usuario, venta_articulo, venta_estado):
        self.venta_id = venta_id
        self.venta_venta = venta_venta
        self.venta_fecha = venta_fecha
        self.venta_ganancia = venta_ganancia
        self.venta_usuario = venta_usuario
        self.venta_articulo = venta_articulo  # String con formato '{1,2,3}'
        self.venta_estado = venta_estado

    def mostrar_info(self):
        return f"ID: {self.venta_id}, Nombre: {self.venta_venta}, Fecha: {self.venta_fecha}, Ganancia: {self.venta_ganancia}, Empleado: {self.venta_usuario}, Lista de compras: {self.venta_articulo}, Estado: {self.venta_estado}"


class Venta_confirmar:  
    # Constructor
    def __init__(self, venta_id, venta_venta, venta_ganancia, venta_usuario, venta_articulo, venta_estado):
        self.venta_id = venta_id
        self.venta_venta = venta_venta
        self.venta_ganancia = venta_ganancia
        self.venta_usuario = venta_usuario
        self.venta_articulo = venta_articulo 
        self.venta_estado = venta_estado


class Venta_sin_articulo:
    # Constructor
    def __init__(self, venta_id, venta_venta, venta_fecha, venta_ganancia, venta_usuario, venta_estado):
        self.venta_id = venta_id
        self.venta_venta = venta_venta
        self.venta_fecha = venta_fecha
        self.venta_ganancia = venta_ganancia
        self.venta_usuario = venta_usuario
        self.venta_estado = venta_estado

class Venta_nombre_usuario:
    # Constructor
    def __init__(self, venta_id, venta_venta, venta_usuario):
        self.venta_id = venta_id
        self.venta_venta = venta_venta
        self.venta_usuario = venta_usuario

class Venta_eliminar:
    # Constructor
    def __init__(self, venta_id):
        self.venta_id = venta_id