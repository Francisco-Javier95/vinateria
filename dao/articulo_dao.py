# DAO: Data Acces Object
# articulos_dao: Objeto de acceso a datos de la tabla de articulos

from database.conexion import Conexion
from models.articulo import Articulo

class ArticuloDAO:

    #SELECT * FROM articulo
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM articulos")
        registros = cursor.fetchall()

        articulos = []
        for registro in registros:
            articulo = Articulo (articulo_id = registro[0], articulo_articulo = registro[1], articulo_categoria = registro[2], articulo_imagen = registro[3], articulo_precio = registro[4], articulo_stock = registro[5], articulo_proveedor = registro[6])
            articulos.append(articulo)
        cursor.close()
        conexion.close()
        return articulos
    
    def insertar(self, articulo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            INSERT INTO articulos (articulo_articulo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                articulo.articulo_articulo,
                articulo.articulo_categoria,
                articulo.articulo_imagen,
                articulo.articulo_precio,
                articulo.articulo_stock,
                articulo.articulo_proveedor
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, articulo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            UPDATE articulos 
            SET articulo_articulo = %s, articulo_categoria = %s, articulo_imagen = %s, articulo_precio = %s, articulo_stock = %s, articulo_proveedor = %s
            WHERE articulo_id = %s
        """
        cursor.execute(
            sql,
            (
                articulo.articulo_articulo,
                articulo.articulo_categoria,
                articulo.articulo_imagen,
                articulo.articulo_precio,
                articulo.articulo_stock,
                articulo.articulo_proveedor,
                articulo.articulo_id
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, articulo_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM articulos WHERE articulo_id = %s",
            (articulo_id.articulo_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()