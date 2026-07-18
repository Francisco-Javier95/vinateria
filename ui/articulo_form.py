import flet as ft

from models.articulo import Articulo
from dao.articulo_dao import ArticuloDAO

def articulo_form(regresar = None, formulario_visible = False, cerrando_modal = None):
    # ------------ Campos del formulario ------------------
    articulo_input = ft.TextField(
        label = "Nombre: ",
        width = 400,
        color = "#424955"
    )
    codigo_input = ft.TextField(
        label = "Código: ",
        width = 400,
        color = "#424955"
    )
    categoria_input = ft.TextField(
        label = "Categoría: ",
        width = 400,
        color = "#424955"
    )
    imagen_input = ft.TextField(
        label = "Imagen: ",
        width = 400,
        color = "#424955"
    )
    precio_input = ft.TextField(
        label = "Precio: ",
        width = 400,
        color = "#424955"
    )
    stock_input = ft.TextField(
        label = "Stock: ",
        width = 400,
        color = "#424955"
    )
    proveedor_input = ft.TextField(
        label = "Proveedor: ",
        width = 400,
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
        imagen_input.value = ""
        precio_input.value = ""
        stock_input.value = ""
        proveedor_input.value = ""

    def guardar_articulo(evento):
        # Recuperar los valores de los TextFile
        articulo_articulo = articulo_input.value
        articulo_codigo = codigo_input.value
        articulo_categoria = categoria_input.value
        articulo_imagen = imagen_input.value
        articulo_precio = precio_input.value
        articulo_stock = stock_input.value
        articulo_proveedor = proveedor_input.value

        # Validación de campos vacíos
        if articulo_articulo == "" or articulo_codigo == "" or articulo_categoria == "" or articulo_imagen == "" or articulo_precio == "" or articulo_stock == "" or articulo_proveedor == "":
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
                articulo_imagen = articulo_imagen,
                articulo_precio = float(articulo_precio),
                articulo_stock = int(articulo_stock),
                articulo_proveedor = int(articulo_proveedor)
            )

            articulo_dao.insertar(nuevo_articulo)

            mensaje.value = f"Articulo {articulo_articulo} ha sido insertado exitosamente"
            mensaje.color = ft.Colors.GREEN
            
            limpiar_formualrio()

            # ---------------------- Si el modal esta activo y si existe la función para cerrar
            if formulario_visible and cerrando_modal:
                evento.page.update()
                import time
                time.sleep(0.5)
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
                    ft.Text(
                        "Crear producto",
                        size = 24,
                        weight = ft.FontWeight.BOLD,
                        color = "#c9a03d"
                    ),
                    ft.IconButton(
                        icon = ft.Icons.CLOSE,
                        bgcolor = "#6b1d41",
                        icon_color = "#ffffff",
                        on_click = lambda e: cerrando_modal(),

                        tooltip = "Cerrar" # Texto que aparece al pasar el cursor
                    )
                ],
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN 
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

            ft.Text(
                "Crea nuevas tarjetas de productos en tu inventario",
                size = 16,
                weight = ft.FontWeight.BOLD,
                color = "#9095a0"
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
                        "Crear",
                        bgcolor = "#6b1d41",
                        on_click= guardar_articulo
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
    