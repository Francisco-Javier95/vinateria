class Usuario:

    # Constructor
    def __init__(self, usuario_id, usuario_usuario, usuario_apaterno, usuario_amaterno, usuario_nuempleado, usuario_correo, usuario_contrasenia, usuario_privilegio):
        self.usuario_id = usuario_id
        self.usuario_usuario = usuario_usuario
        self.usuario_apaterno = usuario_apaterno
        self.usuario_amaterno = usuario_amaterno
        self.usuario_nuempleado = usuario_nuempleado
        self.usuario_correo = usuario_correo
        self.usuario_contrasenia = usuario_contrasenia
        self.usuario_privilegio = usuario_privilegio

    def mostrar_info(self):
        return f"Nombre: {self.usuario_usuario}, Apellido paterno: {self.usuario_apaterno}, Apellido materno: {self.usuario_amaterno}, Número empleado: {self.usuario_nuempleado}, Correo: {self.usuario_correo}, Contraseña: {self.usuario_contrasenia}, Privilegio: {self.usuario_privilegio}"
    
class Usuario_eliminar:
    # Constructor
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id