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
        padding = 30,
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
        padding = 20,
        content = ft.Column(
            controls = [
                ft.ElevatedButton(
                    "Punto de venta",
                    icon = ft.Icons.HOME,
                    width = 180,
                    on_click = mostrar_inicio
                ),
                ft.ElevatedButton(
                    "Inventario",
                    icon = ft.Icons.INVENTORY,
                    width = 180,
                    on_click = mostrar_lista_articulos # No se le coloca () ya que esto indica que es una acción que se eejecutra de forma automatica, sin la opión de que el usuario oprima el botón de "Invetario"
                ),
                ft.ElevatedButton(
                    "Proveedores",
                    icon = ft.Icons.HOME,
                    width = 180
                ),
                ft.ElevatedButton(
                    "Informes",
                    icon = ft.Icons.HOME,
                    width = 180
                ),
                ft.ElevatedButton(
                    "Usuarios",
                    icon = ft.Icons.HOME,
                    width = 180
                ),
                ft.ElevatedButton(
                    "Corte",
                    icon = ft.Icons.HOME,
                    width = 180
                ),

                ft.Divider(color = "#CCC9C5"),

                ft.Text(
                    "Imagen",
                    size = 22,
                    weight = ft.FontWeight.BOLD,
                    color = ft.Colors.BLACK 
                ),
            ],
            spacing = 15
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