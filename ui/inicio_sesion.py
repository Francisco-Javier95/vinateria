import flet as ft
from dao.usuario_dao import UsuarioDAO
import hashlib
import globals  # Importar el módulo de variables globales

def inicio_sesion(page: ft.Page, on_restablecer, on_exito):
    # Estilos de los label
    estilo_de_label = ft.TextStyle(
        color = "#926600", 
        weight = ft.FontWeight.BOLD,
        size = 14
    )
    estilo_del_label_focus = ft.TextStyle(
        color = "#926600", 
        weight = ft.FontWeight.BOLD,
        size = 14
    )

    # --------- Campos del formulario -------------
    correo_input = ft.TextField(
        label="Correo electrónico",
        hint_text="ejemplo@correo.com",

        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_click = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        focused_border_color = "#c9a03d", # Borde al enfocar
        color = "#424955",

        fill_color = ft.Colors.WHITE, # Fondo del campo (requiere filled=True o estilo)
        filled = True, # Activa el relleno
        bgcolor = "#f9f6f0", # Fondo del menú desplegable

        expand=True,
        keyboard_type=ft.KeyboardType.EMAIL,
    )

    contrasenia_input = ft.TextField(
        label="Contraseña",
        hint_text="********",
        password=True,
        can_reveal_password=True,

        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_click = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        focused_border_color = "#c9a03d", # Borde al enfocar
        color = "#424955",

        fill_color = ft.Colors.WHITE, # Fondo del campo (requiere filled=True o estilo)
        filled = True, # Activa el relleno
        bgcolor = "#f9f6f0", # Fondo del menú desplegable

        expand=True,
        on_submit=lambda e: iniciar_sesion(e),
    )

    mensaje = ft.Text("", color=ft.Colors.RED, size=14)

    # -------------Metodo para iniciar sesion---------------
    def iniciar_sesion(e):
        correo = correo_input.value.strip() if correo_input.value else ""
        contrasenia = contrasenia_input.value.strip() if contrasenia_input.value else ""

        if not correo or not contrasenia:
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            page.update()
            return

        try:
            usuario_dao = UsuarioDAO()
            usuario = usuario_dao.obtener_por_correo(correo)

            if usuario is None:
                mensaje.value = "Correo electrónico no registrado"
                mensaje.color = ft.Colors.RED
                page.update()
                return

            contrasenia_hash = hashlib.sha256(contrasenia.encode()).hexdigest()
            if usuario.usuario_contrasenia != contrasenia_hash:
                mensaje.value = "Contraseña incorrecta"
                mensaje.color = ft.Colors.RED
                page.update()
                return

            mensaje.value = "¡Bienvenido! Redirigiendo..."
            mensaje.color = ft.Colors.GREEN
            page.update()

            # === GUARDAR USUARIO EN VARIABLE GLOBAL ===
            globals.establecer_sesion(usuario)

            import time
            time.sleep(0.5)
            on_exito(usuario)

        except Exception as error:
            mensaje.value = f"Error al iniciar sesión: {error}"
            mensaje.color = ft.Colors.RED
            page.update()

    
    titulo = ft.Text(
        "La Vinata",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="#c9a03d",
    )

    subtitulo = ft.Text(
        "¡Bienvenido a Vinatería Pichardo!",
        size=16,
        color="#9095a0",
    )

    btn_login = ft.ElevatedButton(
        "Ingresar",
        style = ft.ButtonStyle(
            # Borde sólido vino-caramelo de 2 píxeles por defecto
            side = {
                ft.ControlState.DEFAULT: 
                    ft.BorderSide(
                        width = 2,
                        color = "#a11e2f"
                    ),
                # Borde rojo de 2 píxeles al pasar el mouse
                ft.ControlState.HOVERED: 
                    ft.BorderSide(
                        width = 2,
                        color = "#6b1d41"
                    )
            },
            padding = 20,
            shape = ft.RoundedRectangleBorder(radius = 10)
        ),
        bgcolor = "#6b1d41",
        color = "#ffffff",
        expand = True,
        width = 800,
        on_click=iniciar_sesion,
    )

    link_restablecer = ft.TextButton(
        content = ft.Text(
            "Restablecer contraseña",
            style = ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE),
            color = "#c9a03d"
        ),
        on_click=on_restablecer,
    )

    contenedor_login = ft.Container(
        content=ft.Column(
            controls=[
                titulo,
                subtitulo,
                ft.Divider(height=20, color="transparent"),
                correo_input,
                contrasenia_input,
                mensaje,
                btn_login,
                link_restablecer,
            ],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=400,
        ),
        bgcolor="#ffffff",
        height = 400,
        border_radius=10,
        padding=ft.Padding.symmetric(horizontal=50, vertical=30),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.BLACK12,
        ),
    )

    return ft.Container(
        content=contenedor_login,
        alignment=ft.Alignment.CENTER,
        expand=True,
    )