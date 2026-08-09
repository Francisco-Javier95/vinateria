import flet as ft
import threading
import time

class ToastNotification:
    
    def __init__(self, page):
        self.page = page
        self.container = ft.Column(
            controls=[],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        )
        
        self.floating_container = ft.Container(
            content=self.container,
            right=20,
            top=20,
            width=380,
        )
        
        if self.floating_container not in page.overlay:
            page.overlay.append(self.floating_container)
    
    def mostrar_toast(self, titulo, mensaje, tipo="crear", duracion=1):
        colores = {
            "exito": {"color": "#066945", "icono": ft.Icons.ADD, "badge": "NUEVO"},
            "crear": {"color": "#066945", "icono": ft.Icons.ADD, "badge": "NUEVO"},
            "editar": {"color": "#004dd3", "icono": ft.Icons.EDIT, "badge": "EDITADO"},
            "eliminar": {"color": "#bd0000", "icono": ft.Icons.DELETE, "badge": "ELIMINADO"},
            "info": {"color": "#2196F3", "icono": ft.Icons.INFO, "badge": None}
        }
        
        color = colores.get(tipo, colores["info"])
        
        # ========== TARJETA COMO EL EJEMPLO ==========
        card = ft.Container(
            padding=12,
            border_radius=8,
            bgcolor="#ffffff",
            border=ft.Border.all(1, "#e8e4e0"),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            ),
            width=380,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # Icono + Texto
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    color["icono"],
                                    color=color["color"],
                                    size=20,
                                ),
                                bgcolor=ft.Colors.with_opacity(0.12, color["color"]),
                                border_radius=8,
                                padding=10,
                            ),
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        titulo,
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color="#1e1e1e",
                                    ),
                                    ft.Text(
                                        mensaje,
                                        size=12,
                                        color="#424955",
                                    ),
                                ],
                            ),
                        ],
                        spacing=10,
                    ),
                ],
            ),
        )
        
        # Contenedor con animación de entrada
        toast_container = ft.Container(
            content=card,
            opacity=0,
            margin=ft.Margin.only(bottom=6),
        )
        
        self.container.controls.insert(0, toast_container)
        
        # Animar entrada
        toast_container.opacity = 1
        self.page.update()
        
        # ========== ELIMINAR COMPLETAMENTE DESPUÉS DE LA DURACIÓN ==========
        def auto_eliminar():
            time.sleep(duracion)
            if toast_container in self.container.controls:
                self.container.controls.remove(toast_container)
                self.page.update()
                    
        
        threading.Thread(target=auto_eliminar, daemon=True).start()
        
        return toast_container