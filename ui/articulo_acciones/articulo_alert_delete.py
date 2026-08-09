import flet as ft

from models.articulo import Articulo_eliminar
from dao.articulo_dao import ArticuloDAO

import globals

def alerta_eliminar(regresar = None, formulario_visible = False, cerrando_modal = None, registro = None):

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    # Variable para almacenar el tipo de eliminación
    tipo_eliminacion = "fisica" # Puede ser "fisica" o "logica"

    def confirmar(evento):
        # Recuperar el nombre del artículo
        articulo_articulo = registro.get('nombre') if registro else ""
        articulo_id = registro.get('id') if registro else None

        # Obtener la función de SnackBar
        snackbar_func = globals.obtener_snackbar()

        if not articulo_id:
            mensaje.value = "No se pudo identificar el artículo"
            mensaje.color = ft.Colors.RED
            evento.page.update()
            return

        try:
            articulo_dao = ArticuloDAO()
            
            # ===== VERIFICAR SI TIENE VENTAS ASOCIADAS =====
            tiene_ventas = articulo_dao.tiene_ventas_asociadas(articulo_id)
            
            resultado = False
            
            if tiene_ventas:
                # Si tiene ventas, usar eliminación lógica
                print(f"El artículo '{articulo_articulo}' tiene ventas asociadas. Usando eliminación lógica.")
                resultado = articulo_dao.eliminar_logico(articulo_id)
                
                if resultado:
                    mensaje.value = ""
                    mensaje.color = ft.Colors.GREEN
                    
                    # ===== SNACKBAR PARA ELIMINACIÓN LÓGICA =====
                    if snackbar_func:
                        snackbar_func(f"Producto '{articulo_articulo}' eliminado exitosamente", "eliminar")
                    
                    # ===== NOTIFICACIÓN PARA ELIMINACIÓN LÓGICA =====
                    globals.agregar_notificacion(
                        titulo=f"Producto '{articulo_articulo}'",
                        mensaje="eliminado exitosamente",
                        tipo="eliminar"
                    )

                    # Actualizar el contador de notificaciones
                    try:
                        if evento.page and hasattr(evento.page, 'actualizar_contador'):
                            evento.page.actualizar_contador()
                    except:
                        pass

            else:
                # Si NO tiene ventas, eliminar físicamente
                print(f"El artículo '{articulo_articulo}' no tiene ventas. Eliminando físicamente.")
                
                # Primero obtener la imagen para eliminarla
                articulo = articulo_dao.obtener_id_del_articulo(articulo_id)
                nombre_imagen = articulo.articulo_imagen if articulo else None
                
                # Eliminar físicamente
                resultado = articulo_dao.eliminar_fisico(articulo_id)
                
                if resultado:
                    mensaje.value = ""
                    mensaje.color = ft.Colors.GREEN
                    
                    # Eliminar la imagen si existe
                    if nombre_imagen:
                        import os
                        ruta_imagen = f"assets/imagenes/imagenes_DB/{nombre_imagen}"
                        if os.path.exists(ruta_imagen):
                            if nombre_imagen not in ["imagen_default_campo_imagen.png", "botella_negra_default_Punto_de_Venta.jpg"]:
                                try:
                                    os.remove(ruta_imagen)
                                    print(f"Imagen eliminada: {ruta_imagen}")
                                except Exception as e:
                                    print(f"Error al eliminar imagen: {e}")
                    
                    # ===== SNACKBAR PARA ELIMINACIÓN FÍSICA =====
                    if snackbar_func:
                        snackbar_func(f"Producto '{articulo_articulo}' eliminado exitosamente", "eliminar")
                    
                    # ===== NOTIFICACIÓN PARA ELIMINACIÓN FÍSICA =====
                    globals.agregar_notificacion(
                        titulo=f"Producto {articulo_articulo}",
                        mensaje="eliminado exitosamente",
                        tipo="eliminar"
                    )

                    # Actualizar el contador de notificaciones
                    try:
                        if evento.page and hasattr(evento.page, 'actualizar_contador'):
                            evento.page.actualizar_contador()
                    except:
                        pass

            if resultado:
                # Actualizar el contador de notificaciones
                try:
                    if evento.page and hasattr(evento.page, 'actualizar_contador'):
                        evento.page.actualizar_contador()
                except:
                    pass

                # Cerrar el modal
                if formulario_visible and cerrando_modal:
                    evento.page.update()
                    cerrando_modal()
                    return
            else:
                mensaje.value = "No se pudo completar la operación"
                mensaje.color = ft.Colors.RED

        except Exception as error:
            mensaje.value = f"Error al eliminar: {error}"
            mensaje.color = ft.Colors.RED

        evento.page.update()


    contenido_alerta = ft.Column(
        controls = [
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "La Vinata",
                        ft.TextStyle(weight=ft.FontWeight.BOLD)  # Estilo en negrita
                    ),
                    ft.TextSpan(
                        " dice:",
                        ft.TextStyle() # Este texto es normal
                    ),
                ],
                size = 14,
                color = "#0d1b2a",

                text_align=ft.TextAlign.CENTER, # Alinear texto en el centro
            ),

            ft.Text(
                "¿Deseas eliminar este producto?",
                size = 14,
                color = "#0d1b2a",

                text_align=ft.TextAlign.CENTER, # Alinear texto en el centro
            ),
            
            ft.Row(
                controls = [
                    # Boton 'Confirmar'
                    ft.OutlinedButton(
                        "Confirmar",

                        style = ft.ButtonStyle(
                            bgcolor = "#ffffff",  # Color de fondo
                            side = {
                                ft.ControlState.DEFAULT: 
                                    ft.BorderSide(
                                        width = 2,
                                        color = "#066945"
                                    ),
                                # Borde rojo de 2 píxeles al pasar el mouse
                                ft.ControlState.HOVERED: 
                                    ft.BorderSide(
                                        width = 2,
                                        color = "#0cc349"
                                    )
                            },
                            padding = {
                                ft.ControlState.DEFAULT: ft.Padding.symmetric(horizontal = 10, vertical = 10)
                            },
                            color = "#066945",
                            shape = ft.RoundedRectangleBorder(radius = 10),
                        ),

                        on_click = confirmar # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                    ),

                    # Boton 'Cancelar'
                    ft.OutlinedButton(
                        "Cancelar",

                        style = ft.ButtonStyle(
                            bgcolor = "#ffffff",  # Color de fondo
                            side = {
                                ft.ControlState.DEFAULT: 
                                    ft.BorderSide(
                                        width = 2,
                                        color = "#840606"
                                    ),
                                # Borde rojo de 2 píxeles al pasar el mouse
                                ft.ControlState.HOVERED: 
                                    ft.BorderSide(
                                        width = 2,
                                        color = "#da1d1d"
                                    )
                            },
                            padding = {
                                ft.ControlState.DEFAULT: ft.Padding.symmetric(horizontal = 10, vertical = 10)
                            },
                            color = "#840606",
                            shape = ft.RoundedRectangleBorder(radius = 10)
                        ),

                        on_click = lambda e: cerrando_modal() # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                    ),
                ],
                expand = True,
                alignment = ft.MainAxisAlignment.CENTER
            )
        ]
    )

    # ---------------- Envolver en un contenedor con estilo ----------------
    if formulario_visible:
        
        return ft.Container(
            content = contenido_alerta,
            bgcolor = "#ffffff",
            border = ft.Border.all(
                2,
                "#c9a03d"
            ),
            border_radius = 10,
            padding = 30,
            shadow = ft.BoxShadow(
                spread_radius = 1, # Expansión de la sombra
                blur_radius = 20, #Difuminado
                color = ft.Colors.BLACK_38
            ),
            width = 250
        )
    else:
        return ft.Container(
            padding = 30,
            content = contenido_alerta,
        )