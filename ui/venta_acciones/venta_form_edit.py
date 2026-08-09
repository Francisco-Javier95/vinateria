import flet as ft

from models.venta import Venta_nombre_usuario
from dao.venta_dao import VentaDAO
from dao.usuario_dao import UsuarioDAO

import globals

def venta_form_edit(regresar = None, formulario_visible = False, cerrando_modal = None, registro = None):
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
    venta_input = ft.TextField(
        label = "Nombre: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Miguel_8_Vinos",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        value = registro.get('nombre') if registro else "", # Cargar datos

        # Numero maximo de caracteres
        max_length = 39, # Limita a 39 caracteres (+ 11 de "VEN-" Y "-VINATA") / crea un contador y lo muestra debajo del input (campo)
        counter = ft.Container() # No mostrar contador
    )

    # --------- Dropdown para usuarios ---------
    usuario_input = ft.Dropdown(
        label = "Usuario: ",
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        tooltip = "Selecciona un usuario...",
        options = [], # Mostrar las categorias
        expand = True,
        menu_height = 200, # ALTURA MÁXIMA (5 items aprox)

        color = "#6b1d41", # Color del texto
        fill_color = ft.Colors.WHITE, # Fondo del campo (requiere filled=True o estilo)
        filled = True, # Activa el relleno
        border_color = "#916500", # Color del borde
        focused_border_color = "#c9a03d", # Borde al enfocar
        bgcolor = "#f9f6f0", # Fondo del menú desplegable

        value = registro.get('usuario_id') # Cargar datos
    )

    # Metodo para cargar los usuarios desde la Base de Datos
    def cargar_usuarios():
        try:
            usuario_nombre_dao = UsuarioDAO()
            usuarios = usuario_nombre_dao.nombres_usuarios()

            usuario_input.options.clear() # Limpia las opciones del dropdown

            for usuario in usuarios:
                nombre_usuario_completo = f"{usuario.usuario_usuario} {usuario.usuario_apaterno} {usuario.usuario_amaterno}"
                usuario_input.options.append(
                    ft.dropdown.Option(
                        key = usuario.usuario_id,
                        text = nombre_usuario_completo,
                        style=ft.TextStyle(
                            color="#6b1d41",
                            size=14
                        )
                    ),
                )
                # print(f"ID: {usuario.usuario_id}, Empleado: {nombre_usuario_completo}")
            # Si hay usuarios, seleccionar la primera por defecto
            if usuario_input.options:
                if registro and registro.get('usuario_id'):
                    # Buscar el usuario que coincida
                    for option in usuario_input.options:
                        if option.key == registro.get('usuario_id'):
                            usuario_input.value = option.key
                            break
                else:
                    usuario_input.value = usuario_input.options[0].key

        except Exception as error:
            mensaje.value = f"Error al consultar los usuarios: {error}"
            mensaje.color = ft.Colors.RED
    

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    # # -------------- Función para limpiar el formulario -------------------
    # def limpiar_formualrio():
    #     usuario_input.value = ""
    #     venta_input.value = ""

    def editar_venta(evento):
        # Recuperar los valores de los TextFile
        venta_venta = venta_input.value
        venta_usuario = usuario_input.value
        venta_id = registro.get('id') if registro else None

        # Obtener la función de SnackBar
        snackbar_func = globals.obtener_snackbar()

        # Validación de campos vacíos
        if venta_venta == "" or venta_usuario == "":
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            # Actualizar la interfaz para mostrar el mensaje
            evento.page.update()
            return

        try:
            venta_nombre = f"VEN-{venta_venta}-VINATA"

            venta_dao = VentaDAO()

            if venta_dao.verificar_nombre_existente(venta_nombre, venta_id):
                mensaje.value = f"La venta '{venta_venta}' ya está registrada"
                mensaje.color = "#ff0000"
                evento.page.update()
                return
            
            venta = Venta_nombre_usuario(
                venta_id = venta_id,
                venta_venta = venta_nombre,
                venta_usuario = int(venta_usuario) # Convertir a entero
            )

            print(venta_id, venta_nombre, venta_usuario)

            venta_dao.editar_nombre_usuario(venta)

            mensaje.value = f"Venta {venta_venta} ha sido editada exitosamente"
            mensaje.color = ft.Colors.GREEN
                
            # ===== MOSTRAR SNACKBAR DE ÉXITO =====
            if snackbar_func:
                snackbar_func(f"Venta '{venta_nombre}' editada exitosamente", "editar")
                    
            # ===== AGREGAR NOTIFICACIÓN AL SISTEMA =====
            globals.agregar_notificacion(
                titulo=f"Venta '{venta_nombre}'",
                mensaje="editada exitosamente",
                tipo="editar"
            )

            # Actualizar el contador de notificaciones
            try:
                if evento.pila and hasattr(evento.pila, 'actualizar_contador'):
                    evento.pila.actualizar_contador()
            except:
                pass
            
            # limpiar_formualrio()

            # # ---------------------- Si el modal esta activo y si existe la función para cerrar
            # if formulario_visible and cerrando_modal:
            #     evento.page.update()
            #     cerrando_modal()
            #     return

        except ValueError:
            mensaje.value = "El campo 'usuario' debe ser un número entero"
            mensaje.value = ft.Colors.RED
        except Exception as error:
            mensaje.value = f"Error al editar la venta: {error}"
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
                                "Editar venta",
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
                        "Editar venta",
                        size = 24,
                        weight = ft.FontWeight.BOLD,
                        color = "#c9a03d"
                    ),
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
                                ft.TextStyle()  # Estilo en negrita
                            ),
                            ft.TextSpan(
                                "editar",
                                ft.TextStyle(weight=ft.FontWeight.BOLD) # Este texto es normal
                            ),
                            ft.TextSpan(
                                " información básica de una venta",
                                ft.TextStyle()  # Estilo en negrita
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
            
            venta_input,

            usuario_input,

            
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
                width = 500,
                on_click = editar_venta
            ),

            mensaje
        ],
        spacing = 15,
        expand = True
    )

    # Cargar los usuarios
    cargar_usuarios()

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
    