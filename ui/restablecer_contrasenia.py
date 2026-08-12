import flet as ft
from dao.usuario_dao import UsuarioDAO
import hashlib

import globals

def restablecer_contrasenia(page: ft.Page, on_volver):

    # Estilos de los label
    estilo_de_label = ft.TextStyle(
        color = "#926600", 
        weight = ft.FontWeight.BOLD,
        size = 14
    )
    estilo_del_label_focus = ft.TextStyle(
        color = "#424955", 
        weight = ft.FontWeight.BOLD,
        size = 14
    )

    # ------------ Campos del formulario ------------------
    correo_input = ft.TextField(
        label="Correo electrónico",
        hint_text="ejemplo@correo.com", # Esto es el placeholder

        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        keyboard_type=ft.KeyboardType.EMAIL,
    )

    nuempleado_input = ft.TextField(
        label="Número de empleado",
        # value = "1",
        hint_text="12345", # Esto es el placeholder

        # Habre un: Teclado numerico con decimal en telefonos o tablets
        keyboard_type=ft.KeyboardType.NUMBER,
        # Filtro para permitir solo numeros con . para decimales
        input_filter=ft.InputFilter(
            allow=True,
            regex_string = r"^[0-9]*$",  # Permite números y punto decimal
            replacement_string = ""
        ),
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(),
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",
    )

    nueva_contrasenia_input = ft.TextField(
        label="Nueva contraseña",
        hint_text="********",
        password=True,
        can_reveal_password=True,

        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",
    )

    confirmar_contrasenia_input = ft.TextField(
        label="Confirmar contraseña",
        hint_text="********",
        password=True,
        can_reveal_password=True,

        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",
        
        on_submit=lambda e: restablecer(e),
    )

    mensaje = ft.Text("", color=ft.Colors.RED, size=14)

    # === FUNCIÓN PARA RESTABLECER CONTRASEÑA ===
    def restablecer(e):
        correo = correo_input.value.strip() if correo_input.value else ""
        nuempleado = nuempleado_input.value.strip() if nuempleado_input.value else ""
        nueva_contrasenia = nueva_contrasenia_input.value.strip() if nueva_contrasenia_input.value else ""
        confirmar_contrasenia = confirmar_contrasenia_input.value.strip() if confirmar_contrasenia_input.value else ""

        # Obtener la función de SnackBar
        snackbar_func = globals.obtener_snackbar()

        if not correo or not nuempleado or not nueva_contrasenia or not confirmar_contrasenia:
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            page.update()
            return

        if nueva_contrasenia != confirmar_contrasenia:
            mensaje.value = "Las contraseñas no coinciden"
            mensaje.color = ft.Colors.RED
            page.update()
            return

        if len(nueva_contrasenia) < 8:
            mensaje.value = "La contraseña debe tener al menos 8 caracteres"
            mensaje.color = ft.Colors.RED
            page.update()
            return

        try:
            usuario_dao = UsuarioDAO()
            usuario = usuario_dao.obtener_por_correo_y_empleado(correo, int(nuempleado))

            if usuario is None:
                mensaje.value = "No se encontró un usuario con esos datos"
                mensaje.color = ft.Colors.RED
                page.update()
                return

            nuevo_hash = hashlib.sha256(nueva_contrasenia.encode()).hexdigest()
            usuario_dao.actualizar_contrasenia(usuario.usuario_id, nuevo_hash)

            # mensaje.value = "Contraseña actualizada exitosamente"
            mensaje.color = ft.Colors.GREEN

            # ===== MOSTRAR SNACKBAR DE ÉXITO =====
            if snackbar_func:
                snackbar_func(f"Contraseña restablecida exitosamente", "exito")
            
            # ===== AGREGAR NOTIFICACIÓN AL SISTEMA =====
            globals.agregar_notificacion(
                titulo=f"Contraseña de '{usuario.usuario_usuario}'",
                mensaje="restablecida exitosamente",
                tipo="exito"
            )

            # Actualizar el contador de notificaciones
            try:
                if page and hasattr(page, 'actualizar_contador'):
                    page.actualizar_contador()
            except:
                pass

            page.update()

            import time
            time.sleep(1)
            on_volver(None)

        except ValueError:
            mensaje.value = "El número de empleado debe ser un número válido"
            mensaje.color = ft.Colors.RED
            page.update()
        except Exception as error:
            mensaje.value = f"Error al restablecer contraseña: {error}"
            mensaje.color = ft.Colors.RED
            page.update()

    
    titulo = ft.Text(
        "Restablecer Contraseña",
        size = 28,
        weight=ft.FontWeight.BOLD,
        color="#c9a03d",
        text_align = ft.TextAlign.CENTER
    )

    subtitulo = ft.Text(
        spans = [
            ft.TextSpan(
                "Tranquilo, ",
                ft.TextStyle()  # Estilo en normal
            ),
            ft.TextSpan(
                "con los datos correctos",
                ft.TextStyle(weight = ft.FontWeight.BOLD)  # Este texto sera en NEGRITA
            ),
            ft.TextSpan(
                ", puedes ",
                ft.TextStyle()  # Estilo en normal
            ),
            ft.TextSpan(
                "restablecer tu contraseña",
                ft.TextStyle(weight = ft.FontWeight.BOLD)  # Este texto sera en NEGRITA
            ),
        ],
        size=14,
        color="#9095a0",
        text_align = ft.TextAlign.CENTER
    )

    btn_restablecer = ft.ElevatedButton(
        "Restablecer contraseña",
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
        on_click=restablecer,
    )

    link_volver = ft.TextButton(
        "Inicio sesión",
        style=ft.ButtonStyle(color="#c9a03d"),
        on_click=on_volver,
    )

    contenedor_restablecer = ft.Container(
        content=ft.Column(
            controls=[
                titulo,
                subtitulo,
                ft.Divider(height=20, color="transparent"),
                correo_input,
                nuempleado_input,
                ft.Column(
                    controls = [
                        nueva_contrasenia_input,
                        ft.Text("8+ caracteres", size = 16, color = "#9095a0")
                    ],
                    spacing = 0
                ),
                confirmar_contrasenia_input,
                mensaje,
                btn_restablecer,
                link_volver,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#ffffff",
        border_radius=10,
        padding=30,
        width=450,
        height=600,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.BLACK12,
        ),
    )

    return ft.Container(
        content=contenedor_restablecer,
        alignment=ft.Alignment.CENTER,
        expand=True,
    )