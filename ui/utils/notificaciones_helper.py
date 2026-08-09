import globals

def actualizar_contador_notificaciones(page):
    """Actualiza el contador de notificaciones desde cualquier lugar"""
    try:
        if page and hasattr(page, 'actualizar_contador'):
            page.actualizar_contador()
    except Exception as e:
        print(f"Error al actualizar contador: {e}")

def notificar_accion(page, titulo, mensaje, tipo="success"):
    """Agrega una notificación y actualiza el contador"""
    globals.agregar_notificacion(titulo, mensaje, tipo)
    actualizar_contador_notificaciones(page)