import flet as ft
from ui.inicio_sesion import inicio_sesion
from ui.restablecer_contrasenia import restablecer_contrasenia
from ui.main_window import main_window
import globals

def main(page: ft.Page):
    # Configuración de la página
    page.title = "La Vinata - Sistema de Punto de Venta"
    page.window_width = 1100
    page.window_height = 700
    page.padding = 0
    page.bgcolor = "#F9F6F0"

    # Variable para almacenar el contenido actual
    contenido_actual = ft.Container(
        expand=True,
        gradient = ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=["#c8377b", "#6b1d41", "#6b1d41"],
            stops=[0.0, 0.5, 1.0],
        ),
        height = 5000
    )

    # ========== FUNCIÓN PARA MOSTRAR SNACKBAR ==========
    def mostrar_snackbar(mensaje, tipo="exito", duracion=3000):
        # Configuraciones según tipo
        configs = {
            "exito": {
                "bg": "#ffffff", 
                "icon": ft.Icons.CHECK_CIRCLE,
                "icon_color": "#066945"
            },
            "guardar": {
                "bg": "#ffffff", 
                "icon": ft.Icons.SAVE,
                "icon_color": "#004dd3"
            },
            "cancelar": {
                "bg": "#ffffff", 
                "icon": ft.Icons.CANCEL,
                "icon_color": "#bd0000"
            },
            "crear": {
                "bg": "#ffffff", 
                "icon": ft.Icons.ADD_CIRCLE,
                "icon_color": "#066945"
            },
            "editar": {
                "bg": "#ffffff", 
                "icon": ft.Icons.EDIT,
                "icon_color": "#004dd3"
            },
            "eliminar": {
                "bg": "#ffffff", 
                "icon": ft.Icons.DELETE,
                "icon_color": "#bd0000"
            },
            "error": {
                "bg": "#ffffff", 
                "icon": ft.Icons.ERROR,
                "icon_color": "#ff0000"
            },
            "advertencia": {
                "bg": "#ffffff", 
                "icon": ft.Icons.WARNING,
                "icon_color": "#FF9800"
            },
            "info": {
                "bg": "#ffffff", 
                "icon": ft.Icons.INFO,
                "icon_color": "#2196F3"
            }
        }
        
        config = configs.get(tipo, configs["info"])
        
        # Crear el SnackBar
        snackbar = ft.SnackBar(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        config["icon"],
                        color=config["icon_color"],
                        size=24,
                    ),
                    ft.Text(
                        mensaje,
                        color="#6b1d41",
                        size=16,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor =config["bg"],
            duration=duracion,
            behavior=ft.SnackBarBehavior.FLOATING,
            shape=ft.RoundedRectangleBorder(radius=10),
            margin=ft.Margin.only(top=20, left=20, right=20),
            width = 550,
            elevation=6,
        )
        
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()
    
    # Registrar la función en globals
    globals.mostrar_snackbar = mostrar_snackbar

    # ============================================================
    # === FUNCIÓN PARA CERRAR SESIÓN ===
    # ============================================================
    def cerrar_sesion(e):
        # Limpiar la variable global
        globals.limpiar_sesion()
        mostrar_login()

    # ============================================================
    # === FUNCIONES PARA CAMBIAR DE VISTA ===
    # ============================================================
    def mostrar_login():
        """Muestra la pantalla de inicio de sesión"""
        contenido_actual.content = inicio_sesion(page, ir_restablecer, login_exitoso)
        page.update()

    def mostrar_restablecer():
        """Muestra la pantalla de restablecer contraseña"""
        contenido_actual.content = restablecer_contrasenia(page, volver_login)
        page.update()

    def mostrar_main_window():
        """Muestra la ventana principal de la aplicación"""
        contenido_actual.content = main_window(page, cerrar_sesion)
        page.update()

    # ============================================================
    # === CALLBACKS PARA NAVEGACIÓN ===
    # ============================================================
    def ir_restablecer(e):
        """Navega a la pantalla de restablecer contraseña"""
        mostrar_restablecer()

    def volver_login(e):
        """Vuelve a la pantalla de login"""
        mostrar_login()

    def login_exitoso(usuario):
        """Se ejecuta cuando el login es exitoso"""
        mostrar_main_window()

    # ============================================================
    # === CONSTRUIR LA INTERFAZ ===
    # ============================================================
    page.add(contenido_actual)
    mostrar_login()

if __name__ == "__main__":
    ft.app(target=main)