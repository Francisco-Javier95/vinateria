class Usuario:

    # Constructor
    def __init__(self, usuario_id, usuario_usuario, usuario_aPaterno, usuario_aMaterno, usuario_nuEmpleado, usuario_correo, usuario_contrasenia, usuario_privilegio):
        self.usuario_id = usuario_id
        self.usuario_usuario = usuario_usuario
        self.usuario_aPaterno = usuario_aPaterno
        self.usaurio_aMaterno = usuario_aMaterno
        self.usuario_nuEmpleado = usuario_nuEmpleado
        self.usuario_correo = usuario_correo
        self.usuario_contrasenia = usuario_contrasenia
        self.usuario_privilegio = usuario_privilegio

    def mostrar_info(self):
        return f"Nombre: {self.usuario_usuario}, Apellido paterno: {self.usuario_aPaterno}, Apellido materno: {self.usaurio_aMaterno}, Número empleado: {self.usuario_nuEmpleado}, Correo: {self.usuario_correo}, Contraseña: {self.usuario_contrasenia}, Privilegio: {self.usuario_privilegio}"