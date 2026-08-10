import flet as ft
import globals

from ui.punto_de_venta import punto_de_venta
from ui.articulos_list import articulos_list
from ui.proveedores_list import proveedores_list
from ui.informes import informes
from ui.usuarios_list import usuarios_list
from ui.corte_list import ventas_list
from ui.notificaciones import panel_notificaciones

def main_window(page: ft.Page, cerrar_sesion):
    # Definir configuración de la página principal
    page.expand = True
    page.padding = 0
    page.bgcolor = "#F9F6F0"

    # Obtener el usuario actual
    usuario_actual = globals.obtener_sesion()
    
    # Obtener el privilegio del usuario (por defecto 3 si no hay sesión)
    privilegio = usuario_actual.usuario_privilegio if usuario_actual else 3

    # Widget container
    contenido = ft.Container(
        padding=5,
        expand=True
    )
    
    def mostrar_inicio(e=None):
        contenido.content = punto_de_venta()
        page.update()

    def mostrar_lista_articulos(e=None):
        contenido.content = articulos_list(mostrar_inicio)
        page.update()

    def mostrar_lista_proveedores(e=None):
        contenido.content = proveedores_list(mostrar_inicio)
        page.update()

    def mostrar_informes(e=None):
        contenido.content = informes(mostrar_inicio)
        page.update()

    def mostrar_lista_usuarios(e=None):
        contenido.content = usuarios_list(mostrar_inicio)
        page.update()

    def mostrar_lista_corte(e=None):
        contenido.content = ventas_list(mostrar_inicio)
        page.update()

    # ========== DEFINIR PERMISOS POR PRIVILEGIO ==========
    # Privilegios:
    # 1 = Administrador (Acceso total)
    # 2 = Supervisor de almacén (Punto de venta, Inventario, Proveedores)
    # 3 = Cajero (Punto de venta, Inventario)
    
    # Función para verificar si el usuario tiene acceso a un módulo
    def tiene_acceso(privilegio_requerido):
        # Si el usuario es administrador (1), tiene acceso a todo
        if privilegio == 1:
            return True
        # Si no es administrador, verificar si su privilegio coincide con el requerido
        return privilegio == privilegio_requerido

    def crear_avatar(nombre_usuario, size=40):
        if nombre_usuario:
            partes = nombre_usuario.split()
            iniciales = "".join([parte[0].upper() for parte in partes[:2]])
        else:
            iniciales = "?"
        
        return ft.Container(
            content=ft.Text(iniciales, color="#ffffff", weight=ft.FontWeight.BOLD, size=17),
            bgcolor="#1e1e1e",
            border=ft.Border.all(2, "#ffffff"),
            border_radius=35,
            width=35,
            height=35,
            alignment=ft.Alignment.CENTER,
            tooltip=nombre_usuario
        )

    # ========== CONSTRUIR MENÚ LATERAL SEGÚN PRIVILEGIO ==========
    def construir_menu_lateral():
        """Construye el menú lateral según el privilegio del usuario"""
        
        # Diccionario de botones con sus configuraciones
        botones_menu = {
            "punto_venta": {
                "texto": "Punto de venta",
                "icono": ft.Icons.POINT_OF_SALE,
                "on_click": mostrar_inicio,
                "privilegio_minimo": 3  # Accesible para todos
            },
            "inventario": {
                "texto": "Inventario",
                "icono": ft.Icons.WINE_BAR,
                "on_click": mostrar_lista_articulos,
                "privilegio_minimo": 3  # Accesible para todos
            },
            "proveedores": {
                "texto": "Proveedores",
                "icono": ft.Icons.LOCAL_SHIPPING,
                "on_click": mostrar_lista_proveedores,
                "privilegio_minimo": 2  # Solo Supervisor y Admin
            },
            "informes": {
                "texto": "Informes",
                "icono": ft.Icons.TRENDING_UP,
                "on_click": mostrar_informes,
                "privilegio_minimo": 1  # Solo Admin
            },
            "usuarios": {
                "texto": "Usuarios",
                "icono": ft.Icons.PERSON,
                "on_click": mostrar_lista_usuarios,
                "privilegio_minimo": 1  # Solo Admin
            },
            "corte": {
                "texto": "Corte",
                "icono": ft.Icons.ATTACH_MONEY,
                "on_click": mostrar_lista_corte,
                "privilegio_minimo": 1  # Solo Admin
            }
        }
        
        # Obtener el nombre del rol según privilegio
        nombres_roles = {
            1: "Administrador",
            2: "Supervisor de almacén",
            3: "Cajero"
        }
        nombre_rol = nombres_roles.get(privilegio, "Usuario")
        
        # Crear la lista de botones permitidos
        botones_permitidos = []
        
        for clave, config in botones_menu.items():
            # Verificar si el usuario tiene acceso a este módulo
            if privilegio <= config["privilegio_minimo"]:
                botones_permitidos.append(
                    ft.ElevatedButton(
                        config["texto"],
                        style=ft.ButtonStyle(
                            side={
                                ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#6b1d41"),
                                ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#6c4e07")
                            },
                            bgcolor={
                                ft.ControlState.DEFAULT: "#ffffff",
                                ft.ControlState.HOVERED: "#efb034",
                            },
                            color={
                                ft.ControlState.DEFAULT: "#efb034",
                                ft.ControlState.HOVERED: "#ffffff",
                            },
                            icon_color={
                                ft.ControlState.DEFAULT: "#efb034",
                                ft.ControlState.HOVERED: "#ffffff",
                            },
                            padding=20,
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        icon=config["icono"],
                        width=250,
                        on_click=config["on_click"]
                    )
                )
        
        # Construir el menú completo
        return ft.Container(
            width=220,
            bgcolor="#F9F6F0",
            border=ft.Border.all(1, "#e2dcd5"),
            padding=10,
            content=ft.Column(
                controls=[
                    # Botones del menú
                    ft.Column(
                        controls=botones_permitidos,
                        spacing=5,
                    ),
                    
                    # Logo al final
                    ft.Column(
                        controls=[
                            ft.Divider(color="#CCC9C5"),
                            ft.Image(
                                src="imagenes/logotipo_La_Vinata.png",
                                width=200,
                                height=200,
                                border_radius=10
                            )
                        ],
                        spacing=3
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10
            )
        )

    # ========== BARRA DE USUARIO ==========
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
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="#ffffff",
                            overflow=ft.TextOverflow.ELLIPSIS,
                            width=125,
                        ),
                        ft.Text(
                            f"Rol: {['', 'Admin', 'Supervisor', 'Cajero'][privilegio if privilegio <= 3 else 0]}",
                            size=10,
                            color="#c9a03d",
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
        icon=ft.Icons.LOGOUT,
        style=ft.ButtonStyle(
            bgcolor="#1e1e1e",
            color="#ffffff",
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=cerrar_sesion,
    )

    # ========== NOTIFICACIONES ==========
    panel_notificaciones_abierto = False
    overlay_notificaciones = None

    contenedor_contador = ft.Container(
        content=ft.Text("0", size=11, color="#ffffff", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        bgcolor="#c9a03d",
        border_radius=10,
        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
        visible=False,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
    )

    def actualizar_contador():
        contador = globals.contar_notificaciones_no_leidas()
        
        if contador > 0:
            contenedor_contador.content.value = str(contador)
            contenedor_contador.visible = True
            contenedor_contador.bgcolor = "#c9a03d"
        else:
            contenedor_contador.visible = False
        
        if page:
            try:
                page.update()
            except:
                pass
        
        print(f"Contador actualizado: {contador} notificaciones no leídas")
    
    globals.registrar_callback_contador(actualizar_contador)
    page.actualizar_contador = actualizar_contador

    def abrir_panel_notificaciones(e):
        nonlocal panel_notificaciones_abierto, overlay_notificaciones
        
        if panel_notificaciones_abierto:
            cerrar_panel_notificaciones(e)
            return
        
        panel = panel_notificaciones(
            page=page,
            cerrar_panel=lambda: cerrar_panel_notificaciones(None)
        )
        
        overlay = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(expand=True),
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
        
        overlay_notificaciones = overlay
        panel_notificaciones_abierto = True
        page.overlay.append(overlay)
        page.update()

    def cerrar_panel_notificaciones(e):
        nonlocal panel_notificaciones_abierto, overlay_notificaciones
        
        if overlay_notificaciones and overlay_notificaciones in page.overlay:
            page.overlay.remove(overlay_notificaciones)
        
        panel_notificaciones_abierto = False
        overlay_notificaciones = None
        actualizar_contador()
        page.update()

    # Botón de notificaciones
    boton_notificaciones = ft.IconButton(
        icon=ft.Icons.NOTIFICATIONS_OUTLINED,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: "#1e1e1e",
                ft.ControlState.HOVERED: "#c9a03d",
            },
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#c9a03d"),
                ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#926600"),
            },
            icon_color={
                ft.ControlState.DEFAULT: "#ffffff",
                ft.ControlState.HOVERED: "#1e1e1e",
            },
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding.symmetric(horizontal=8, vertical=8)
        ),
        height=50,
        width=50,
        align=ft.Alignment.CENTER,
        tooltip="Notificaciones",
        on_click=abrir_panel_notificaciones,
        icon_size=28,
    )
    
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

    boton_inicio = ft.IconButton(
        icon=ft.Icons.HOUSE,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: "#1e1e1e",
                ft.ControlState.HOVERED: "#c9a03d",
            },
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#c9a03d"),
                ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#926600"),
            },
            icon_color={
                ft.ControlState.DEFAULT: "#ffffff",
                ft.ControlState.HOVERED: "#1e1e1e",
            },
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding.symmetric(horizontal=8, vertical=8)
        ),
        height=50,
        width=50,
        align=ft.Alignment.CENTER,
        tooltip="Punto de Venta",
        on_click=mostrar_inicio
    )

    imagen_vinateria = ft.Image(
        src="imagenes/La_Vinata_Vinos_y_Licores_HEADER.png",
        expand=True
    )

    imagen_wine_pos = ft.Image(
        src="imagenes/Nombre_software.png",
        expand=True
    )

    inicio_imagen = ft.Row(
        controls=[
            boton_inicio,
            imagen_wine_pos
        ],
        height=50,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    avatar_y_cerrar_sesion = ft.Row(
        controls=[
            barra_usuario,
            ft.Container(content=ft.Text(""), height=20, width=1, bgcolor="#c9a03d"),
            boton_cerrar_sesion,
            btn_notificaciones_con_contador
        ],
        width=400,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # ========== CONSTRUIR MENÚ LATERAL ==========
    menu_lateral = construir_menu_lateral()

    # ========== FOOTER ==========
    copyright = ft.Column(
        controls=[
            ft.Text(
                spans=[
                    ft.TextSpan("2026 © ", ft.TextStyle(color="#ffffff", size=12)),
                    ft.TextSpan("La Vinata", ft.TextStyle(color="#c9a03d", size=12))
                ],
            ),
            ft.Text("Todos los derechos reservados", color="#ffffff", size=12)
        ],
        spacing=0
    )

    telefono = "522471242745"

    contacto = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PHONE, color="#ffffff", size=30),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Contacto:", color="#ffffff", weight=ft.FontWeight.BOLD, size=18),
                            ft.Text(
                                "+52 247 124 2745",
                                style=ft.TextStyle(
                                    decoration=ft.TextDecoration.UNDERLINE,
                                    decoration_color="#c9a03d",
                                    decoration_thickness=1,
                                ),
                                color="#c9a03d",
                                size=20,
                            )
                        ]
                    ),
                    url=f"https://wa.me/{telefono}",
                    tooltip="Hablar con el equipo"
                )
            ]
        )
    )

    footer = ft.Row(
        controls=[
            copyright,
            ft.Container(content=imagen_vinateria, height=50),
            contacto
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # ========== LAYOUT PRINCIPAL ==========
    layout = ft.Container(
        content=ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Row(
                        controls=[
                            inicio_imagen,
                            avatar_y_cerrar_sesion
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    bgcolor="#1e1e1e",
                    padding=10
                ),
                # Contenido principal
                ft.Container(
                    content=ft.Row(
                        controls=[
                            menu_lateral,
                            contenido
                        ],
                        expand=True
                    ),
                    expand=True,
                    bgcolor="#F9F6F0"
                ),
                # Footer
                ft.Container(
                    content=ft.Row(controls=[footer], expand=True),
                    bgcolor="#1e1e1e",
                    padding=10
                )
            ],
            spacing=0,
        )
    )

    mostrar_inicio()
    return layout