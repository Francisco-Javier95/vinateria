import flet as ft

from models.proveedor import Proveedor
from dao.proveedor_dao import ProveedorDAO

def proveedor_form_edit(regresar = None, formulario_visible = False, cerrando_modal = None, registro = None):
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
    proveedor_input = ft.TextField(
        label = "Nombre/s: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Jared Alan",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('nombre') if registro else "" # Cargar datos
    )
    apaterno_input = ft.TextField(
        label = "Apellido paterno: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Jared Alan",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('apellido_paterno') if registro else "" # Cargar datos
    )
    amaterno_input = ft.TextField(
        label = "Apellido materno: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Jared Alan",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('apellido_materno') if registro else "" # Cargar datos
    )
    telefono_input = ft.TextField(
        label = "Teléfono: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Jared Alan",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('telefono') if registro else "" # Cargar datos
    )
    direccion_input = ft.TextField(
        label = "Dirección: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Jared Alan",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('direccion') if registro else "" # Cargar datos
    )
    correo_input = ft.TextField(
        label = "Correo eletrónico: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Jared Alan",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('correo') if registro else "" # Cargar datos
    )
    

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    # # -------------- Función para limpiar el formulario -------------------
    # def limpiar_formualrio():
    #   proveedor_input.value = ""
    #   apaterno_input.value = ""
    #   amaterno_input.value = ""
    #   telefono_input.value = ""
    #   direccion_input.value = ""
    #   correo_input.value = ""

    def editar_proveedor(evento):
        # Recuperar los valores de los TextFile
        proveedor_proveedor = proveedor_input.value
        proveedor_apaterno = apaterno_input.value
        proveedor_amaterno = amaterno_input.value
        proveedor_telefono = telefono_input.value
        proveedor_direccion = direccion_input.value
        proveedor_correo = correo_input.value

        # Validación de campos vacíos
        if proveedor_proveedor == "" or proveedor_apaterno == "" or proveedor_amaterno == "" or proveedor_telefono == "" or proveedor_direccion == "" or proveedor_correo == "":
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            # Actualizar la interfaz para mostrar el mensaje
            evento.page.update()
            return
        try:
            proveedor_dao = ProveedorDAO()
            proveedor_id = registro.get('id') if registro else None

            editar_proveedor = Proveedor(
                proveedor_id = proveedor_id,
                proveedor_proveedor = proveedor_proveedor,
                proveedor_apaterno = proveedor_apaterno,
                proveedor_amaterno = proveedor_amaterno,
                proveedor_telefono = proveedor_telefono,
                proveedor_direccion = proveedor_direccion,
                proveedor_correo = proveedor_correo
            )

            print(proveedor_id, proveedor_proveedor, proveedor_apaterno, proveedor_amaterno, proveedor_telefono, proveedor_direccion, proveedor_correo)

            proveedor_dao.actualizar(editar_proveedor)

            mensaje.value = f"Proveedor {proveedor_proveedor} ha sido editado exitosamente"
            mensaje.color = ft.Colors.GREEN
            
            # limpiar_formualrio()

            # # ---------------------- Si el modal esta activo y si existe la función para cerrar
            # if formulario_visible and cerrando_modal:
            #     evento.page.update()
            #     cerrando_modal()
            #     return

        except Exception as error:
            mensaje.value = f"Error al insertar el proveedor: {error}"
            mensaje.value = ft.Colors.RED

        # Actualizar la interfaz para mostrar el mensaje 
        evento.page.update()
    
    # ------------- Construir el encabezado segun el modo ------------------
    controles_encabezado = []

    if formulario_visible:
        # Mostrar el titulo con el boton de cerrar
        controles_encabezado.append(
            ft.Row(
                controls = [
                    ft.IconButton(
                        icon = ft.Icons.CLOSE,
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
                            shape = ft.RoundedRectangleBorder(radius = 10)
                        ),
                        bgcolor = "#6b1d41",
                        icon_color = "#ffffff",
                        on_click = lambda e: cerrando_modal(),

                        tooltip = "Cerrar" # Texto que aparece al pasar el cursor
                    ),
                    ft.Row(
                        controls = [
                            ft.Text(
                                "Editar proveedor",
                                size = 24,
                                weight = ft.FontWeight.BOLD,
                                color = "#c9a03d"
                            )
                        ],
                        expand = True,
                        alignment = ft.MainAxisAlignment.CENTER
                    )
                ],
                # alignment = ft.MainAxisAlignment.SPACE_BETWEEN 
            )
        )
    else:
        # ------------- Modo normal ---------------------
        controles_encabezado.append(
            ft.Row(
                controls = [
                    ft.Container(
                        # ft.OutlinedButton(
                        #     "",
                        #     icon = ft.Icons.ARROW_BACK,
                        #     icon_color = "#ffffff",
                        #     on_click = lambda e: regresar()
                        # ),
                        bgcolor = "#6b1d41",
                    ),
                    ft.Text(
                        "Editar proveedor",
                        size = 24,
                        weight = ft.FontWeight.BOLD,
                        color = "#c9a03d"
                    ),
                ]
            )
        )

    # =============== Distribución del formulario en dos columnas ===============
    # ------------ Columna izquierda -------------------------
    columna_izquierda = ft.Column(
        controls = [
            # Fila 1: Nombre/s
            proveedor_input,
    
            # Fila 2: Apellido materno
            amaterno_input,
    
            # Fila 3: Dirección
            direccion_input
        ],
        spacing = 15,
        expand = True
    )
    
    # ----------- Columna derecha --------------------
    columna_derecha = ft.Column(
        controls = [
            # Fila 1: Apellido paterno
            apaterno_input,
    
            # Fila 2: Teléfono
            telefono_input,
    
            # Fila 3: Correo eletrónico
            correo_input,
        ],
        spacing = 15,
        expand = True
    )

    # ----------- Contenedor principal con dos columnas ---------------
    contenido_dos_columnas = ft.Column(
        ft.Row(
            controls = [
                columna_izquierda,
                columna_derecha,
            ],
            spacing = 20,
            expand = True,
            vertical_alignment = ft.CrossAxisAlignment.START
        )
    )
    # =============== FIN Distribución del formulario en dos columnas ===============

    
    # ------------- Construir el formulario ----------------
    contenido_formulario = ft.Column(
        controls = [
            *controles_encabezado, # El * desempaqueta la lista

            ft.Row(
                controls = [
                    ft.Text(
                        spans=[ # Edita la información de tus proveedores
                            ft.TextSpan(
                                "Edita",
                                ft.TextStyle(weight = ft.FontWeight.BOLD)  # Estilo en negrita
                            ),
                            ft.TextSpan(
                                " la información de tus ",
                                ft.TextStyle() # Este texto es normal
                            ),
                            ft.TextSpan(
                                "proveedores",
                                ft.TextStyle(weight = ft.FontWeight.BOLD)  # Estilo en negrita
                            )
                        ],
                        text_align=ft.TextAlign.CENTER,
                        size = 16,
                        width = 200,
                        color = "#9095a0"
                    ),
                ],        
                expand = True,
                alignment = ft.MainAxisAlignment.CENTER
            ),
            
            contenido_dos_columnas,

            # Fila 4 cnetral: Boton Registrar
            ft.Row(
                controls = [
                    ft.ElevatedButton(
                        "Registrar",
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
                        on_click = editar_proveedor
                    ),
                ],
                spacing = 10,
                expand = True
            ),

            mensaje
        ],
        spacing = 15,
        expand = True
    )

    # ---------------- Envolver en un contenedor con estilo ----------------
    if formulario_visible:
        
        return ft.Container(
            content = contenido_formulario,
            bgcolor = "#ffffff",
            border_radius = 20,
            padding = 30,
            shadow = ft.BoxShadow(
                spread_radius = 1, # Expansión de la sombra
                blur_radius = 20, #Difuminado
                color = ft.Colors.BLACK_38
            ),
            width = 500
        )
    else:
        return ft.Container(
            padding = 30,
            content = contenido_formulario,
        )
    