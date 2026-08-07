# DAO: Data Acces Object
# proveedor_dao: Objeto de acceso a datos de la tabla de proveedores

from database.conexion import Conexion
from models.privilegio import Privilegio

class PrivilegioDAO():

    # SELECT privilegio_privilegio FROM privilegios
    def nombres_privilegios(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT privilegio_id, privilegio_privilegio FROM privilegios ORDER BY privilegio_id ASC")
        registros = cursor.fetchall()

        nombres = []
        for registro in registros:
            privilegio = Privilegio(
                privilegio_id = registro[0],
                privilegio_privilegio = registro[1]
            )
            nombres.append(privilegio)

        cursor.close()
        conexion.close()
        return nombres