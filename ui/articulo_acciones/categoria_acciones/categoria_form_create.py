import flet as ft

from models.categoria import Categoria
from dao.categoria_dao import CategoriaDAO

def categoria_form_create(regresar = None, tabla_categoria_visible = False, cerrando_modal = None):
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
    categoria_input = ft.TextField(
        label = "Nombre: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Tinto",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955"
    )
    # --------- Dropdown para tipos ---------
    tipo_input = ft.Dropdown(
        label = "Tipo: ",
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(),
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        tooltip = "Selecciona un tipo...",
        # Mostrar tipos
        options = [
            ft.dropdown.Option(
                "Vino",
                style = ft.TextStyle(
                    color = "#6b1d41",
                    size = 14
                )                
            ),
            ft.dropdown.Option(
                "Licor",
                style = ft.TextStyle(
                    color = "#6b1d41",
                    size = 14
                )                
            )
        ], 
        expand = True,
        menu_height = 90, # ALTURA MÁXIMA (5 items aprox)

        color = "#6b1d41", # Color del texto
        fill_color = ft.Colors.WHITE, # Fondo del campo (requiere filled = True o estilo)
        filled = True, # Activa el relleno
        border_color = "#916500", # Color del borde
        focused_border_color = "#c9a03d", # Borde al enfocar
        bgcolor = "#f9f6f0", # Fondo del menú desplegable

        value = "Vino"
    )

    # ------------ Campos del formulario ------------------
    descripcion_input = ft.TextField(
        label = "Descripción: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Descripción breve de la categoría",  # Esto es el placeholder
        multiline = True, # Permite múltiples líneas
        min_lines = 2, # Muestra al menos 3 líneas
        max_lines = 5, # Muestra hasta 5 líneas antes de scroll
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955"
    )
    

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    # -------------- Función para limpiar el formulario -------------------
    def limpiar_formulario():
        categoria_input.value = ""
        tipo_input.value = ""
        descripcion_input.value = ""

    def guardar_usuario(evento):
        # Recuperar los valores de los TextFile
        categoria_categoria = categoria_input.value
        categoria_tipo = tipo_input.value
        categoria_descripcion = descripcion_input.value

        # Validación de campos vacíos
        if categoria_categoria == "" or categoria_tipo == "" or categoria_descripcion == "":
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            # Actualizar la interfaz para mostrar el mensaje
            evento.page.update()
            return
        try:
            categoria_dao = CategoriaDAO()
            categoria_id = None

            nueva_categoria = Categoria(
                categoria_id = categoria_id,
                categoria_categoria = categoria_categoria,
                categoria_tipo = categoria_tipo,
                categoria_descripcion = categoria_descripcion
            )

            categoria_dao.insertar(nueva_categoria)

            mensaje.value = f"Categoría {categoria_categoria} ha sido insertada exitosamente"
            mensaje.color = ft.Colors.GREEN
            
            limpiar_formulario()

            # # ---------------------- Si el modal esta activo y si existe la función para cerrar
            # if tabla_categoria_visible and cerrando_modal:
            #     evento.page.update()
            #     cerrando_modal()
            #     return

        except Exception as error:
            mensaje.value = f"Error al insertar la categoría: {error}"
            mensaje.value = ft.Colors.RED

        # Actualizar la interfaz para mostrar el mensaje 
        evento.page.update()
    
    # ------------- Construir el encabezado segun el modo ------------------
    controles_encabezado = []

    if tabla_categoria_visible:
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
                                "Crear categoría",
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
                        "Crear categoría",
                        size = 24,
                        weight = ft.FontWeight.BOLD,
                        color = "#c9a03d"
                    )
                ]
            )
        )
    
    # ------------- Construir el formulario ----------------
    contenido_formulario = ft.Column(
        controls = [
            *controles_encabezado, # El * desempaqueta la lista

            ft.Row(
                controls = [
                    ft.Text(
                        spans=[
                            ft.TextSpan(
                                "Puedes ",
                                ft.TextStyle()  # Estilo en normal
                            ),
                            ft.TextSpan(
                                "crear categorías",
                                ft.TextStyle(weight = ft.FontWeight.BOLD)  # Estilo en negrita
                            ),
                            ft.TextSpan(
                                " conforme a tu necesidad",
                                ft.TextStyle() # Este texto es normal
                            )
                        ],
                        text_align=ft.TextAlign.CENTER,
                        size = 16,
                        width = 300,
                        color = "#9095a0"
                    ),
                ],        
                expand = True,
                alignment = ft.MainAxisAlignment.CENTER
            ),

            # Campos
            categoria_input,
            tipo_input,
            descripcion_input,

            # Bóton de registrar
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
                on_click = guardar_usuario,
                width = 600
            ),

            mensaje
        ],
        spacing = 15,
        expand = True
    )

    # ---------------- Envolver en un contenedor con estilo ----------------
    if tabla_categoria_visible:
        
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