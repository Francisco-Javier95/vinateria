import flet as ft

from models.articulo import Articulo
from dao.articulo_dao import ArticuloDAO
from ui.articulo_form import articulo_form

def articulos_list(regresar):
    # ---------------- Variables de estado -------------------
    capa_oscura_abierta_modal = False # Indica si el modal esta visible/activo
    capa_oscura_modal = None # Es el contenido con backgroud oscuro semitransparente (capa oscuara)
    pagina_referencia = None # Guardar la referencia a la pagina (contenido)

    # -------------- Contenedor de capas ---------------------
    pila = ft.Stack(expand = True) # ft.Stack permite superponer widgets (elementos)
    # 'expand = True' hace que ocupe todo el espacio disponible
    
    # --------------- Tabla de productos ---------------------
    # Tabla de productos
    tabla = ft.DataTable(
        columns = [
            ft.DataColumn(ft.Text("Imagen")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Precio"))
        ],
        rows = []
    )

    mensaje = ft.Text()

    # -----------------Función para cargar los productos/articulos
    def cargar_articulos():
        try:
            articulo_dao = ArticuloDAO()
            articulos = articulo_dao.obtener_todos()

            tabla.rows.clear() # Limpia los registros de la tabla

            for articulo in articulos:
                tabla.rows.append(
                    ft.DataRow(
                        cells = [
                            ft.DataCell(ft.Text(articulo.articulo_imagen)),
                            ft.DataCell(ft.Text(articulo.articulo_articulo)),
                            ft.DataCell(ft.Text(str(articulo.articulo_categoria))),
                            ft.DataCell(ft.Text(str(articulo.articulo_stock))),
                            ft.DataCell(ft.Text(f"${articulo.articulo_precio:.2f}")) # ':.2f significa 2 decimales', siendo que el formato es, ejemplo: $1999.99)
                        ]
                    )
                )
            
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()

        except Exception as error:
            mensaje.value = f"Error al consultar los productos: {error}"
            mensaje.color = ft.Colors.RED
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()

    # ------------------- Función para cerrar la modal --------------------
    def cerrar_modal():
        # Cierra el modal, eliminando la capa oscura de la pila

        # 'nonlocal' permite modificar variables de la función padre (articulos_list)
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Varificar si el modal está abierto y la capa oscura exite en la pila
        if capa_oscura_abierta_modal and capa_oscura_modal in pila.controls:
            # Remover la capa uscura del Stack (la elimina visualemente)
            pila.controls.remove(capa_oscura_modal)

            # limpiar las capas
            capa_oscura_modal = None
            capa_oscura_abierta_modal = False

            # Volver a cargar la lista de los productos/articulos
            cargar_articulos()

            # Actualizar la interfaz
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()
    
    def abrir_modal(evento):
        # Crear y muestrar el modal con el formulario de "Crear producto"
        # evento: El evento del clic en el boton "Crear"

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = articulo_form(
            formulario_visible = True, # Activar el modal, mostrando el formulario
            cerrando_modal = cerrar_modal
        )

        # --------------- Crear la capa oscura (OVERLAY) --------------
        capa_oscura = ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK_45,
            content=ft.Column(
                controls=[contenido_modal],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
                width = 5000
            )
        )

        # -------------- Agregar la capa a la pila ---------------------
        # La capa se superpone al contenido principal
        pila.controls.append(capa_oscura)

        # Guardar referencia a la capa
        capa_oscura_modal = capa_oscura

        # Cambiar el esado de "cerrado" a "abierto"
        capa_oscura_abierta_modal = True

        # Actualizar la interfaz
        if pila.page:
            pila.update() # Se actualiza la pila para mostrar cambios
        elif pagina_referencia:
            pagina_referencia.update()

    contenido_principal = ft.Container(
        padding = 30,
        content = ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        ft.Row(
                            controls = [
                                ft.Text(
                                    "Inventario",
                                    size = 24,
                                    weight = ft.FontWeight.BOLD,
                                    color = "#c9a03d"
                                ),
                                ft.OutlinedButton(
                                    "Crear",
                                    icon = ft.Icons.WINE_BAR,
                                    on_click = abrir_modal # Al hacer clic, sobre el boton de "Crear" se abrira el modal
                                )
                            ]
                        ),
                        # ft.OutlinedButton(
                        #     "Regresar",
                        #     icon = ft.Icons.ARROW_BACK,
                        #     on_click = lambda e: regresar()
                        # )
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(),

                ft.Container(
                    content = tabla,
                    border = ft.Border.all(
                        1,
                        ft.Colors.BLUE_GREY_200
                    ),

                    border_radius = 10,
                    padding = 10
                ),

                mensaje
            ],
            spacing = 20,
            scroll = ft.ScrollMode.AUTO
        )
    )

    # --------------- Agregar el contenido principal a la pila ----------------
    pila.controls.append(contenido_principal)

    # ---------------- Cargar datos iniciales (SIN actualizar) ------------------
    # Solo cargaran los datos, pero NO se hace update porque la pila aun no esta en la pagina. La actualización se hara cuando se agregue.
    try:
        articulo_dao = ArticuloDAO()
        articulos = articulo_dao.obtener_todos()

        tabla.rows.clear()
        for articulo in articulos:
            tabla.rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(articulo.articulo_imagen)),
                        ft.DataCell(ft.Text(articulo.articulo_articulo)),
                        ft.DataCell(ft.Text(str(articulo.articulo_categoria))),
                        ft.DataCell(ft.Text(str(articulo.articulo_stock))),
                        ft.DataCell(ft.Text(f"${articulo.articulo_precio:.2f}")) # ':.2f significa 2 decimales', siendo que el formato es, ejemplo: $1999.99)
                    ]
                )
            )
    except Exception as error:
        mensaje.value = f"Error al consultar los productos: {error}"
        mensaje.color = ft.Colors.RED

    return pila