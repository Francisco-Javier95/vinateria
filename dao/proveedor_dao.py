# DAO: Data Acces Object
# proveedor_dao: Objeto de acceso a datos de la tabla de proveedores

from database.conexion import Conexion
from models.proveedor import Proveedor

class ProveedorDAO:

    #SELECT * FROM proveedores
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM proveedores")
        registros = cursor.fetchall()

        proveedores = []
        for registro in registros:
            proveedor = Proveedor (proveedor_id = registro[0], proveedor_proveedor = registro[1], proveedor_aPaterno = registro[2], proveedor_aMaterno = registro[3], proveedor_telefono = registro[4], proveedor_direccion = registro[5], proveedor_correo = registro[6])
            proveedores.append(proveedor)
        cursor.close()
        conexion.close()
        return proveedores
    
    def insertar(self, proveedor):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            INSERT INTO proveedores (proveedor_proveedor, proveedor_apaterno, proveedor_amaterno, proveedor_telefono, proveedor_direccion, proveedor_correo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                proveedor.proveedor_proveedor,
                proveedor.proveedor_aPaterno,
                proveedor.proveedor_aMaterno,
                proveedor.proveedor_telefono,
                proveedor.proveedor_direccion,
                proveedor.proveedor_correo
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, proveedor):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            UPDATE proveedores 
            SET proveedor_proveedor = %s, proveedor_apaterno = %s, proveedor_amaterno = %s, proveedor_telefono = %s, proveedor_direccion = %s, proveedor_correo = %s
            WHERE proveedor_id = %s
        """
        cursor.execute(
            sql,
            (
                proveedor.proveedor_proveedor,
                proveedor.proveedor_aPaterno,
                proveedor.proveedor_aMaterno,
                proveedor.proveedor_telefono,
                proveedor.proveedor_direccion,
                proveedor.proveedor_correo,
                proveedor.proveedor_id
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, proveedor_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM proveedores WHERE proveedor_id = %s",
            (proveedor_id.proveedor_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()