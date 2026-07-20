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

        cursor.execute("SELECT * FROM categorias")
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

        cursor.execute("SELECT categoria_categoria FROM categorias")
        registros = cursor.fetchall()

        nombres = []
        for registro in registros:
            categoria = Categoria_nombre(categoria_categoria = registro[0])
            nombres.append(categoria)
        cursor.close()
        conexion.close()
        return nombres
    
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

    def eliminar(self, categoria_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM categorias WHERE categoria_id = %s",
            (categoria_id.categoria_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()