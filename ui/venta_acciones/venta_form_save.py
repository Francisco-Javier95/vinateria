import flet as ft
from datetime import datetime

from models.venta import Venta
from dao.venta_dao import VentaDAO

def guardar_form(regresar=None, formulario_visible=False, cerrando_modal=None, total=0.0, lista_articulos=None, usuario_id=1, limpiar_lista=None):
    # Estilos de los label
    estilo_de_label = ft.TextStyle(
        color="#926600",
        weight=ft.FontWeight.BOLD,
        size=14
    )
    estilo_del_label_focus = ft.TextStyle(
        color="#424955",
        weight=ft.FontWeight.BOLD,
        size=14
    )

    # Variables de estado
    articulos_ids = lista_articulos if lista_articulos else []
    usuario_actual = usuario_id
    total_actual = total

    def validar_campo(e):
        """Habilita el botón cuando el campo tiene texto"""
        if nombre_input.value and nombre_input.value.strip() != "":
            boton_guardar.disabled = False
        else:
            boton_guardar.disabled = True
        e.page.update()

    # Función/metodo para guardar la venta
    def guardar_venta(evento):
        try:
            # Guardar el valor del campo "nombre_input"
            nombre = nombre_input.value.strip() if nombre_input.value else ""

            # Crear el nombre completo de la venta
            venta_nombre = f"VEN-{nombre}-VINATA"

            # Convertir lista de IDs a formato PostgreSQL (array)
            articulos_array = "{" + ",".join(str(id) for id in articulos_ids) + "}"

            # Estado de la venta (Pendiente por defecto)
            estado = "Pendiente"

            # Crear objeto Venta
            nueva_venta = Venta(
                venta_id=None,
                venta_venta=venta_nombre,
                venta_fecha=None,
                venta_ganancia=total_actual,
                venta_usuario=usuario_actual,
                venta_articulo=articulos_array,
                venta_estado=estado
            )

            # Insertar en la base de datos
            venta_dao = VentaDAO()
            venta_dao.insertar(nueva_venta)


            # === LIMPIAR LISTA Y CERRAR MODAL ===
            import time
            time.sleep(0.5)

            # Ejecutar el callback para limpiar la lista
            if limpiar_lista:
                limpiar_lista()

            # Cerrar el modal
            if formulario_visible and cerrando_modal:
                cerrando_modal()
                return

        except Exception as error:
            print(f"Error al guardar la venta: {error}")
            evento.page.update()

    # --------- Interfaz -----------------

    # Campo de nombre
    nombre_input = ft.TextField(
        label="Nombre: ",
        label_style=estilo_de_label,
        on_focus=lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(),
        on_blur=lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        on_change=validar_campo,  # <--- Validar en tiempo real
        hint_text="Miguel_8_vinos",
        focused_border_color="#c9a03d",
        expand=True,
        color="#424955"
    )

    # Botón guardar (inicialmente deshabilitado)
    boton_guardar = ft.ElevatedButton(
        "Guardar",
        style=ft.ButtonStyle(
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#a11e2f"),
                ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#6b1d41")
            },
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        bgcolor="#6b1d41",
        color="#ffffff",
        width=500,
        disabled=True,  # Deshabilitado hasta que se escriba
        on_click=guardar_venta
    )

    # ------------- Construir el encabezado según el modo ------------------
    controles_encabezado = []

    if formulario_visible:
        controles_encabezado.append(
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
                        on_click=lambda e: cerrando_modal() if cerrando_modal else None,
                        tooltip="Cerrar"
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Guardar venta",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color="#c9a03d"
                            )
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
            )
        )
    else:
        controles_encabezado.append(
            ft.Row(
                controls=[
                    ft.Container(
                        bgcolor="#6b1d41",
                    ),
                    ft.Text(
                        "Guardar venta",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#c9a03d"
                    ),
                ]
            )
        )

    # ------------- Construir el formulario ----------------
    contenido_formulario = ft.Column(
        controls=[
            *controles_encabezado,

            # Mensaje informativo
            ft.Row(
                controls=[
                    ft.Text(
                        spans=[
                            ft.TextSpan(
                                "En caso de no cerrar una ",
                                ft.TextStyle()
                            ),
                            ft.TextSpan(
                                "venta",
                                ft.TextStyle(weight=ft.FontWeight.BOLD)
                            ),
                            ft.TextSpan(
                                ", siempre puedes ",
                                ft.TextStyle()
                            ),
                            ft.TextSpan(
                                "guardar",
                                ft.TextStyle(weight=ft.FontWeight.BOLD)
                            ),
                            ft.TextSpan(
                                " la lista de productos del cliente para después",
                                ft.TextStyle()
                            )
                        ],
                        text_align=ft.TextAlign.CENTER,
                        size=16,
                        width=400,
                        color="#9095a0"
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER
            ),

            nombre_input,

            boton_guardar,
        ],
        spacing=15,
        width=300,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ---------------- Envolver en un contenedor con estilo ----------------
    if formulario_visible:
        return ft.Container(
            content=contenido_formulario,
            bgcolor="#ffffff",
            border_radius=20,
            padding=30,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.BLACK_38
            ),
            width=500,
        )
    else:
        return ft.Container(
            padding=30,
            content=contenido_formulario,
            expand=True
        )