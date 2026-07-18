import flet as ft

from models.articulo import Articulo
from dao.articulo_dao import ArticuloDAO

# def articulo_form(regresar):
#     articulo_input = ft.TextField(
#         label = "Nombre: ",
#         width = 400
#     )
#     codigo_input = ft.TextField(
#         label = "Código: ",
#         width = 400
#     )
#     categoria_input = ft.TextField(
#         label = "Categoría: ",
#         width = 400
#     )
#     imagen_input = ft.TextField(
#         label = "Imagen: ",
#         width = 400
#     )
#     precio_input = ft.TextField(
#         label = "Precio: ",
#         width = 400
#     )
#     stock_input = ft.TextField(
#         label = "Stock: ",
#         width = 400
#     )
#     proveedor_input = ft.TextField(
#         label = "Proveedor: ",
#         width = 400
#     )

#     mensaje = ft.Text(
#         "",
#         color = ft.Colors.GREEN
#     )

#     def guardar_articulo(e):
#         #Recuperar los valores de los TextFile
#         articulo_articulo = articulo_input.value
#         articulo_codigo = codigo_input.value
#         articulo_categoria = categoria_input.value
#         articulo_imagen = imagen_input.value
#         articulo_precio = precio_input.value
#         articulo_stock = stock_input.value
#         articulo_proveedor = proveedor_input.value

#         # Validación de campos vacíos
#         if articulo_articulo == "" or articulo_codigo == "" or articulo_categoria == "" or articulo_imagen == "" or articulo_precio == "" or articulo_stock == "" or articulo_proveedor == "":
#             mensaje.value = "Todos los campos son obligatorios"
#             mensaje.color = ft.Colors.RED
#             # Actualizar la interfaz para mostrarel mensaje
#             e.page.update()
#             return
#         try:
#             articulo_dao = ArticuloDAO()
#             articulo_id = None

#             nuevo_articulo = Articulo(
#                 articulo_id = articulo_id,
#                 articulo_articulo = articulo_articulo,
#                 articulo_codigo = articulo_codigo,
#                 articulo_categoria = int(articulo_categoria),
#                 articulo_imagen = articulo_imagen,
#                 articulo_precio = float(articulo_precio),
#                 articulo_stock = int(articulo_stock),
#                 articulo_proveedor = int(articulo_proveedor)
#             )

#             articulo_dao.insertar(nuevo_articulo)

#             mensaje.value = f"Producto {articulo_articulo} ha sido insertado exitosamente"
#             mensaje.color = ft.Colors.GREEN
#             articulo_input.value = ""
#             codigo_input.value = ""
#             categoria_input.value = ""
#             imagen_input.value = ""
#             precio_input.value = ""
#             stock_input.value = ""
#             proveedor_input.value = ""
#         except ValueError:
#             mensaje.value = "El campo 'Categoría' debe ser un número entero"
#             mensaje.value = ft.Colors.RED
#         except Exception as error:
#             mensaje.value = f"Error al insertar el producto: {error}"
#             mensaje.value = ft.Colors.RED

#         # Actualizar la interfaz para mostrarel mensaje
#         e.page.update()

#     return ft.Container(
#         padding = 30,
#         content = ft.Column(
#             controls = [
#                 ft.Text(
#                     "Crear producto",
#                     size = 24,
#                     weight = ft.FontWeight.BOLD
#                 ),

#                 ft.Text(
#                     "Crea nuevas tarjetas de productos en tu inventario",
#                     size = 14,
#                     color = ft.Colors.BLUE_GREY_900
#                 ),
                
#                 articulo_input,
#                 codigo_input,
#                 categoria_input,
#                 imagen_input,
#                 precio_input,
#                 stock_input,
#                 proveedor_input,

#                 ft.Row(
#                     controls = [

#                         ft.ElevatedButton(
#                             "Crear",
#                             icon = ft.Icons.SAVE,
#                             on_click = guardar_articulo
#                         ),

#                         ft.OutlinedButton(
#                             "",
#                             icon = ft.Icons.ARROW_BACK,
#                             on_click = lambda e: regresar()
#                         )
#                     ]
#                 ),

#                 mensaje
#             ],

#             spacing = 15
#         )
#     )

def articulo_form(regresar):
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

    def guardar_articulo(e):
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
            e.page.update()
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
            articulo_input.value = ""
            codigo_input.value = ""
            categoria_input.value = ""
            imagen_input.value = ""
            precio_input.value = ""
            stock_input.value = ""
            proveedor_input.value = ""
        except ValueError:
            mensaje.value = "El campo 'categoria' debe ser un número entero"
            mensaje.value = ft.Colors.RED
        except Exception as error:
            mensaje.value = f"Error al insertar el articulo: {error}"
            mensaje.value = ft.Colors.RED

        # Actualizar la interfaz para mostrar el mensaje 
        e.page.update()

    return ft.Container(
        padding = 30,
        content = ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        ft.Container(
                            ft.OutlinedButton(
                                "",
                                icon = ft.Icons.ARROW_BACK,
                                icon_color = ft.Colors.WHITE,
                                on_click = lambda e: regresar()
                            ),
                            bgcolor = "#6b1d41"
                        ),
                        
                        ft.Text(
                            "Crear producto",
                            size = 24,
                            weight = ft.FontWeight.BOLD,
                            color = "#c9a03d"
                        ),
                    ]
                ),

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
                
                ft.Row(
                    controls = [
                        ft.ElevatedButton(
                            "Crear",
                            bgcolor = "#6b1d41",
                            on_click= guardar_articulo
                        ),
                    ]
                ),

                mensaje
            ],

            spacing = 15
        )
    )