# DAO: Data Acces Object
# venta_dao: Objeto de acceso a datos de la tabla de ventas

# DAO: Data Access Object
# venta_dao: Objeto de acceso a datos de la tabla de ventas

from database.conexion import Conexion
from models.venta import Venta
from models.venta import Venta_sin_articulo

class VentaDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT v.venta_id, v.venta_venta, v.venta_fecha, v.venta_ganancia, u.usuario_usuario, v.venta_estado FROM ventas v INNER JOIN usuarios u ON v.venta_usuario = u.usuario_id ORDER BY venta_id DESC")
        registros = cursor.fetchall()

        ventas = []
        for registro in registros:
            venta = Venta_sin_articulo(
                venta_id=registro[0],
                venta_venta=registro[1],
                venta_fecha=registro[2],
                venta_ganancia=registro[3],
                venta_usuario=registro[4],
                venta_estado=registro[5],
            )
            ventas.append(venta)
        cursor.close()
        conexion.close()
        return ventas

    def obtener_estados(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT venta_estado FROM ventas ORDER BY venta_id ASC")
        registros = cursor.fetchall()

        estados = []
        for registro in registros:
            venta = Venta(
                venta_estado=registro[0],
            )
            estados.append(venta)
        cursor.close()
        conexion.close()
        return estados

    def obtener_id_de_la_venta(self, venta_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
                SELECT v.venta_id, v.venta_venta, v.venta_fecha, v.venta_ganancia, 
                    u.usuario_usuario, v.venta_articulo, v.venta_estado
                FROM ventas v
                INNER JOIN usuarios u ON v.venta_usuario = u.usuario_id
                WHERE v.venta_id = %s
            """,
            (venta_id,)
        )

        datos = cursor.fetchone()
        cursor.close()
        conexion.close()

        if datos:
            return Venta(
                venta_id=datos[0],
                venta_venta=datos[1],
                venta_fecha=datos[2],
                venta_ganancia=datos[3],
                venta_usuario=datos[4], # Guardar el nombre del usuario
                venta_articulo=datos[5],
                venta_estado=datos[6]
            )

        return None

    def obtener_id_editar_venta(self, venta_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT venta_id, venta_venta, venta_fecha, venta_ganancia, venta_usuario, venta_articulo, venta_estado FROM ventas WHERE venta_id = %s
        """,
        (venta_id,)
        )

        datos = cursor.fetchone()
        cursor.close()
        conexion.close()

        if datos:
            return Venta(
                venta_id = datos[0],
                venta_venta = datos[1],
                venta_fecha = datos[2],
                venta_ganancia = datos[3],
                venta_usuario = datos[4],
                venta_articulo = datos[5],
                venta_estado = datos[6]
            )

        return None
    
    def insertar(self, venta):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO ventas (venta_venta, venta_ganancia, venta_usuario, venta_estado)
            VALUES (%s, %s, %s, %s)
            RETURNING venta_id
        """
        cursor.execute(
            sql,
            (
                venta.venta_venta,
                venta.venta_ganancia,
                venta.venta_usuario,
                venta.venta_estado,
            )
        )
        venta_id = cursor.fetchone()[0]
        conexion.commit()
        cursor.close()
        conexion.close()
        return venta_id

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT MAX(venta_id) FROM ventas")
        ultimo_id = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        return ultimo_id



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
        

    def editar_nombre_usuario(self, venta):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            UPDATE ventas 
            SET venta_venta = %s, venta_usuario = %s
            WHERE venta_id = %s
        """
        cursor.execute(
            sql,
            (
                venta.venta_venta,
                venta.venta_usuario,
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
            (venta_id.venta_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()