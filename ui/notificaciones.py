# ui/notificaciones.py

import flet as ft
import globals

def panel_notificaciones(page=None, cerrar_panel=None):
    """Crea el panel lateral de notificaciones"""
    
    # Contenedor de la lista de notificaciones
    lista_notificaciones = ft.Column(
        controls=[],
        spacing=5,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    def actualizar_lista():
        """Actualiza la lista de notificaciones"""
        lista_notificaciones.controls.clear()
        
        notificaciones = globals.obtener_notificaciones()
        
        if not notificaciones:
            # Mostrar mensaje cuando no hay notificaciones
            lista_notificaciones.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(
                                ft.Icons.NOTIFICATIONS_OFF,
                                size=50,
                                color="#9095a0",
                            ),
                            ft.Text(
                                "No hay notificaciones",
                                size=16,
                                color="#9095a0",
                                weight=ft.FontWeight.W_500,
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=50,
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                )
            )
        else:
            for notif in notificaciones:
                # Determinar el icono según el tipo
                iconos = {
                    "exito": ft.Icons.CHECK_CIRCLE,
                    "guardar": ft.Icons.SAVE,
                    "cancelar": ft.Icons.CANCEL,
                    "crear": ft.Icons.ADD_CIRCLE,
                    "editar": ft.Icons.EDIT,
                    "eliminar": ft.Icons.DELETE,
                }

                # Y los colores:
                colores = {
                    "exito": "#066945",
                    "guardar": "#004dd3",
                    "cancelar": "#bd0000",
                    "crear": "#066945",
                    "editar": "#004dd3",
                    "eliminar": "#bd0000",
                }
                
                # Crear tarjeta de notificación
                tarjeta = ft.Container(
                    content=ft.Row(
                        controls=[
                            # Icono
                            ft.Container(
                                content=ft.Icon(
                                    iconos.get(notif["tipo"], ft.Icons.NOTIFICATIONS),
                                    color= colores.get(notif["tipo"]),
                                    size=24,
                                ),
                                bgcolor="#ffffff",
                                border=ft.Border.all(width=1, color=colores.get(notif["tipo"])),
                                border_radius=8,
                                padding=8,
                                width=36,
                                height=36,
                                alignment=ft.Alignment.CENTER,
                            ),
                            # Contenido
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        notif["titulo"],
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color="#6b1d41",
                                    ),
                                    ft.Text(
                                        notif["mensaje"],
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color="#6b1d41",
                                    ),
                                    ft.Text(
                                        notif["fecha"],
                                        size=10,
                                        color="#9095a0",
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            # Indicador de no leída
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.CIRCLE,
                                    size=10,
                                    color="#de3b40",
                                ),
                                visible=not notif["leida"],
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor="#ffffff" if notif["leida"] else "#ffffff",
                    border=ft.Border.all(width=2, color="#e2dcd5"),
                    border_radius=8,
                    padding=10,
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
                    on_click=lambda e, nid=notif["id"]: marcar_y_actualizar(nid),
                )
                lista_notificaciones.controls.append(tarjeta)
        
        # Sincronizar el contador después de actualizar la lista
        if page and hasattr(page, 'actualizar_contador'):
            page.actualizar_contador()
        elif page:
            # Si no tiene el método, actualizar manualmente
            contador_valor = globals.contar_notificaciones_no_leidas()
            # Actualizar el contador en el encabezado si existe
            if hasattr(panel, 'contador_text'):
                panel.contador_text.value = str(contador_valor)
                panel.contador_text.visible = contador_valor > 0
        
        if page:
            page.update()
    
    def marcar_y_actualizar(notificacion_id):
        """Marca una notificación como leída y actualiza"""
        globals.marcar_como_leida(notificacion_id)
        actualizar_lista()
    
    def marcar_todas():
        """Marca todas las notificaciones como leídas"""
        globals.marcar_todas_como_leidas()
        actualizar_lista()
    
    def limpiar_todas():
        """Limpia todas las notificaciones"""
        globals.limpiar_notificaciones()
        actualizar_lista()
    
    # ========== CONTADOR DEL PANEL ==========
    contador_panel = ft.Text(
        "0",
        size=12,
        color="#ffffff",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )
    
    # Actualizar el contador del panel
    def actualizar_contador_panel():
        contador = globals.contar_notificaciones_no_leidas()
        contador_panel.value = str(contador) if contador > 0 else "0"
        contador_panel.visible = contador > 0
        return contador
    
    # ========== ENCABEZADO DEL PANEL ==========
    encabezado = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            style=ft.ButtonStyle(
                                side={
                                    ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#a11e2f"),
                                    ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#6b1d41")
                                },
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            bgcolor="#6b1d41",
                            icon_color="#ffffff",
                            on_click=lambda e: cerrar_panel() if cerrar_panel else None,
                            icon_size=24,
                            tooltip="Cerrar"
                        ),
                        ft.Text(
                            "Notificaciones",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#6b1d41",
                        ),
                        ft.Container(
                            content=contador_panel,
                            bgcolor="#de3b40",
                            border_radius=10,
                            padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                            visible=False,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.DONE_ALL,
                            icon_color="#6b1d41",
                            tooltip="Marcar todas como leídas",
                            on_click=lambda e: marcar_todas(),
                            icon_size=20,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color="#de3b40",
                            tooltip="Limpiar todas",
                            on_click=lambda e: limpiar_todas(),
                            icon_size=20,
                        ),
                    ],
                    spacing=0,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.Padding.symmetric(vertical=15, horizontal=20),
        bgcolor="#f9f6f0",
    )
    
    # Guardar referencia al contador en el panel
    panel = ft.Container(
        content=ft.Column(
            controls=[
                encabezado,
                ft.Container(
                    content=lista_notificaciones,
                    expand=True,
                    padding=10,
                    bgcolor="#f9f6f0",
                ),
            ],
            spacing=0,
            expand=True,
        ),
        width=380,
        height=1000,
        bgcolor="#ffffff",
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
        ),
    )
    
    # Guardar referencia al contador en el panel
    panel.contador_text = contador_panel
    
    # Actualizar el contador inicial
    actualizar_contador_panel()
    actualizar_lista()
    
    return panel