# DAO: Data Acces Object
# venta_dao: Objeto de acceso a datos de la tabla de ventas

# DAO: Data Access Object
# venta_dao: Objeto de acceso a datos de la tabla de ventas

from database.conexion import Conexion
from models.venta import Venta

class VentaDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM ventas ORDER BY venta_id ASC")
        registros = cursor.fetchall()

        ventas = []
        for registro in registros:
            venta = Venta(
                venta_id=registro[0],
                venta_venta=registro[1],
                venta_fecha=registro[2],
                venta_ganancia=registro[3],
                venta_usuario=registro[4],
                venta_articulo=registro[5],
                venta_estado=registro[6],
            )
            ventas.append(venta)
        cursor.close()
        conexion.close()
        return ventas

    def obtener_id_del_proveedor(self, venta_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT venta_id, venta_venta, venta_fecha, venta_ganancia, venta_usuario, venta_articulo, venta_estado FROM ventas WHERE venta_id = %s",
            (venta_id,)
        )

        datos_venta = cursor.fetchone()
        cursor.close()
        conexion.close()

        if datos_venta:
            return Venta(
                venta_id = datos_venta[0],
                venta_venta = datos_venta[1],
                venta_fecha = datos_venta[2],
                venta_ganancia = datos_venta[3],
                venta_usuario = datos_venta[4],
                venta_articulo = datos_venta[5],
                venta_estado = datos_venta[6],
            )

        return None
    
    def insertar(self, venta):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO ventas (venta_venta, venta_ganancia, venta_usuario, venta_articulo, venta_estado)
            VALUES (%s, %s, %s, %s, %s)
        """

        # venta_fecha se omitirá para usar CURRENT_DATE en la BD
        cursor.execute(
            sql,
            (
                venta.venta_venta,
                venta.venta_ganancia,
                venta.venta_usuario,
                venta.venta_articulo,
                venta.venta_estado,
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, venta):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            UPDATE ventas 
            SET venta_venta = %s, venta_ganancia = %s, venta_usuario = %s, venta_articulo = %s, venta_estado = %s
            WHERE venta_id = %s
        """
        cursor.execute(
            sql,
            (
                venta.venta_venta,
                venta.venta_ganancia,
                venta.venta_usuario,
                venta.venta_articulo,
                venta.venta_estado,
                venta.venta_id
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, venta_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM ventas WHERE venta_id = %s",
            (venta_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()