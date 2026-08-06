# dao/detalle_venta_dao.py
from database.conexion import Conexion
from models.detalle_venta import DetalleVenta

class DetalleVentaDAO:
    
    def insertar(self, detalle):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO detalles_venta (detalle_venta_id, detalle_articulo_id, detalle_cantidad, detalle_precio_unitario, detalle_subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                detalle.detalle_venta_id,
                detalle.detalle_articulo_id,
                detalle.detalle_cantidad,
                detalle.detalle_precio_unitario,
                detalle.detalle_subtotal
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()
    
    def obtener_por_venta(self, venta_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT detalle_id, detalle_venta_id, detalle_articulo_id, detalle_cantidad, detalle_precio_unitario, detalle_subtotal FROM detalles_venta WHERE detalle_venta_id = %s",
            (venta_id,)
        )
        registros = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        detalles = []
        for registro in registros:
            detalle = DetalleVenta(
                detalle_id=registro[0],
                detalle_venta_id=registro[1],
                detalle_articulo_id=registro[2],
                detalle_cantidad=registro[3],
                detalle_precio_unitario=registro[4],
                detalle_subtotal=registro[5]
            )
            detalles.append(detalle)
        return detalles