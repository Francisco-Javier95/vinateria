import flet as ft

from models.usuario import Usuario_eliminar
from dao.usuario_dao import UsuarioDAO

import globals

def alerta_eliminar(regresar = None, formulario_visible = False, cerrando_modal = None, registro = None):

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    def confirmar(evento):
        # Recuperar el nombre del usuario
        usuario_usuario = registro.get('nombre') if registro else ""

        # Obtener la función de SnackBar
        snackbar_func = globals.obtener_snackbar()

        mensaje.value = "Todos los campos son obligatorios"
        mensaje.color = ft.Colors.RED
        try:
            usuario_dao = UsuarioDAO()
            usuario_id = registro.get('id') if registro else None

            eliminar_usuario = Usuario_eliminar(usuario_id = usuario_id,)

            usuario_dao.eliminar(eliminar_usuario)

            mensaje.value = ""
            mensaje.color = ft.Colors.GREEN

            # ===== SNACKBAR PARA ELIMINACIÓN FÍSICA =====
            if snackbar_func:
                snackbar_func(f"Proveedor '{usuario_usuario}' eliminado exitosamente", "eliminar")
                    
            # ===== NOTIFICACIÓN PARA ELIMINACIÓN FÍSICA =====
            globals.agregar_notificacion(
                titulo=f"Proveedor {usuario_usuario}",
                mensaje="eliminado exitosamente",
                tipo="eliminar"
            )

            # Actualizar el contador de notificaciones
            try:
                if evento.page and hasattr(evento.page, 'actualizar_contador'):
                    evento.page.actualizar_contador()
            except:
                pass

            print(f"Usuario {usuario_usuario} ha sido eliminado exitosamente de ID {usuario_id}")

            # ------Cerrar el modal después de actualizar------
            if formulario_visible and cerrando_modal:
                evento.page.update()
                # Cerrar el modal
                cerrando_modal()
                return

        except Exception as error:
            mensaje.value = f"Error al eliminar el: {error}"
            mensaje.value = ft.Colors.RED


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
                "¿Deseas eliminar este usuario?",
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