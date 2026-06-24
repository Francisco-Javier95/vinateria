class Venta:

    # Constructor
    def __init__(self, venta_id, venta_venta, venta_fecha, venta_ganancia, venta_usuario, venta_articulo):
        self.venta_id = venta_id
        self.venta_venta = venta_venta
        self.venta_fecha = venta_fecha
        self.venta_ganancia = venta_ganancia
        self.venta_usuario = venta_usuario
        self.venta_articulo = venta_articulo

    def mostrar_info(self):
        return f"ID: {self.venta_id}, Nombre: {self.venta_venta}, Fecha: {self.venta_fecha}, Ganancia: {self.venta_ganancia}, Empleado: {self.venta_usuario}, Lista de compras: {self.venta_articulo}"