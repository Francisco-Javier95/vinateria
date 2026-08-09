# DAO: Data Acces Object
# categoría_dao: Objeto de acceso a datos de la tabla de cateorías

from database.conexion import Conexion
from models.categoria import Categoria
from models.categoria import Categoria_nombre

class CategoriaDAO:

    #SELECT * FROM categorias
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM categorias WHERE categoria_id != 1 ORDER BY categoria_id ASC")
        registros = cursor.fetchall()

        categorias = []
        for registro in registros:
            categoria = Categoria (categoria_id = registro[0], categoria_categoria = registro[1], categoria_tipo = registro[2], categoria_descripcion = registro[3])
            categorias.append(categoria)
        cursor.close()
        conexion.close()
        return categorias
    
    # SELECT categoria_categoria FROM categorias
    def nombres_categorias(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT categoria_id, categoria_categoria FROM categorias ORDER BY categoria_id ASC")
        registros = cursor.fetchall()

        nombres = []
        for registro in registros:
            categoria = Categoria_nombre(
                categoria_id = registro[0],
                categoria_categoria = registro[1]
            )
            nombres.append(categoria)
        cursor.close()
        conexion.close()
        return nombres

    # SELECT * FROM categorias WHERE categoria_id = %s
    def obtener_id_de_la_categoria (self, categoria_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM categorias WHERE categoria_id = %s",
            (categoria_id,)
        )

        datos_categoria = cursor.fetchone()

        if datos_categoria:
            return Categoria(
                categoria_id = datos_categoria[0],
                categoria_categoria = datos_categoria[1],
                categoria_tipo = datos_categoria[2],
                categoria_descripcion = datos_categoria[3]
            )

        conexion.commit()
        cursor.close()
        conexion.close()

        return None
    
    def insertar(self, categoria):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            INSERT INTO categorias (categoria_categoria, categoria_tipo, categoria_descripcion)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                categoria.categoria_categoria,
                categoria.categoria_tipo,
                categoria.categoria_descripcion
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    # Verificar si existe un proveedor con el mismo teléfono
    def verificar_nombre_existente(self, nombre, categoria_id = None):
        # Verificar si existe una categoría con el mismo nombre registrado
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        if categoria_id:
            # Para edición: excluir el proveedor actual
            cursor.execute(
                "SELECT COUNT(*) FROM categorias WHERE categoria_categoria = %s AND categoria_id != %s",
                (nombre, categoria_id)
            ) 
        else:
            # Para creación: verificar en toda la tabla
            cursor.execute(
                "SELECT COUNT(*) FROM categorias WHERE categoria_categoria = %s",
                (nombre,)
            )

        count = cursor.fetchone()[0]
        cursor.close()
        conexion.close()

        return count > 0

    def actualizar(self, categoria):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            UPDATE categorias 
            SET categoria_categoria = %s, categoria_tipo = %s, categoria_descripcion = %s
            WHERE categoria_id = %s
        """
        cursor.execute(
            sql,
            (
                categoria.categoria_categoria,
                categoria.categoria_tipo,
                categoria.categoria_descripcion,
                categoria.categoria_id
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    # Metodo para cambiar los articulos que tengan la categoria asignada a eliminar al id de la categoria "Ninguna"
    def eliminar(self, categoria):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            # Iniciar transacción
            conexion.autocommit = False

            # 1. Obtener el ID del proveedor a eliminar
            categoria_id = categoria.categoria_id

            # 2. ACTUALIZAR artículos que tienen esta categoría
            cursor.execute(
                "UPDATE articulos_1 SET articulo_categoria = 1 WHERE articulo_categoria = %s",
                (categoria_id,)
            )

            registros_afectados = cursor.rowcount
            print(f"{registros_afectados} artículos actualizados a 'Ninguna' (categoria_id = 1)")

            # 3. ELIMINAR la categoría
            cursor.execute(
                "DELETE FROM categorias WHERE categoria_id = %s",
                (categoria_id,)
            )

            # Confirmar transacción
            conexion.commit()
            print(f"Categoría ID {categoria_id} eliminada exitosamente")

        except Exception as error:
            # Si hay error, deshacer todos los cambios
            conexion.rollback()
            print(f"Error al eliminar categoría: {error}")
            raise error

        finally:
            cursor.close()
            conexion.close()