# DAO: Data Acces Object
# usuario_dao: Objeto de acceso a datos de la tabla de usuarios

from database.conexion import Conexion
from models.usuario import Usuario
from models.usuario import Usuario_nombre

class UsuarioDAO:

    #SELECT * FROM usuarios
    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT u.usuario_id, u.usuario_usuario, u.usuario_apaterno, u.usuario_amaterno, u.usuario_nuempleado, u.usuario_correo, u.usuario_contrasenia, p.privilegio_privilegio FROM usuarios u INNER JOIN privilegios p ON u.usuario_privilegio = p.privilegio_id ORDER BY u.usuario_id ASC")
        registros = cursor.fetchall()

        usuarios = []
        for registro in registros:
            usuario = Usuario (usuario_id = registro[0], usuario_usuario = registro[1], usuario_apaterno = registro[2], usuario_amaterno = registro[3], usuario_nuempleado = registro[4], usuario_correo = registro[5], usuario_contrasenia = registro[6], usuario_privilegio = registro[7])
            usuarios.append(usuario)
        cursor.close()
        conexion.close()
        return usuarios

    # SELECT usuario_usuario, usuario_apaterno, usuario_amaterno FROM usuarios
    def nombres_usuarios(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT usuario_id, usuario_usuario, usuario_apaterno, usuario_amaterno FROM usuarios ORDER BY usuario_id ASC")
        registros = cursor.fetchall()

        nombres = []
        for registro in registros:
            usuario = Usuario_nombre(
                usuario_id = registro[0],
                usuario_usuario = registro[1],
                usuario_apaterno = registro[2],
                usuario_amaterno = registro[3]
            )
            nombres.append(usuario)
        cursor.close()
        conexion.close()
        return nombres

    # SELECT * FROM usuarios WHERE usuario_id = %s
    def obtener_id_del_usuario (self, usuario_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT usuario_id, usuario_usuario, usuario_apaterno, usuario_amaterno, usuario_nuempleado, usuario_correo, usuario_contrasenia, usuario_privilegio FROM usuarios WHERE usuario_id = %s",
            (usuario_id,)
        )

        datos_usuario = cursor.fetchone()

        if datos_usuario:
            return Usuario(
                usuario_id = datos_usuario[0],
                usuario_usuario = datos_usuario[1],
                usuario_apaterno = datos_usuario[2],
                usuario_amaterno = datos_usuario[3],
                usuario_nuempleado = datos_usuario[4],
                usuario_correo = datos_usuario[5],
                usuario_contrasenia = datos_usuario[6],
                usuario_privilegio = datos_usuario[7]
            )

        conexion.commit()
        cursor.close()
        conexion.close()

        return None
    
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

    # Verificar nombre completo
    def verificar_nombre_completo_existente(self, nombre, apellido_p, apellido_m, usuario_id = None):
        # Verificar si existe un usuario con el mismo nombre
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        if usuario_id:
            # Para edición: excluir el usuario actual
            cursor.execute(
                "SELECT COUNT(*) FROM usuarios WHERE usuario_usuario = %s AND usuario_apaterno = %s AND usuario_amaterno = %s AND usuario_id != %s",
                (nombre, apellido_p, apellido_m, usuario_id)
            )
        else:
            # Para creación: verificar en toda la tabla
            cursor.execute(
                "SELECT COUNT(*) FROM usuarios WHERE usuario_usuario = %s AND usuario_apaterno = %s AND usuario_amaterno = %s",
                (nombre, apellido_p, apellido_m,)
            )

        count = cursor.fetchone()[0]
        cursor.close()
        conexion.close()

        return count > 0

    def verificar_numero_empleado_existente(self, numero_empleado, usuario_id = None):
        # Verificar si existe un usuario con el mismo número de empleado
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        if usuario_id:
            # Para edición: excluir el usuario actual
            cursor.execute(
                "SELECT COUNT(*) FROM usuarios WHERE usuario_nuempleado = %s AND usuario_id != %s",
                (numero_empleado, usuario_id)
            )
        else:
            # Para creación: verificar en toda la tabla
            cursor.execute(
                "SELECT COUNT(*) FROM usuarios WHERE usuario_nuempleado = %s",
                (numero_empleado,)
            )

        count = cursor.fetchone()[0]
        cursor.close()
        conexion.close()

        return count > 0

    def verificar_correo_existente(self, correo, usuario_id = None):
        # Verificar si existe un usuario con el mismo correo electronico
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        if usuario_id:
            # Para edición: excluir el usuario actual
            cursor.execute(
                "SELECT COUNT(*) FROM usuarios WHERE usuario_correo = %s AND usuario_id != %s",
                (correo, usuario_id)
            )
        else:
            # Para creación: Verificar en toda la tabla
            cursor.execute(
                "SELECT COUNT(*) FROM usuarios WHERE usuario_correo = %s",
                (correo,)
            )

        count = cursor.fetchone()[0]
        cursor.close()
        conexion.close()

        return count > 0

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


    def obtener_por_correo(self, correo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT usuario_id, usuario_usuario, usuario_apaterno, usuario_amaterno, usuario_nuempleado, usuario_correo, usuario_contrasenia, usuario_privilegio FROM usuarios WHERE usuario_correo = %s",
            (correo,)
        )
        datos = cursor.fetchone()
        cursor.close()
        conexion.close()
        if datos:
            from models.usuario import Usuario
            return Usuario(
                usuario_id=datos[0],
                usuario_usuario=datos[1],
                usuario_apaterno=datos[2],
                usuario_amaterno=datos[3],
                usuario_nuempleado=datos[4],
                usuario_correo=datos[5],
                usuario_contrasenia=datos[6],
                usuario_privilegio=datos[7]
            )
        return None

    def obtener_por_correo_y_empleado(self, correo, nuempleado):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT usuario_id, usuario_usuario, usuario_apaterno, usuario_amaterno, usuario_nuempleado, usuario_correo, usuario_contrasenia, usuario_privilegio FROM usuarios WHERE usuario_correo = %s AND usuario_nuempleado = %s",
            (correo, nuempleado)
        )
        datos = cursor.fetchone()
        cursor.close()
        conexion.close()
        if datos:
            from models.usuario import Usuario
            return Usuario(
                usuario_id=datos[0],
                usuario_usuario=datos[1],
                usuario_apaterno=datos[2],
                usuario_amaterno=datos[3],
                usuario_nuempleado=datos[4],
                usuario_correo=datos[5],
                usuario_contrasenia=datos[6],
                usuario_privilegio=datos[7]
            )
        return None

    def actualizar_contrasenia(self, usuario_id, nueva_contrasenia_hash):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE usuarios SET usuario_contrasenia = %s WHERE usuario_id = %s",
            (nueva_contrasenia_hash, usuario_id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()