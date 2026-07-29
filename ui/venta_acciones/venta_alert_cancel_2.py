import flet as ft

from models.venta import Venta_eliminar
from dao.venta_dao import VentaDAO

def alerta_cancelar_2(regresar = None, formulario_visible = False, cerrando_modal = None, registro = None):

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    def confirmar(evento):
        # Recuperar el nombre del articulo
        venta_venta = registro.get('nombre') if registro else ""

        try:
            venta_dao = VentaDAO()
            venta_id = registro.get('id') if registro else None

            cancelar_venta = Venta_eliminar(venta_id = venta_id,)

            venta_dao.eliminar(cancelar_venta)

            mensaje.value = f"Venta {venta_venta} ha sido cancelada exitosamente"
            mensaje.color = ft.Colors.GREEN
            print(f"Venta {venta_venta} ha sido cancelada exitosamente de ID {venta_id}")

            # ------Cerrar el modal después de cancelar la venta------
            if formulario_visible and cerrando_modal:
                evento.page.update()
                # Cerrar el modal
                cerrando_modal()
                return

        except Exception as error:
            mensaje.value = f"Error al cancelar el: {error}"
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
                "¿Deseas cancelar esta venta?",
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

                        on_click = confirmar # Al hacer clic, sobre el boton de "Confirmar" se abrira el modal
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

                        on_click = lambda e: cerrando_modal() # Al hacer clic, sobre el boton de "Cancelar" se abrira el modal
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