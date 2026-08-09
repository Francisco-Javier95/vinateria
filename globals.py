# globals.py

# Declarar variable local
venta_pendiente_global = None

# Variable global para almacenar la sesión del usuario
sesion_usuario = None

notificaciones = []  # Lista para almacenar las notificaciones
MAX_NOTIFICACIONES = 50  # Límite máximo de notificaciones

_callback_actualizar_contador = None

# Variable para la función de SnackBar
mostrar_snackbar = None

def obtener_snackbar():
    """Retorna la función para mostrar SnackBars"""
    return mostrar_snackbar

def registrar_callback_contador(callback):
    """Registra un callback para actualizar el contador"""
    global _callback_actualizar_contador
    _callback_actualizar_contador = callback

def agregar_notificacion(titulo, mensaje, tipo="info", icono=None):
    from datetime import datetime
    
    # Diccionario de iconos por tipo
    iconos_por_tipo = {
        "info": "📢",
        "crear": "✅",
        "editar": "✏️",
        "eliminar": "🗑️"
    }
    
    # Colores por tipo
    colores_por_tipo = {
        "crear": {"bg": "#4CAF50", "text": "#ffffff"},
        "editar": {"bg": "#2196F3", "text": "#ffffff"},
        "eliminar": {"bg": "#f44336", "text": "#ffffff"},
        "info": {"bg": "#FF9800", "text": "#ffffff"}
    }
    
    # Crear la notificación
    notificacion = {
        "id": len(notificaciones) + 1,
        "titulo": titulo,
        "mensaje": mensaje,
        "tipo": tipo,
        "icono": icono or iconos_por_tipo.get(tipo, "📢"),
        "color": colores_por_tipo.get(tipo, {"bg": "#2196F3", "text": "#ffffff"}),
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "leida": False
    }
    
    # Agregar al inicio de la lista (más reciente primero)
    notificaciones.insert(0, notificacion)
    
    # Limitar el número de notificaciones
    if len(notificaciones) > MAX_NOTIFICACIONES:
        notificaciones.pop()
    
    print(f"Notificación agregada: {titulo}")
    
    # Actualizar el contador si hay callback registrado
    if _callback_actualizar_contador:
        _callback_actualizar_contador()
    
    return notificacion

def obtener_notificaciones(no_leidas=False):
    """Obtiene la lista de notificaciones"""
    if no_leidas:
        return [n for n in notificaciones if not n["leida"]]
    return notificaciones

def marcar_como_leida(notificacion_id):
    """Marca una notificación como leída"""
    for notificacion in notificaciones:
        if notificacion["id"] == notificacion_id:
            notificacion["leida"] = True
            return True
    return False

def marcar_todas_como_leidas():
    """Marca todas las notificaciones como leídas"""
    for notificacion in notificaciones:
        notificacion["leida"] = True

def eliminar_notificacion(notificacion_id):
    """Elimina una notificación específica"""
    global notificaciones
    notificaciones = [n for n in notificaciones if n["id"] != notificacion_id]
    return True

def limpiar_notificaciones():
    """Limpia todas las notificaciones"""
    global notificaciones
    notificaciones = []

def contar_notificaciones_no_leidas():
    """Cuenta cuántas notificaciones no leídas hay"""
    return len([n for n in notificaciones if not n["leida"]])

def establecer_sesion(usuario):
    """Establece la sesión del usuario actual"""
    global sesion_usuario
    sesion_usuario = usuario
    print(f"Sesión establecida para: {usuario.usuario_usuario}")

def obtener_sesion():
    """Obtiene la sesión del usuario actual"""
    return sesion_usuario

def limpiar_sesion():
    """Limpia la sesión del usuario actual"""
    global sesion_usuario
    sesion_usuario = None
    print("Sesión limpiada")

def usuario_autenticado():
    """Verifica si hay un usuario autenticado"""
    return sesion_usuario is not None