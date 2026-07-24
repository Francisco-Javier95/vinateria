import flet as ft

from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO
from dao.privilegio_dao import PrivilegioDAO

def usuario_form_edit(regresar = None, formulario_visible = False, cerrando_modal = None, registro = None):
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
    usuario_input = ft.TextField(
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
    nuempleado_input = ft.TextField(
        label = "Número empleado: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "1",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('numero_empleado') if registro else "" # Cargar datos
    )
    correo_input = ft.TextField(
        label = "Correo electrónico: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "ejemplo@gmail.com",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('correo') if registro else "" # Cargar datos
    )
    contrasenia_input = ft.TextField(
        label = "Contraseña: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "********",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('contrasenia') if registro else "" # Cargar datos
    )

    # --------- Dropdown para categorìas ---------
    privilegio_input = ft.Dropdown(
        label = "Privilegio: ",
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        tooltip = "Selecciona un privilegio...",
        options = [], # Mostrar los privilegios
        expand = True,
        menu_height = 135, # ALTURA MÁXIMA (5 items aprox)

        color = "#6b1d41", # Color del texto
        fill_color = ft.Colors.WHITE, # Fondo del campo (requiere filled = True o estilo)
        filled = True, # Activa el relleno
        border_color = "#916500", # Color del borde
        focused_border_color = "#c9a03d", # Borde al enfocar
        bgcolor = "#f9f6f0", # Fondo del menú desplegable

        value = registro.get('privilegio_id') if registro else None # Cargar datos
    )

    # Metodo para cargar los privilegios desde la Base de Datos
    def cargar_privilegios():
        try:
            privilegio_nombre_dao = PrivilegioDAO()
            privilegios = privilegio_nombre_dao.nombres_privilegios()

            privilegio_input.options.clear() # Limpia las opciones del dropdown

            valor_privilegio = 1
            for privilegio in privilegios:
                privilegio_input.options.append(
                    ft.dropdown.Option(
                        key = valor_privilegio,
                        text = privilegio.privilegio_privilegio,
                        style = ft.TextStyle(
                            color = "#6b1d41",
                            size = 14
                        )
                    ),
                )
                valor_privilegio = valor_privilegio + 1
            # Si hay privilegios, seleccionar la primera por defecto
            if privilegio_input.options:
                if registro and registro.get('privilegio_id'):
                    # Buscar la privilegio que coincida
                    for option in privilegio_input.options:
                        if option.key == registro.get('privilegio_id'):
                            privilegio_input.value = option.key
                            break
                else:
                    privilegio_input.value = privilegio_input.options[0].key

        except Exception as error:
            mensaje.value = f"Error al consultar los privilegios: {error}"
            mensaje.color = ft.Colors.RED
    

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    # # -------------- Función para limpiar el formulario -------------------
    # def limpiar_formualrio():
    #   usuario_input.value = ""
    #   apaterno_input.value = ""
    #   amaterno_input.value = ""
    #   nuempleado_input.value = ""
    #   correo_input.value = ""
    #   contrasenia_input.value = ""
    #   privilegio_input.value = privilegio_input.options[0].key if privilegio_input.options else ""

    def editar_usuario(evento):
        # Recuperar los valores de los TextFile
        usuario_usuario = usuario_input.value
        usuario_apaterno = apaterno_input.value
        usuario_amaterno = amaterno_input.value
        usuario_nuempleado = nuempleado_input.value
        usuario_correo = correo_input.value
        usuario_contrasenia = contrasenia_input.value
        usuario_privilegio = privilegio_input.value

        # Validación de campos vacíos
        if usuario_usuario == "" or usuario_apaterno == "" or usuario_amaterno == "" or usuario_nuempleado == "" or usuario_correo == "" or usuario_contrasenia == "" or usuario_privilegio == None:
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            # Actualizar la interfaz para mostrar el mensaje
            evento.page.update()
            return
        try:
            usuario_dao = UsuarioDAO()
            usuario_id = registro.get('id') if registro else None

            editar_usuario = Usuario(
                usuario_id = usuario_id,
                usuario_usuario = usuario_usuario,
                usuario_apaterno = usuario_apaterno,
                usuario_amaterno = usuario_amaterno,
                usuario_nuempleado = int(usuario_nuempleado), # Convertir a numero entero
                usuario_correo = usuario_correo,
                usuario_contrasenia = usuario_contrasenia,
                usuario_privilegio = int(usuario_privilegio) # Convertir a numero entero-
            )

            print(usuario_id, usuario_usuario, usuario_apaterno, usuario_amaterno, usuario_nuempleado, usuario_correo, usuario_contrasenia, usuario_privilegio)

            usuario_dao.actualizar(editar_usuario)

            mensaje.value = f"Usuario {usuario_usuario} ha sido editado exitosamente"
            mensaje.color = ft.Colors.GREEN
            
            # limpiar_formualrio()

            # # ---------------------- Si el modal esta activo y si existe la función para cerrar
            # if formulario_visible and cerrando_modal:
            #     evento.page.update()
            #     cerrando_modal()
            #     return

        except Exception as error:
            mensaje.value = f"Error al insertar el usuario: {error}"
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
                                "Editar usuario",
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
            usuario_input,

            # Fila 2: Apellido materno
            amaterno_input,

            # Fila 3: Correo electrónico
            correo_input,

            # Fila 4: Privilegio
            privilegio_input
        ],
        spacing = 15,
        expand = True
    )

    # ----------- Columna derecha --------------------
    columna_derecha = ft.Column(
        controls = [
            # Fila 1: Apellido paterno
            apaterno_input,

            # Fila 2: Número de empleado
            nuempleado_input,

            # Fila 3: Contreseña
            contrasenia_input,

            # Fila 4: Bóton de registrar
            ft.ElevatedButton(
                "Editar",
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
                on_click = editar_usuario,
                width = 600
            ),

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
        ), 
    )
    # =============== FIN Distribución del formulario en dos columnas ===============

    
    # ------------- Construir el formulario ----------------
    contenido_formulario = ft.Column(
        controls = [
            *controles_encabezado, # El * desempaqueta la lista

            ft.Row(
                controls = [
                    ft.Text(
                        spans=[
                            ft.TextSpan(
                                "Edita",
                                ft.TextStyle(weight = ft.FontWeight.BOLD) # Estilo en negrita
                            ),
                            ft.TextSpan(
                                " la información de los ",
                                ft.TextStyle()  # Este texto es normal
                            ),
                            ft.TextSpan(
                                "usuarios",
                                ft.TextStyle(weight = ft.FontWeight.BOLD) # Estilo en negrita
                            ),
                            ft.TextSpan(
                                " cuando quieras",
                                ft.TextStyle()  # Este texto es normal
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
            
            contenido_dos_columnas,

            mensaje
        ],
        spacing = 15,
        expand = True
    )

    # Cargar los privilegios
    cargar_privilegios()

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
    