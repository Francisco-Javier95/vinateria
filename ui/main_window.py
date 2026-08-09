import flet as ft
import globals

from ui.punto_de_venta import punto_de_venta

from ui.articulos_list import articulos_list
from ui.proveedores_list import proveedores_list
from ui.informes import informes
from ui.usuarios_list import usuarios_list
from ui.corte_list import ventas_list
from ui.notificaciones import panel_notificaciones
from ui.toast_notification import ToastNotification

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
        # Crea un avatar circular con las iniciales del usuario
        # Obtener iniciales del nombre
        if nombre_usuario:
            partes = nombre_usuario.split()
            iniciales = "".join([parte[0].upper() for parte in partes[:2]])
        else:
            iniciales = "?"
        
        return ft.Container(
            content = ft.Text(
                iniciales,
                color = "#ffffff",
                weight = ft.FontWeight.BOLD,
                size = 17
            ),
            bgcolor = "#1e1e1e",
            border = ft.Border.all(
                2,
                "#ffffff"
            ),
            border_radius = 35,
            width = 35,
            height = 35,
            alignment = ft.Alignment.CENTER,

            tooltip = nombre_usuario
        )


    if usuario_actual:
        nombre_usuario = usuario_actual.usuario_usuario
        avatar = crear_avatar(nombre_usuario)
        
        barra_usuario = ft.Row(
            controls=[
                avatar,
                ft.Column(
                    controls=[
                        ft.Text(
                            nombre_usuario,
                            size = 14,
                            weight = ft.FontWeight.BOLD,
                            color = "#ffffff",
                            overflow = ft.TextOverflow.ELLIPSIS,  # Agrega "..." al final
                            width = 125,  # Ancho aproximado para 20 caracteres
                        ),
                    ],
                    spacing=0,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
    else:
        barra_usuario = ft.Text("Usuario no autenticado", size=14, color="#9095a0")


    # Botón de cerrar sesión
    boton_cerrar_sesion = ft.ElevatedButton(
        "Salir",
        icon = ft.Icons.LOGOUT,
        style = ft.ButtonStyle(
            bgcolor = "#1e1e1e",
            color = "#ffffff",
            shape = ft.RoundedRectangleBorder(radius = 10),
        ),
        on_click = cerrar_sesion,
    )

    toast_manager = ToastNotification(page)
    globals.set_toast_manager(toast_manager)

    # ========== VARIABLES DE ESTADO ==========
    panel_notificaciones_abierto = False
    overlay_notificaciones = None

    # Crear el contenedor del contador
    contenedor_contador = ft.Container(
        content=ft.Text(
            "0",
            size=11,
            color="#ffffff",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor="#c9a03d",
        border_radius=10,
        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
        visible=False,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
    )

    # Función para actualizar el contador
    def actualizar_contador():
        """Actualiza el contador de notificaciones no leídas"""
        contador = globals.contar_notificaciones_no_leidas()
        
        if contador > 0:
            contenedor_contador.content.value = str(contador)
            contenedor_contador.visible = True
            contenedor_contador.bgcolor = "#c9a03d"
        else:
            contenedor_contador.visible = False
        
        # Actualizar la página
        if page:
            try:
                page.update()
            except:
                pass
        
        print(f"🔔 Contador actualizado: {contador} notificaciones no leídas")
    
    # Registrar el callback en globals
    globals.registrar_callback_contador(actualizar_contador)
    
    # Guardar referencia en la página para actualizar desde otros lugares
    page.actualizar_contador = actualizar_contador

    # ========== FUNCIONES DEL PANEL DE NOTIFICACIONES ==========
    def abrir_panel_notificaciones(e):
        nonlocal panel_notificaciones_abierto, overlay_notificaciones
        
        if panel_notificaciones_abierto:
            cerrar_panel_notificaciones(e)
            return
        
        # Crear el panel de notificaciones
        panel = panel_notificaciones(
            page=page,
            cerrar_panel=lambda: cerrar_panel_notificaciones(None)
        )
        
        # Crear overlay (capa oscura)
        overlay = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(expand=True),  # Espacio para hacer clic y cerrar
                    panel,
                ],
                spacing=0,
                expand=True,
            ),
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            expand=True,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            on_click=lambda e: cerrar_panel_notificaciones(e),
        )
        
        # Guardar referencia
        overlay_notificaciones = overlay
        panel_notificaciones_abierto = True
        
        # Agregar a la página
        page.overlay.append(overlay)
        
        # Marcar todas como leídas al abrir (opcional)
        # globals.marcar_todas_como_leidas()
        # actualizar_contador()
        
        page.update()

    # ========== BOTÓN DE NOTIFICACIONES ==========
    boton_notificaciones = ft.IconButton(
        icon = ft.Icons.NOTIFICATIONS_OUTLINED,
        style = ft.ButtonStyle(
            bgcolor = {
                ft.ControlState.DEFAULT: "#1e1e1e",
                ft.ControlState.HOVERED: "#c9a03d",
            },
            side = {
                ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#c9a03d"),
                ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#926600"),
            },
            icon_color = {
                ft.ControlState.DEFAULT: "#ffffff",
                ft.ControlState.HOVERED: "#1e1e1e",
            },
            shape = ft.RoundedRectangleBorder(radius = 10),
            padding = ft.Padding.symmetric(horizontal = 8, vertical = 8)
        ),
        height = 50,
        width = 50,
        align = ft.Alignment.CENTER,
        tooltip = "Notificaciones",
        on_click = abrir_panel_notificaciones,
        icon_size = 28,
    )
    
    # Stack para superponer el contador sobre el botón
    # El contador se posiciona en la esquina superior derecha del botón
    btn_notificaciones_con_contador = ft.Stack(
        controls=[
            boton_notificaciones,
            ft.Container(
                content=contenedor_contador,
                bottom=-4,
                left=-4,
            ),
        ],
        width=50,
        height=50,
    )
    
    def cerrar_panel_notificaciones(e):
        nonlocal panel_notificaciones_abierto, overlay_notificaciones
        
        if overlay_notificaciones and overlay_notificaciones in page.overlay:
            page.overlay.remove(overlay_notificaciones)
        
        panel_notificaciones_abierto = False
        overlay_notificaciones = None
        
        # Actualizar contador al cerrar
        actualizar_contador()
        page.update()

    boton_inicio = ft.IconButton(
        icon = ft.Icons.HOUSE,
        style = ft.ButtonStyle(
            bgcolor = {
                ft.ControlState.DEFAULT: "#1e1e1e",
                ft.ControlState.HOVERED: "#c9a03d",
            },
            side = {
                ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#c9a03d"),
                ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#926600"),
            },
            icon_color = {
                ft.ControlState.DEFAULT: "#ffffff",
                ft.ControlState.HOVERED: "#1e1e1e",
            },
            shape = ft.RoundedRectangleBorder(radius = 10),
            padding = ft.Padding.symmetric(horizontal = 8, vertical = 8)
        ),
        height = 50,
        width = 50,
        align = ft.Alignment.CENTER,
        tooltip = "Punto de Venta",

        on_click = mostrar_inicio
    )

    imagen_vinateria = ft.Image(
        src = f"imagenes/La_Vinata_Vinos_y_Licores_HEADER.png",
        expand = True
    )

    inicio_imagen = ft.Row(
        controls = [
            boton_inicio,
            imagen_vinateria
        ],
        height = 50,
        alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    )

    avatar_y_cerrar_sesion = ft.Row(
        controls = [
            barra_usuario,

            ft.Container(content = ft.Text(""), height = 20, width = 1, bgcolor = "#c9a03d"),

            boton_cerrar_sesion,
            btn_notificaciones_con_contador

        ],
        width = 400,
        alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    )

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

    copyright = ft.Column(
        controls = [
            ft.Text(
                spans = [
                    ft.TextSpan(
                        "2026 © ",
                        ft.TextStyle(color = "#ffffff", size = 12) # Texto en blanco
                    ),
                    ft.TextSpan(
                        "La Vinata",
                        ft.TextStyle(color = "#c9a03d", size = 12) # Texto color mostaza
                    )
                ],
            ),
            ft.Text(
                "Todos los derechos reservados",
                color = "#ffffff",
                size = 12
            )
        ],
        spacing = 0
    )

    telefono = "522471242745"

    contacto = ft.Container(
        content = ft.Row(
            controls = [
                ft.Icon(
                    ft.Icons.PHONE,
                    color = "#ffffff",
                    size = 30
                ),

                ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.Text(
                                "Contacto:",
                                color = "#ffffff",
                                weight = ft.FontWeight.BOLD,
                                size = 18
                            ),
                            ft.Text(
                                "+52 247 124 2745",
                                style = ft.TextStyle(
                                    decoration = ft.TextDecoration.UNDERLINE,
                                    decoration_color = "#c9a03d", # Color del subrayado
                                    decoration_thickness = 1, # Grosor del subrayado
                                ),
                                color = "#c9a03d",
                                size = 20,
                            )
                        ]
                    ),
                    url = f"https://wa.me/{telefono}",
                    tooltip = "Hablar con el equipo"
                )
            ]
        )
    )
    

    footer = ft.Row(
        controls = [
            copyright,

            ft.Container(
                content = imagen_vinateria,
                height = 50
            ),

            contacto
        ],
        expand = True,
        alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    )

    layout = ft.Container(
        content = ft.Column(
            controls = [ 
                # Primer nivel (HEADER)
                ft.Container(
                    content = ft.Row(
                        controls = [
                            inicio_imagen,
                            avatar_y_cerrar_sesion
                        ],
                        expand = True,
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    bgcolor = "#1e1e1e",
                    padding = 10
                ),

                # Segundo nivel (Menú lateral y contenido)
                ft.Container(
                    content = ft.Row(
                        controls = [
                            menu_lateral,
                            contenido
                        ],
                        expand = True
                    ),
                    expand = True,
                    bgcolor = "#F9F6F0"
                ),

                # Tercer nivel (Footer)
                ft.Container(
                    content = ft.Row(
                        controls = [
                            footer
                        ],
                        expand = True,
                    ),
                    bgcolor = "#1e1e1e",
                    padding = 10
                )
            ],
            spacing = 0,
        )
    )

    mostrar_inicio()

    return layout