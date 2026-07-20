# DAO: Data Acces Object
# articulos_dao: Objeto de acceso a datos de la tabla de articulos

from database.conexion import Conexion
from models.articulo import Articulo

class ArticuloDAO:

    #SELECT * FROM articulos
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT a.articulo_id, a.articulo_articulo, a.articulo_codigo, c.categoria_categoria, a.articulo_imagen, a.articulo_precio, a.articulo_stock, p.proveedor_proveedor FROM articulos_1 a INNER JOIn categorias c ON a.articulo_categoria = c.categoria_id INNER JOIN proveedores p ON a.articulo_proveedor = p.proveedor_id")
        registros = cursor.fetchall()

        articulos = []
        for registro in registros:
            articulo = Articulo (articulo_id = registro[0], articulo_articulo = registro[1], articulo_codigo = registro[2], articulo_categoria = registro[3], articulo_imagen = registro[4], articulo_precio = registro[5], articulo_stock = registro[6], articulo_proveedor = registro[7])
            articulos.append(articulo)
        cursor.close()
        conexion.close()
        return articulos
    
    def insertar(self, articulo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            INSERT INTO articulos_1 (articulo_articulo, articulo_codigo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                articulo.articulo_articulo,
                articulo.articulo_codigo,
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
            UPDATE articulos_1 
            SET articulo_articulo = %s, articulo_codigo = %s, articulo_categoria = %s, articulo_imagen = %s, articulo_precio = %s, articulo_stock = %s, articulo_proveedor = %s
            WHERE articulo_id = %s
        """
        cursor.execute(
            sql,
            (
                articulo.articulo_articulo,
                articulo.articulo_codigo,
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
            "DELETE FROM articulos_1 WHERE articulo_id = %s",
            (articulo_id.articulo_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()