import flet as ft

from models.articulo import Articulo
from dao.articulo_dao import ArticuloDAO
import base64
import os
import asyncio

def articulo_form(regresar = None, formulario_visible = False, cerrando_modal = None):
    # ------------ Campos del formulario ------------------
    articulo_input = ft.TextField(
        label = "Nombre: ",
        expand = True,
        color = "#424955"
    )
    codigo_input = ft.TextField(
        label = "Código: ",
        expand = True,
        color = "#424955"
    )
    categoria_input = ft.TextField(
        label = "Categoría: ",
        expand = True,
        color = "#424955"
    )
    
    # -------------- Campo imagen ------------------
    # Variable para almacenar la imagen seleccionada
    imagen_seleccionada = None
    imagen_previa = ft.Image(
        src = "",
        width = 150,
        height = 150,
        border_radius = 10,
        visible = False # Oculto inicialmente
    )

    # Texto que muestra el nombre del archivo
    nombre_archivo = ft.Text(
        "Ningún archivo seleccionado",
        size = 12,
        color = ft.Colors.GREY_600
    )

    file_picker = ft.FilePicker()

    # -------------- Función para manejar la seleccion de la imagen ----------
    def on_archivo_seleccionado(e: ft.filePickerResultEvent):
        nonlocal imagen_seleccionada

        if e.files and len(e.files) > 0:
            # Obtener el arcghivo seleccionado
            archivo = e.files[0]
            ruta_archivo = archivo.path

            # Mostrar el nombre del archivo
            nombre_archivo.value = f"{archivo.name}"

            try:
                # Leer la imagen y convertirla a base64 para mostrarla
                with open(ruta_archivo, "rb") as f:
                    datos_imagen = f.read()
                    # Codificar en base64 para mostrar
                    imagen_base64 = base64.b64encode(datos_imagen).decode('utf-8')

                    # Guardar la imagen para usarla al guardar
                    imagen_seleccionada = imagen_base64

                    # Mostrar la vista previa
                    imagen_previa.src_base64 = imagen_base64
                    imagen_previa.visible = True

                    #Actualizar la interfaz
                    e.page.update()

            except Exception as error:
                nombre_archivo.value = f"Error al cargar: {error}"
                nombre_archivo.color = ft.Colors.RED
                e.page.update()
        else:
            # Si el usuario cancela la selección
            nombre_archivo.value = "Ningun archivo seleccionado"
            imagen_previa.visible = False
            imagen_seleccionada = None
            e.page.update()

    # --------- Crear el file picker -----------
    file_picker.on_result = on_archivo_seleccionado

    # --------- Boton para seleccionar imagen ---------
    def seleccionar_imagen(e):
        # Permitir solo imagenes
        try:
            e.page.run_task(
                file_picker.pick_files,
                allow_multiple = False, # Solo una imagen
                allowed_extensions = ["jpg", "jpeg", "png", "gif", "bmp", "webp"],
                dialog_title = "Seleccionar imagen" 
            )
        except Exception as error:
            print(f"Error al seleccionar imagen: {error}")
    
    def eliminar_imagen(e):
        # Eliminar la imagen seleccionada
        nonlocal imagen_seleccionada
        imagen_seleccionada = None
        nombre_archivo.value = "Ningún archivo seleccionado"
        nombre_archivo.color = ft.Colors.GREY_600
        imagen_previa.visible = False
        e.page.update()

    # Contenedor de la imagen (selector + vista previa)
    imagen_input = ft.Column(
        controls = [
            ft.Row(
                controls = [
                    ft.OutlinedButton(
                        "Seleccionar imagen",
                        icon = ft.Icons.IMAGE,
                        on_click = seleccionar_imagen,
                        style = ft.ButtonStyle(
                            bgcolor = ft.Colors.BLUE_50,
                            side = ft.BorderSide(color = ft.Colors.BLUE_400, width = 1) 
                        )
                    ),
                    ft.IconButton(
                        icon = ft.Icons.DELETE,
                        icon_color = ft.Colors.RED_400,
                        tooltip = "Eliminar imagen",
                        on_click = eliminar_imagen,
                        visible = False # Se mostrara solo cuando haya imagen
                    )
                ],
                alignment = ft.MainAxisAlignment.START,
                spacing = 10
            ),
            nombre_archivo,
            ft.Container(
                content = imagen_previa,
            )
        ],
        spacing = 5
    )
    # -------------- FIN Campo imagen ------------------


    precio_input = ft.TextField(
        label = "Precio: ",
        expand = True,
        color = "#424955"
    )
    stock_input = ft.TextField(
        label = "Stock: ",
        expand = True,
        color = "#424955"
    )
    proveedor_input = ft.TextField(
        label = "Proveedor: ",
        expand = True,
        color = "#424955"
    )

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    # -------------- Función para limpiar el formulario -------------------
    def limpiar_formualrio():
        articulo_input.value = ""
        codigo_input.value = ""
        categoria_input.value = ""
        # imagen_input.value = ""
        precio_input.value = ""
        stock_input.value = ""
        proveedor_input.value = ""

        # Limpiar la imagen
        imagen_seleccionada = None
        nombre_archivo.value = "Ningún archivo seleccionado"
        imagen_previa.visible = False

    def guardar_articulo(evento):
        # Recuperar los valores de los TextFile
        articulo_articulo = articulo_input.value
        articulo_codigo = codigo_input.value
        articulo_categoria = categoria_input.value
        # articulo_imagen = imagen_input.value
        articulo_precio = precio_input.value
        articulo_stock = stock_input.value
        articulo_proveedor = proveedor_input.value

        # Obtener la imagen seleccionada
        articulo_imagen = imagen_seleccionada

        # Validación de campos vacíos
        if articulo_articulo == "" or articulo_codigo == "" or articulo_categoria == "" or articulo_imagen is None or articulo_precio == "" or articulo_stock == "" or articulo_proveedor == "":
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            # Actualizar la interfaz para mostrar el mensaje
            evento.page.update()
            return
        try:
            articulo_dao = ArticuloDAO()
            articulo_id = None

            nuevo_articulo = Articulo(
                articulo_id = articulo_id,
                articulo_articulo = articulo_articulo,
                articulo_codigo = articulo_codigo,
                articulo_categoria = int(articulo_categoria),
                articulo_imagen = articulo_imagen, # Guardamos la imagen en base64
                articulo_precio = float(articulo_precio),
                articulo_stock = int(articulo_stock),
                articulo_proveedor = int(articulo_proveedor)
            )

            articulo_dao.insertar(nuevo_articulo)

            mensaje.value = f"Articulo {articulo_articulo} ha sido insertado exitosamente"
            mensaje.color = ft.Colors.GREEN
            
            limpiar_formualrio()

            if formulario_visible and cerrando_modal:
                evento.page.update()
                cerrando_modal()
                return


        except ValueError:
            mensaje.value = "El campo 'categoria' debe ser un número entero"
            mensaje.value = ft.Colors.RED
        except Exception as error:
            mensaje.value = f"Error al insertar el articulo: {error}"
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
                            }
                        ),
                        bgcolor = "#6b1d41",
                        icon_color = "#ffffff",
                        on_click = lambda e: cerrando_modal(),

                        tooltip = "Cerrar" # Texto que aparece al pasar el cursor
                    ),
                    ft.Row(
                        controls = [
                            ft.Text(
                                "Crear producto",
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
                        "Crear producto",
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
                                "Crea",
                                ft.TextStyle(weight=ft.FontWeight.BOLD)  # Estilo en negrita
                            ),
                            ft.TextSpan(
                                " nuevas tarjetas de",
                                ft.TextStyle() # Este texto es normal
                            ),
                            ft.TextSpan(
                                " productos",
                                ft.TextStyle(weight=ft.FontWeight.BOLD)  # Estilo en negrita
                            ),
                            ft.TextSpan(
                                " en tu inventario",
                                ft.TextStyle()  # Este texto es normal
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

            articulo_input,
            codigo_input,
            categoria_input,
            
            imagen_input,

            precio_input,
            stock_input,
            proveedor_input,

            # ------ BOTONES ---------
            ft.Row(
                controls = [
                    ft.ElevatedButton(
                        "Guardar",
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
                        ),
                        bgcolor = "#6b1d41",
                        color = "#ffffff",
                        expand = True,
                        on_click = guardar_articulo
                    ),
                ],
                spacing = 10
            ),
            mensaje
        ],
        spacing = 15
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
    