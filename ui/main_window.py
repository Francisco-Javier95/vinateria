import flet as ft

from ui.articulos_list import articulos_list

def main_window(page: ft.Page):
    # Definir configuración de la página principal
    page.title = "Sistema de Punto de Venta 'La Vinata'"
    page.window_width = 1100
    page.window_height = 700
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

    def inicio():
        return ft.Column(
            controls = [
                titulo,
                subtitulo
            ],
            spacing = 10
        )
    
    def mostrar_inicio(e=None):
        contenido.content = inicio()
        page.update()

    def mostrar_lista_articulos(e=None):
        contenido.content = articulos_list(mostrar_inicio)
        page.update()

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
                            width = 250
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
                            width = 250
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
                            width = 250
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
                            width = 250
                        )
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

    layout = ft.Row(
        controls = [
            menu_lateral,
            contenido
        ],
        expand = True
    )

    page.add(layout) # Sin el page.add no se mostraria nada

    mostrar_inicio()