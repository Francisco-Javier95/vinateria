class DetalleVenta:

    # Constructor
    def __init__(self, detalle_id, detalle_venta_id, detalle_articulo_id, detalle_cantidad, detalle_precio_unitario, detalle_subtotal):
        self.detalle_id = detalle_id
        self.detalle_venta_id = detalle_venta_id
        self.detalle_articulo_id = detalle_articulo_id
        self.detalle_cantidad = detalle_cantidad
        self.detalle_precio_unitario = detalle_precio_unitario
        self.detalle_subtotal = detalle_subtotal