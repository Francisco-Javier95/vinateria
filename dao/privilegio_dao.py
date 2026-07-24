# DAO: Data Acces Object
# proveedor_dao: Objeto de acceso a datos de la tabla de proveedores

from database.conexion import Conexion
from models.privilegio import Privilegio_nombre

class PrivilegioDAO():

    # SELECT privilegio_privilegio FROM privilegios
    def nombres_privilegios(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT privilegio_privilegio FROM privilegios")
        registros = cursor.fetchall()

        nombres = []
        for registro in registros:
            privilegio = Privilegio_nombre(privilegio_privilegio = registro[0])
            nombres.append(privilegio)

        cursor.close()
        conexion.close()
        return nombres