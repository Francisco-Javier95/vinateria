import flet as ft
import globals

from ui.punto_de_venta import punto_de_venta

from ui.articulos_list import articulos_list
from ui.proveedores_list import proveedores_list
from ui.informes import informes
from ui.usuarios_list import usuarios_list
from ui.corte_list import ventas_list

def main_window(page: ft.Page, cerrar_sesion):
    # Definir configuración de la página principal
    # page.title = "Sistema de Punto de Venta 'La Vinata'"
    page.expand = True
    page.padding = 0
    page.bgcolor = "#F9F6F0"

    # Ejemplo de widget: Text
    titulo = ft.Text(
        "Sistema de Punto de Venta",
        size = 24,
        weight = ft.FontWeight.BOLD,
        color = ft.Colors.PURPLE_800
    )

    subtitulo = ft.Text(
        "Seleccione una opción del menú",
        size = 24,
        color = ft.Colors.PINK_900
    )

    # Widget container
    contenido = ft.Container(
        padding = 5,
        expand = True
    )
    
    def mostrar_inicio(e = None):
        contenido.content = punto_de_venta()
        page.update()

    def mostrar_lista_articulos(e = None):
        contenido.content = articulos_list(mostrar_inicio)
        page.update()

    def mostrar_lista_proveedores(e = None):
        contenido.content = proveedores_list(mostrar_inicio)
        page.update()

    def mostrar_informes(e = None):
        contenido.content = informes(mostrar_inicio)
        page.update()

    def mostrar_lista_usuarios(e = None):
        contenido.content = usuarios_list(mostrar_inicio)
        page.update()

    def mostrar_lista_corte(e = None):
        contenido.content = ventas_list(mostrar_inicio)
        page.update()


    usuario_actual = globals.obtener_sesion()

    def crear_avatar(nombre_usuario, size=40):
        """Crea un avatar circular con las iniciales del usuario"""
        # Obtener iniciales del nombre
        if nombre_usuario:
            partes = nombre_usuario.split()
            iniciales = "".join([parte[0].upper() for parte in partes[:2]])
        else:
            iniciales = "?"
        
        return ft.Container(
            content=ft.Text(
                iniciales,
                size=size // 2,
                color="#ffffff",
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor="#6b1d41",
            border_radius=size // 2,
            width=size,
            height=size,
            alignment=ft.Alignment.CENTER,
            tooltip=nombre_usuario,
        )


    # if usuario_actual:
    #     nombre_usuario = usuario_actual.usuario_usuario
    #     avatar = crear_avatar(nombre_usuario)
        
    #     barra_usuario = ft.Row(
    #         controls=[
    #             avatar,
    #             ft.Column(
    #                 controls=[
    #                     ft.Text(
    #                         nombre_usuario,
    #                         size=14,
    #                         weight=ft.FontWeight.BOLD,
    #                         color="#6b1d41",
    #                     ),
    #                     ft.Text(
    #                         "Bienvenido",
    #                         size=11,
    #                         color="#926600",
    #                     ),
    #                 ],
    #                 spacing=0,
    #             ),
    #         ],
    #         spacing=10,
    #         alignment=ft.MainAxisAlignment.START,
    #     )
    # else:
    #     barra_usuario = ft.Text("Usuario no autenticado", size=14, color="#9095a0")


    # Botón de cerrar sesión
    # boton_cerrar_sesion = ft.ElevatedButton(
    #     "Cerrar sesión",
    #     icon=ft.Icons.LOGOUT,
    #     style=ft.ButtonStyle(
    #         bgcolor="#de3b40",
    #         color="#ffffff",
    #         shape=ft.RoundedRectangleBorder(radius=10),
    #     ),
    #     on_click=cerrar_sesion,
    # )


    menu_lateral = ft.Container(
        width = 220,
        bgcolor = "#F9F6F0",
        border = ft.Border.all(
            1,
            "#e2dcd5"
        ),
        padding = 10,
        content = ft.Column(
            controls = [
                # # === BARRA DE USUARIO EN EL MENÚ ===
                # ft.Container(
                #     content=barra_usuario,
                #     padding=ft.Padding.symmetric(vertical=10, horizontal=5),
                #     border=ft.Border.only(
                #         bottom=ft.BorderSide(width=1, color="#e2dcd5")
                #     ),
                # ),
                ft.Column(
                    controls = [
                        ft.ElevatedButton(
                            "Punto de venta",
                            style = ft.ButtonStyle(
                                # Borde sólido vino-caramelo de 2 píxeles por defecto
                                side = {
                                    ft.ControlState.DEFAULT: 
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6b1d41"
                                        ),
                                    # Borde rojo de 2 píxeles al pasar el mouse
                                    ft.ControlState.HOVERED:
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6c4e07"
                                    )
                                },
                                bgcolor = {
                                    ft.ControlState.DEFAULT: "#ffffff",
                                    ft.ControlState.HOVERED: "#efb034",
                                },
                                color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                icon_color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                padding = 20,
                                shape = ft.RoundedRectangleBorder(radius = 10)
                            ),
                            icon = ft.Icons.POINT_OF_SALE,
                            width = 250,
                            on_click = mostrar_inicio
                        ),
                        ft.ElevatedButton(
                            "Inventario",
                            style = ft.ButtonStyle(
                                # Borde sólido vino-caramelo de 2 píxeles por defecto
                                side = {
                                    ft.ControlState.DEFAULT: 
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6b1d41"
                                        ),
                                    # Borde rojo de 2 píxeles al pasar el mouse
                                    ft.ControlState.HOVERED:
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6c4e07"
                                    )
                                },
                                bgcolor = {
                                    ft.ControlState.DEFAULT: "#ffffff",
                                    ft.ControlState.HOVERED: "#efb034",
                                },
                                color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                icon_color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                padding = 20,
                                shape = ft.RoundedRectangleBorder(radius = 10)
                            ),
                            icon = ft.Icons.WINE_BAR,
                            width = 250,
                            on_click = mostrar_lista_articulos # No se le coloca () ya que esto indica que es una acción que se ejecutara de forma automatica, sin la opión de que el usuario oprima el botón de "Invetario"
                        ),
                        ft.ElevatedButton(
                            "Proveedores",
                            style = ft.ButtonStyle(
                                # Borde sólido vino-caramelo de 2 píxeles por defecto
                                side = {
                                    ft.ControlState.DEFAULT: 
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6b1d41"
                                        ),
                                    # Borde rojo de 2 píxeles al pasar el mouse
                                    ft.ControlState.HOVERED:
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6c4e07"
                                    )
                                },
                                bgcolor = {
                                    ft.ControlState.DEFAULT: "#ffffff",
                                    ft.ControlState.HOVERED: "#efb034",
                                },
                                color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                icon_color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                padding = 20,
                                shape = ft.RoundedRectangleBorder(radius = 10)
                            ),
                            icon = ft.Icons.LOCAL_SHIPPING,
                            width = 250,
                            on_click = mostrar_lista_proveedores # Traer el contenido de "proveedores_list.py"
                        ),
                        ft.ElevatedButton(
                            "Informes",
                            style = ft.ButtonStyle(
                                # Borde sólido vino-caramelo de 2 píxeles por defecto
                                side = {
                                    ft.ControlState.DEFAULT: 
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6b1d41"
                                        ),
                                    # Borde rojo de 2 píxeles al pasar el mouse
                                    ft.ControlState.HOVERED:
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6c4e07"
                                    )
                                },
                                bgcolor = {
                                    ft.ControlState.DEFAULT: "#ffffff",
                                    ft.ControlState.HOVERED: "#efb034",
                                },
                                color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                icon_color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                padding = 20,
                                shape = ft.RoundedRectangleBorder(radius = 10)
                            ),
                            icon = ft.Icons.TRENDING_UP,
                            width = 250,
                            on_click = mostrar_informes # Traer el contenido de "informes.py"
                        ),
                        ft.ElevatedButton(
                            "Usuarios",
                            style = ft.ButtonStyle(
                                # Borde sólido vino-caramelo de 2 píxeles por defecto
                                side = {
                                    ft.ControlState.DEFAULT: 
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6b1d41"
                                        ),
                                    # Borde rojo de 2 píxeles al pasar el mouse
                                    ft.ControlState.HOVERED:
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6c4e07"
                                    )
                                },
                                bgcolor = {
                                    ft.ControlState.DEFAULT: "#ffffff",
                                    ft.ControlState.HOVERED: "#efb034",
                                },
                                color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                icon_color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                padding = 20,
                                shape = ft.RoundedRectangleBorder(radius = 10)
                            ),
                            icon = ft.Icons.PERSON,
                            width = 250,
                            on_click = mostrar_lista_usuarios # Traer el contenido de "usuarios_list.py"
                        ),
                        ft.ElevatedButton(
                            "Corte",
                            style = ft.ButtonStyle(
                                # Borde sólido vino-caramelo de 2 píxeles por defecto
                                side = {
                                    ft.ControlState.DEFAULT: 
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6b1d41"
                                        ),
                                    # Borde rojo de 2 píxeles al pasar el mouse
                                    ft.ControlState.HOVERED:
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6c4e07"
                                    )
                                },
                                bgcolor = {
                                    ft.ControlState.DEFAULT: "#ffffff",
                                    ft.ControlState.HOVERED: "#efb034",
                                },
                                color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                icon_color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                padding = 20,
                                shape = ft.RoundedRectangleBorder(radius = 10)
                            ),
                            icon = ft.Icons.ATTACH_MONEY,
                            width = 250,
                            on_click = mostrar_lista_corte
                        ),
                        ft.ElevatedButton(
                            "Salir",
                            style = ft.ButtonStyle(
                                # Borde sólido vino-caramelo de 2 píxeles por defecto
                                side = {
                                    ft.ControlState.DEFAULT: 
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6b1d41"
                                        ),
                                    # Borde rojo de 2 píxeles al pasar el mouse
                                    ft.ControlState.HOVERED:
                                        ft.BorderSide(
                                            width = 2,
                                            color = "#6c4e07"
                                    )
                                },
                                bgcolor = {
                                    ft.ControlState.DEFAULT: "#ffffff",
                                    ft.ControlState.HOVERED: "#efb034",
                                },
                                color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                icon_color = {
                                    ft.ControlState.DEFAULT: "#efb034",
                                    ft.ControlState.HOVERED: "#ffffff",
                                },
                                padding = 20,
                                shape = ft.RoundedRectangleBorder(radius = 10)
                            ),
                            icon = ft.Icons.LOGOUT,
                            width = 250,
                            margin = ft.Margin.only(top = 50),
                            on_click = cerrar_sesion
                        ),
                    ]
                ),

                ft.Column(
                    controls = [
                        ft.Divider(color = "#CCC9C5"),

                        ft.Image(
                            src = f"imagenes/logotipo_La_Vinata.png",
                            width = 200,
                            height = 200,
                            border_radius = 10
                        )
                    ],
                    spacing = 3
                )
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing = 10
        )
    )

    layout = ft.Container(
        content = ft.Row(
            controls = [
                menu_lateral,
                contenido
            ],
            expand = True
        ),
        expand = True,
        bgcolor = "#F9F6F0"
    )

    mostrar_inicio()

    return layout