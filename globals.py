# Declarar variable local
venta_pendiente_global = None # Variable global que almacenara el valor del ID (venta_id) de la venta pendiente cuando se presiona el boton de "Continuar"


# Variable global para almacenar la sesión del usuario
sesion_usuario = None

def establecer_sesion(usuario):
    # Establece la sesión del usuario actual
    global sesion_usuario
    sesion_usuario = usuario
    print(f"Sesión establecida para: {usuario.usuario_usuario}")

def obtener_sesion():
    # Obtiene la sesión del usuario actual
    return sesion_usuario

def limpiar_sesion():
    # Limpia la sesión del usuario actual
    global sesion_usuario
    sesion_usuario = None
    print("Sesión limpiada")

def usuario_autenticado():
    # Verifica si hay un usuario autenticado
    return sesion_usuario is not None