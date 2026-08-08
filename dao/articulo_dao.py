# DAO: Data Acces Object
# articulos_dao: Objeto de acceso a datos de la tabla de articulos
import os

from database.conexion import Conexion
from models.articulo import Articulo
from models.articulo import Articulo_editar

class ArticuloDAO:

    #SELECT * FROM articulos
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT a.articulo_id, a.articulo_articulo, a.articulo_codigo,
                c.categoria_categoria, a.articulo_imagen, a.articulo_precio,
                a.articulo_stock, p.proveedor_proveedor, a.articulo_vendidos
            FROM articulos_1 a
            INNER JOIN categorias c ON a.articulo_categoria = c.categoria_id
            INNER JOIN proveedores p ON a.articulo_proveedor = p.proveedor_id
            ORDER BY a.articulo_id ASC
        """)
        registros = cursor.fetchall()
        articulos = []
        for reg in registros:
            articulo = Articulo(
                articulo_id=reg[0],
                articulo_articulo=reg[1],
                articulo_codigo=reg[2],
                articulo_categoria=reg[3],
                articulo_imagen=reg[4],
                articulo_precio=reg[5],
                articulo_stock=reg[6],
                articulo_proveedor=reg[7],
                articulo_vendidos=reg[8]
            )
            articulos.append(articulo)
        cursor.close()
        conexion.close()
        return articulos
    
    def obtener_id_del_articulo(self, articulo_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT articulo_id, articulo_articulo, articulo_codigo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor, articulo_vendidos FROM articulos_1 WHERE articulo_id = %s",
            (articulo_id,)
        )

        datos_articulo = cursor.fetchone()

        if datos_articulo:
            return Articulo(
                articulo_id = datos_articulo[0],
                articulo_articulo = datos_articulo[1],
                articulo_codigo = datos_articulo[2],
                articulo_categoria = datos_articulo[3],
                articulo_imagen = datos_articulo[4],
                articulo_precio = datos_articulo[5],
                articulo_stock = datos_articulo[6],
                articulo_proveedor = datos_articulo[7],
                articulo_vendidos = datos_articulo[8]
            )

        conexion.commit()
        cursor.close()
        conexion.close()

        return None
    
    def insertar(self, articulo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            INSERT INTO articulos_1 (articulo_articulo, articulo_codigo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor, articulo_vendidos)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
                articulo.articulo_vendidos
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def verificar_nombre_existente(self, nombre, articulo_id=None):
        """
        Verifica si ya existe un artículo con el mismo nombre.
        Si se proporciona articulo_id, excluye ese artículo de la verificación.
        """
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        if articulo_id:
            # Para edición: excluir el artículo actual
            cursor.execute(
                "SELECT COUNT(*) FROM articulos_1 WHERE articulo_articulo = %s AND articulo_id != %s",
                (nombre, articulo_id)
            )
        else:
            # Para creación: verificar en toda la tabla
            cursor.execute(
                "SELECT COUNT(*) FROM articulos_1 WHERE articulo_articulo = %s",
                (nombre,)
            )
        
        count = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        
        return count > 0
    
    def verificar_codigo_existente(self, codigo, articulo_id=None):
        """
        Verifica si ya existe un artículo con el mismo código.
        Si se proporciona articulo_id, excluye ese artículo de la verificación.
        """
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        if articulo_id:
            # Para edición: excluir el artículo actual
            cursor.execute(
                "SELECT COUNT(*) FROM articulos_1 WHERE articulo_codigo = %s AND articulo_id != %s",
                (codigo, articulo_id)
            )
        else:
            # Para creación: verificar en toda la tabla
            cursor.execute(
                "SELECT COUNT(*) FROM articulos_1 WHERE articulo_codigo = %s",
                (codigo,)
            )
        
        count = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        
        return count > 0

    def editar_form(self, articulo):
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

    def actualizar(self, articulo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            UPDATE articulos_1 
            SET articulo_articulo = %s, articulo_codigo = %s, articulo_categoria = %s, articulo_imagen = %s, articulo_precio = %s, articulo_stock = %s, articulo_proveedor = %s, articulo_vendidos = %s
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
                articulo.articulo_vendidos,
                articulo.articulo_id
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, articulo_id):
        # Elimina un artículo de la base de datos y su imagen asociada
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            # 1. Obtener el nombre de la imagen antes de eliminar el registro
            cursor.execute(
                "SELECT articulo_imagen FROM articulos_1 WHERE articulo_id = %s",
                (articulo_id.articulo_id,)
            )
            resultado = cursor.fetchone()

            if resultado:
                nombre_imagen = resultado[0]
                print(f"Imagen a eliminar: {nombre_imagen}")

                # 2. Eliminar el registro de la base de datos
                cursor.execute(
                    "DELETE FROM articulos_1 WHERE articulo_id = %s",
                    (articulo_id.articulo_id,)
                )

                # 3. Eliminar el archivo de imagen si existe
                if nombre_imagen:
                    ruta_imagen = f"assets/imagenes/imagenes_DB/{nombre_imagen}"

                    # Varificar si el archivo existe y no es la imagen por defecto
                    if os.path.exists(ruta_imagen):
                        # Varificar que no sea una imagen por defecto del sistema
                        if nombre_imagen not in ["imagen_default_campo_imagen.png", "botella_negra_default_Punto_de_Venta.jpg"]:
                            os.remove(ruta_imagen)
                            print(f"Imagen eliminada: {ruta_imagen}")
                        else: 
                            print(f"Imagen por defecto no eliminada: {nombre_imagen}")
                    else:
                        print(f"Archivo de imagen no encontrado: {ruta_imagen}")
            else:
                print(f"No se encontró el artículo con ID: {articulo_id}")
                return False

            conexion.commit()
            print(f"Articulo ID {articulo_id} eliminado existosamente")
            return True

        except Exception as error:
            conexion.rollback()
            print(f"Error al eliminar artículo: {error}")
            raise error

        finally:
            cursor.close()
            conexion.close()