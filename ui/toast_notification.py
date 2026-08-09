# ui/toast_notification.py

import flet as ft
import threading
import time

class ToastNotification:
    """Clase para manejar notificaciones tipo toast en la esquina superior derecha"""
    
    def __init__(self, page):
        self.page = page
        self.toasts_activos = []
        self.container = ft.Column(
            controls=[],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        )
        
        # Contenedor flotante en la esquina superior derecha
        self.floating_container = ft.Container(
            content=self.container,
            right=20,
            top=20,
            width=400,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        # Agregar a la página (solo una vez)
        if self.floating_container not in page.overlay:
            page.overlay.append(self.floating_container)
    
    def mostrar_toast(self, titulo, mensaje, tipo="crear", duracion=7):
        # Configurar colores según el tipo
        colores = {
            "crear": {"bg": "#ffffff", "borde": "#e2dcd5", "color": "#066945", "icono": ft.Icons.ADD},
            "eliminar": {"bg": "#ffffff", "borde": "#e2dcd5", "color": "#bd0000", "icono": ft.Icons.MODE_EDIT},
            "editar": {"bg": "#ffffff", "borde": "#e2dcd5", "color": "#004dd3", "icono": ft.Icons.DELETE},
            "info": {"bg": "#ffffff", "borde": "#e2dcd5", "color": "#066945", "icono": ft.Icons.INFO}
        }
        
        color = colores.get(tipo, colores["crear"])
        
        # Variable para controlar la animación de la barra
        barra_ancho = ft.Container(
            width=0,
            height=4,
            bgcolor="#c9a03d",
            border_radius=ft.BorderRadius.only(
                bottom_left=5,
                bottom_right=5,
            ),
            animate=ft.Animation(100, ft.AnimationCurve.LINEAR),
        )
        
        # Contenedor de la barra (fondo)
        barra_fondo = ft.Container(
            content=barra_ancho,
            width=400,
            height=4,
            bgcolor=ft.Colors.with_opacity(0.3, "#ffffff"),
            border_radius=ft.BorderRadius.only(
                bottom_left=5,
                bottom_right=5,
            ),
        )
        
        # Crear el toast
        toast = ft.Container(
            content=ft.Column(
                controls=[
                    # Contenido principal
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                # Icono
                                ft.Container(
                                    content=ft.Icon(
                                        color["icono"],
                                        color=color["color"],
                                        size=28,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.2, "#ffffff"),
                                    border_radius=8,
                                    padding=8,
                                ),
                                # Textos
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            titulo,
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color="#6b1d41",
                                        ),
                                        ft.Text(
                                            mensaje,
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.with_opacity(0.9, "#6b1d41"),
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                # Botón cerrar
                                ft.IconButton(
                                    icon = ft.Icons.CLOSE,
                                    style = ft.ButtonStyle(
                                        bgcolor = {
                                            ft.ControlState.DEFAULT: "#ffffff",
                                            ft.ControlState.HOVERED: "#c9a03d",
                                        },
                                        side = {
                                            ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#e2dcd5"),
                                            ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#926600"),
                                        },
                                        icon_color = {
                                            ft.ControlState.DEFAULT: "#c9a03d",
                                            ft.ControlState.HOVERED: "#ffffff",
                                        },
                                        shape = ft.RoundedRectangleBorder(radius = 10),
                                        padding = ft.Padding.symmetric(horizontal = 8, vertical = 8)
                                    ),
                                    height = 40,
                                    width = 40,
                                    align = ft.Alignment.CENTER,
                                    tooltip = "Cerrar",

                                    on_click=lambda e: self.cerrar_toast(toast),
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.Padding.symmetric(vertical=12, horizontal=15),
                    ),
                    # Barra de progreso
                    barra_fondo,
                ],
                spacing=0,
            ),
            bgcolor=color["bg"],
            border=ft.Border.all(1, color["borde"]),
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            ),
            width=400,
            animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
            opacity=0,
            scale=ft.Scale(0.8),
        )
        
        # Agregar el toast al contenedor
        self.container.controls.insert(0, toast)
        
        # Guardar referencia para la animación de la barra
        toast.barra_ancho = barra_ancho
        toast.barra_fondo = barra_fondo
        
        # Animar entrada
        toast.opacity = 1
        toast.scale = ft.Scale(1)
        self.page.update()
        
        # Animar la barra (el ancho aumentará progresivamente)
        def animar_barra():
            # Esperar un momento antes de iniciar la barra
            time.sleep(0.3)
            
            # Calcular incrementos para la barra
            steps = 50
            incremento = 400 / steps  # Ancho total de la barra
            paso = duracion / steps  # Tiempo por paso
            
            for i in range(steps + 1):
                if toast not in self.container.controls:
                    break
                try:
                    barra_ancho.width = i * incremento
                    self.page.update()
                except:
                    break
                time.sleep(paso)
            
            # Cerrar el toast automáticamente después de la animación
            if toast in self.container.controls:
                self.cerrar_toast(toast)
        
        # Iniciar la animación en un hilo separado
        hilo = threading.Thread(target=animar_barra, daemon=True)
        hilo.start()
        
        # Guardar referencia del hilo
        toast.hilo = hilo
        
        return toast
    
    def cerrar_toast(self, toast):
        """Cierra un toast específico con animación"""
        if toast not in self.container.controls:
            return
        
        # Detener el hilo si existe
        if hasattr(toast, 'hilo'):
            # No podemos detener el hilo directamente, pero podemos marcar que ya no se actualice
            toast.hilo = None
        
        # Animar salida
        toast.opacity = 0
        toast.scale = ft.Scale(0.8)
        self.page.update()
        
        # Eliminar después de la animación
        time.sleep(0.4)
        if toast in self.container.controls:
            self.container.controls.remove(toast)
            self.page.update()
        
        threading.Thread(daemon=True).start()
    
    def cerrar_todas(self):
        """Cierra todos los toasts activos"""
        for toast in self.container.controls.copy():
            self.cerrar_toast(toast)