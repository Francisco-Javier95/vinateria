# DAO: Data Acces Object
# proveedor_dao: Objeto de acceso a datos de la tabla de proveedores

from database.conexion import Conexion
from models.proveedor import Proveedor
from models.proveedor import Proveedor_nombre

class ProveedorDAO:

    #SELECT * FROM proveedores
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM proveedores WHERE proveedor_id != 1 ORDER BY proveedor_id ASC")
        registros = cursor.fetchall()

        proveedores = []
        for registro in registros:
            proveedor = Proveedor (proveedor_id = registro[0], proveedor_proveedor = registro[1], proveedor_apaterno = registro[2], proveedor_amaterno = registro[3], proveedor_telefono = registro[4], proveedor_direccion = registro[5], proveedor_correo = registro[6])
            proveedores.append(proveedor)
        cursor.close()
        conexion.close()
        return proveedores
    
    # SELECT proveedor_proveedor FROM proveedores
    def nombres_proveedores(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT proveedor_id, proveedor_proveedor FROM proveedores ORDER BY proveedor_id ASC")
        registros = cursor.fetchall()

        nombres = []
        for registro in registros:
            proveedor = Proveedor_nombre(
                proveedor_id = registro[0],
                proveedor_proveedor = registro[1]
            )
            nombres.append(proveedor)
        cursor.close()
        conexion.close()
        return nombres

    # SELECT * FROM proveedores WHERE proveedor_id = %s
    def obtener_id_del_proveedor (self, proveedor_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT proveedor_id, proveedor_proveedor, proveedor_apaterno, proveedor_amaterno, proveedor_telefono, proveedor_direccion, proveedor_correo FROM proveedores WHERE proveedor_id = %s",
            (proveedor_id,)
        )

        datos_proveedor = cursor.fetchone()

        if datos_proveedor:
            return Proveedor(
                proveedor_id = datos_proveedor[0],
                proveedor_proveedor = datos_proveedor[1],
                proveedor_apaterno = datos_proveedor[2],
                proveedor_amaterno = datos_proveedor[3],
                proveedor_telefono = datos_proveedor[4],
                proveedor_direccion = datos_proveedor[5],
                proveedor_correo = datos_proveedor[6]
            )

        conexion.commit()
        cursor.close()
        conexion.close()

        return None
    
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
                proveedor.proveedor_apaterno,
                proveedor.proveedor_amaterno,
                proveedor.proveedor_telefono,
                proveedor.proveedor_direccion,
                proveedor.proveedor_correo
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    # Verificar si existe un proveedor con el mismo nombre
    def verificar_nombre_completo_existente(self, nombre, apellido_p, apellido_m, proveedor_id = None):
        # Varificar si existe un proveedor con el mismo nombre, apellido paterno y apellido materno
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        if proveedor_id:
            # Para edición: excluir el proveedor actual
            cursor.execute(
                "SELECT COUNT(*) FROM proveedores WHERE proveedor_proveedor = %s AND proveedor_apaterno = %s AND proveedor_amaterno = %s AND proveedor_id != %s",
                (nombre, apellido_p, apellido_m, proveedor_id)
            )
        else:
            # Para creación: verificar en toda la tabla
            cursor.execute(
                "SELECT COUNT(*) FROM proveedores WHERE proveedor_proveedor = %s AND proveedor_apaterno = %s AND proveedor_amaterno = %s",
                (nombre, apellido_p, apellido_m,)
            )

        count = cursor.fetchone()[0]
        cursor.close()
        conexion.close()

        return count > 0

    # Verificar si existe un proveedor con el mismo teléfono
    def verificar_telefono_existente(self, telefono, proveedor_id = None):
        # Verificar si existe un número telefonico registrado igual al que se quiere ingresar
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        if proveedor_id:
            # Para edición: excluir el proveedor actual
            cursor.execute(
                "SELECT COUNT(*) FROM proveedores WHERE proveedor_telefono = %s AND proveedor_id != %s",
                (telefono, proveedor_id)
            ) 
        else:
            # Para creación: verificar en toda la tabla
            cursor.execute(
                "SELECT COUNT(*) FROM proveedores WHERE proveedor_telefono = %s",
                (telefono,)
            )

        count = cursor.fetchone()[0]
        cursor.close()
        conexion.close()

        return count > 0

    # Verificar si existe un proveedor con el mismo correo electrónico
    def verificar_correo_existente(self, correo, proveedor_id = None):
        # Verificar si existe un correo electrónico registrado en otro proveedor en la base de datos
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        if proveedor_id:
            # Para edición: excluir el proveedor actual
            cursor.execute(
                "SELECT COUNT(*) FROM proveedores WHERE proveedor_correo = %s AND proveedor_id = %s",
                (correo, proveedor_id)
            )
        else:
            # Para creación: verificar en toda la tabla
            cursor.execute(
                "SELECT COUNT(*) FROM proveedores WHERE proveedor_correo = %s",
                (correo,)
            )

        count = cursor.fetchone()[0]
        cursor.close()
        conexion.close()

        return count > 0

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
                proveedor.proveedor_apaterno,
                proveedor.proveedor_amaterno,
                proveedor.proveedor_telefono,
                proveedor.proveedor_direccion,
                proveedor.proveedor_correo,
                proveedor.proveedor_id
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    # Metodo para cambiar los proveedores de los articulos que tengan el proveedor y despues eliminar al proveedor
    def eliminar(self, proveedor):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # Iniciar transacción
            conexion.autocommit = False
            
            # 1. Obtener el ID del proveedor a eliminar
            proveedor_id = proveedor.proveedor_id
            
            # 2. ACTUALIZAR artículos que tienen este proveedor
            cursor.execute(
                "UPDATE articulos_1 SET articulo_proveedor = 1 WHERE articulo_proveedor = %s",
                (proveedor_id,)
            )
            
            registros_afectados = cursor.rowcount
            print(f"{registros_afectados} artículos actualizados a 'Ninguno' (proveedor_id=1)")
            
            # 3. ELIMINAR el proveedor
            cursor.execute(
                "DELETE FROM proveedores WHERE proveedor_id = %s",
                (proveedor_id,)
            )
            
            # Confirmar transacción
            conexion.commit()
            print(f"Proveedor ID {proveedor_id} eliminado exitosamente")
            
        except Exception as error:
            # Si hay error, deshacer todos los cambios
            conexion.rollback()
            print(f"Error al eliminar proveedor: {error}")
            raise error
            
        finally:
            cursor.close()
            conexion.close()