import flet as ft

from models.proveedor import Proveedor_eliminar
from dao.proveedor_dao import ProveedorDAO

import globals

def alerta_eliminar(regresar = None, formulario_visible = False, cerrando_modal = None, registro = None):

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    def confirmar(evento):
        # Recuperar el nombre del proveedor
        proveedor_nombre = registro.get('nombre') if registro else ""
        proveedor_id = registro.get('id') if registro else None

        # Obtener la función de SnackBar
        snackbar_func = globals.obtener_snackbar()

        try:
            # Validar que no sea el proveedor "Ninguno"
            if proveedor_id == 1:
                print("No se puede eliminar el proveedor 'Ninguno'")
                evento.page.update()
                return

            proveedor_dao = ProveedorDAO()
            eliminar_proveedor = Proveedor_eliminar(proveedor_id=proveedor_id)

            # Ejecutar eliminación
            proveedor_dao.eliminar(eliminar_proveedor)

            mensaje.value = ""
            mensaje.color = ft.Colors.GREEN

            # ===== SNACKBAR PARA ELIMINACIÓN FÍSICA =====
            if snackbar_func:
                snackbar_func(f"Proveedor '{proveedor_nombre}' eliminado exitosamente", "eliminar")
                    
            # ===== NOTIFICACIÓN PARA ELIMINACIÓN FÍSICA =====
            globals.agregar_notificacion(
                titulo=f"Proveedor {proveedor_nombre}",
                mensaje="eliminado exitosamente",
                tipo="eliminar"
            )

            # Actualizar el contador de notificaciones
            try:
                if evento.page and hasattr(evento.page, 'actualizar_contador'):
                    evento.page.actualizar_contador()
            except:
                pass

            print(f"Proveedor '{proveedor_nombre}' (ID: {proveedor_id}) eliminado")

            # Cerrar el modal después de actualizar
            if formulario_visible and cerrando_modal:
                evento.page.update()
                cerrando_modal()
                return

        except Exception as error:
            mensaje.value = f"Error al eliminar: {str(error)}"
            mensaje.color = ft.Colors.RED
            print(f"Error al eliminar proveedor: {error}")
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
                "¿Deseas eliminar este proveedor?",
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
                blur_radius = 20, # Difuminado
                color = ft.Colors.BLACK_38
            ),
            width = 250
        )
    else:
        return ft.Container(
            padding = 30,
            content = contenido_alerta,
        )