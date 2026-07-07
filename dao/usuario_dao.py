# DAO: Data Acces Object
# usuario_dao: Objeto de acceso a datos de la tabla de usuarios

from database.conexion import Conexion
from models.usuario import Usuario

class UsuarioDAO:

    #SELECT * FROM usuarios
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM usuarios")
        registros = cursor.fetchall()

        usuarios = []
        for registro in registros:
            usuario = Usuario (usuario_id = registro[0], usuario_usuario = registro[1], usuario_apaterno = registro[2], usuario_amaterno = registro[3], usuario_nuempleado = registro[4], usuario_correo = registro[5], usuario_contrasenia = registro[6], usuario_privilegio = registro[7])
            usuarios.append(usuario)
        cursor.close()
        conexion.close()
        return usuarios
    
    def insertar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            INSERT INTO usuarios (usuario_usuario, usuario_apaterno, usuario_amaterno, usuario_nuempleado, usuario_correo, usuario_contrasenia, usuario_privilegio)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                usuario.usuario_usuario,
                usuario.usuario_apaterno,
                usuario.usuario_amaterno,
                usuario.usuario_nuempleado,
                usuario.usuario_correo,
                usuario.usuario_contrasenia,
                usuario.usuario_privilegio
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql= """
            UPDATE usuarios 
            SET usuario_usuario = %s, usuario_apaterno = %s, usuario_amaterno = %s, usuario_nuempleado = %s, usuario_correo = %s, usuario_contrasenia = %s, usuario_privilegio = %s
            WHERE usuario_id = %s
        """
        cursor.execute(
            sql,
            (
                usuario.usuario_usuario,
                usuario.usuario_apaterno,
                usuario.usuario_amaterno,
                usuario.usuario_nuempleado,
                usuario.usuario_correo,
                usuario.usuario_contrasenia,
                usuario.usuario_privilegio,
                usuario.usuario_id
            )
        )
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, usuario_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM usuarios WHERE usuario_id = %s",
            (usuario_id.usuario_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()