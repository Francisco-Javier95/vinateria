import flet as ft

from models.articulo import Articulo
from dao.articulo_dao import ArticuloDAO
from ui.articulo_form_create import articulo_form
from ui.articulo_form_edit import articulo_form_edit
from ui.articulo_alert_delete import alerta_eliminar

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
            ft.DataColumn(ft.Text("Imagen", color = "#0d1b2a")),
            ft.DataColumn(ft.Text("Nombre", color = "#0d1b2a")),
            ft.DataColumn(ft.Text("Categoría", color = "#0d1b2a")),
            ft.DataColumn(ft.Text("Stock", color = "#0d1b2a")),
            ft.DataColumn(ft.Text("Proveedor", color = "#0d1b2a")),
            ft.DataColumn(ft.Text("Precio", color = "#0d1b2a")),
            ft.DataColumn(ft.Text("Acciones", color = "#0d1b2a")),
        ],
        expand = True,
        rows = []
    )

    mensaje = ft.Text()

    # -----------------Función para cargar los productos/articulos----------------------
    def cargar_articulos():
        try:
            articulo_dao = ArticuloDAO()
            articulos = articulo_dao.obtener_todos()

            tabla.rows.clear() # Limpia los registros de la tabla

            for articulo in articulos:
                tabla.rows.append(
                    ft.DataRow(
                        cells = [
                            ft.DataCell(ft.Text(articulo.articulo_imagen, color = "#0d1b2a")),
                            ft.DataCell(ft.Text(articulo.articulo_articulo, color = "#0d1b2a")),
                            ft.DataCell(ft.Text(str(articulo.articulo_categoria), color = "#0d1b2a")),
                            ft.DataCell(ft.Text(str(articulo.articulo_stock), color = "#0d1b2a")),
                            ft.DataCell(ft.Text(str(articulo.articulo_proveedor), color = "#0d1b2a")),
                            ft.DataCell(ft.Text(f"${articulo.articulo_precio:.2f}", color = "#0d1b2a")), # ':.2f significa 2 decimales', siendo que el formato es, ejemplo: $1999.99)
                            ft.DataCell(
                                ft.Row(
                                    controls = [
                                        # Boton Editar
                                        ft.OutlinedButton(
                                            f"Editar ID:{articulo.articulo_id}",
                                            data = articulo.articulo_id, # Recuperar el ID del registro/producto

                                            style = ft.ButtonStyle(
                                                bgcolor = "#c9a03d",  # Color de fondo
                                                side = {
                                                    ft.ControlState.DEFAULT: 
                                                        ft.BorderSide(
                                                            width = 2,
                                                            color = "#926600"
                                                        ),
                                                    # Borde rojo de 2 píxeles al pasar el mouse
                                                    ft.ControlState.HOVERED: 
                                                        ft.BorderSide(
                                                            width = 2,
                                                            color = "#c9a03d"
                                                        )
                                                },
                                                color = "#ffffff",
                                                shape = ft.RoundedRectangleBorder(radius = 10)
                                            ),

                                            on_click = abrir_formulario_editar_modal # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                        ),

                                        # Boton Eliminar
                                        ft.OutlinedButton(
                                            f"Eliminar ID:{articulo.articulo_id}",
                                            data = articulo.articulo_id,

                                            style = ft.ButtonStyle(
                                                # Cambiar el color del fondo
                                                bgcolor = {
                                                    ft.ControlState.HOVERED: "#de3b40",
                                                    ft.ControlState.DEFAULT: "#f3f4f6" # Color por defecto
                                                },
                                                # Cambiar el color del borde
                                                side = {
                                                    ft.ControlState.DEFAULT: 
                                                        ft.BorderSide(
                                                            width = 2,
                                                            color = "#de3b40"
                                                        ),
                                                    # Borde rojo de 2 píxeles al pasar el mouse
                                                    ft.ControlState.HOVERED: 
                                                        ft.BorderSide(
                                                            width = 2,
                                                            color = "#de3b40"
                                                        )
                                                },
                                                # Cambiar el color de texto
                                                color={
                                                    ft.ControlState.HOVERED: "#ffffff",
                                                    ft.ControlState.DEFAULT: "#de3b40",
                                                },
                                                # Cambiar el redondeado del borde
                                                shape = ft.RoundedRectangleBorder(radius = 10)
                                            ),

                                            on_click = abrir_alerta_eliminar_articulo # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                        )
                                    ]
                                )
                            )
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

    
    def abrir_formulario_crear_modal(evento):
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

    def abrir_formulario_editar_modal(evento):
        # Crear y muestrar el modal con el formulario de "Editar producto"
        # evento: El evento del clic en el boton "Editar" del registro correspondiente

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # ======== Obtener el ID del articulo desde el boton =========
        # El ID se guarda en la propiedad 'data' del boton
        articulo_id = evento.control.data if evento.control else None # Obtener el articulo_id del boton

        if articulo_id is None:
            print("No se pudo obtener el ID del articulo")
            return
        
        try:
            # === Obtener los datos del articulo desde la BD ===
            articulo_dao = ArticuloDAO()
            articulo = articulo_dao.obtener_id_del_articulo(articulo_id)

            if articulo is None:
                print(f"No se encontro el articulo con ID: {articulo_id}")
                return
            
            # Preparar los datos para el formulario
            registro = {
                'id': articulo.articulo_id,
                'nombre': articulo.articulo_articulo,
                'codigo': articulo.articulo_codigo,
                'categoria_id': articulo.articulo_categoria,
                'imagen': articulo.articulo_imagen,
                'precio': str(articulo.articulo_precio),
                'stock': str(articulo.articulo_stock),
                'proveedor_id': articulo.articulo_proveedor
            }

            print(f"Datos cargados: {registro}")

        except Exception as error:
            print(f"Error al obtener el articulo: {error}")
            return
        # ======= FIN Obtener el ID del articulo desde el boton ========
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = articulo_form_edit(
            formulario_visible = True, # Activar el modal, mostrando el formulario
            cerrando_modal = cerrar_modal,
            registro = registro # Enviar los datos al formulario
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

    def abrir_alerta_eliminar_articulo(evento):
        # Crear y muestrar el modal con la alerta de "La Vinata dice: ¿Desea eliminar este articulo?"
        # evento: El evento del clic en el boton "Eliminar"

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # ======== Obtener el ID del articulo desde el boton =========
        # El ID se guarda en la propiedad 'data' del boton
        articulo_id = evento.control.data if evento.control else None # Obtener el articulo_id del boton

        if articulo_id is None:
            print("No se pudo obtener el ID del articulo")
            return
        
        try:
            # === Obtener los datos del articulo desde la BD ===
            articulo_dao = ArticuloDAO()
            articulo = articulo_dao.obtener_id_del_articulo(articulo_id)

            if articulo is None:
                print(f"No se encontro el articulo con ID: {articulo_id}")
                return
            
            # Preparar los datos para el formulario
            id_y_nombre = {
                'id': articulo.articulo_id,
                'nombre': articulo.articulo_articulo
            }

            print(f"Datos cargados: {id_y_nombre}")

        except Exception as error:
            print(f"Error al obtener el articulo: {error}")
            return
        # ======= FIN Obtener el ID del articulo desde el boton ========
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = alerta_eliminar(
            formulario_visible = True, # Activar el modal, mostrando el formulario
            cerrando_modal = cerrar_modal,
            registro = id_y_nombre # Enviar los datos a la alerta
        )

        # --------------- Crear la capa oscura (OVERLAY) --------------
        capa_oscura = ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK_45,
            content=ft.Column(
                controls=[contenido_modal],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                width = 5000
            ),
            padding = ft.Padding.only(top = 40)
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


    # ================= CONTENIDO PRINCIPAL =================
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
                                    style=ft.ButtonStyle(
                                        bgcolor = "#6b1d41",  # Color de fondo
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
                                        color = "#ffffff",
                                        shape = ft.RoundedRectangleBorder(radius = 10)
                                    ),
                                    
                                    icon = ft.Icons.WINE_BAR,
                                    on_click = abrir_formulario_crear_modal # Al hacer clic, sobre el boton de "Crear" se abrira el modal
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
                        ft.Colors.BLUE_900
                    ),
                    expand = True,
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
                        ft.DataCell(ft.Text(articulo.articulo_imagen, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(articulo.articulo_articulo, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(str(articulo.articulo_categoria), color = "#0d1b2a")),
                        ft.DataCell(ft.Text(str(articulo.articulo_stock), color = "#0d1b2a")),
                        ft.DataCell(ft.Text(str(articulo.articulo_proveedor), color = "#0d1b2a")),
                        ft.DataCell(ft.Text(f"${articulo.articulo_precio:.2f}", color = "#0d1b2a")), # ':.2f significa 2 decimales', siendo que el formato es, ejemplo: $1999.99)
                        ft.DataCell(
                            ft.Row(
                                controls = [
                                    # Boton Editar
                                    ft.OutlinedButton(
                                        f"Editar ID:{articulo.articulo_id}",
                                        data = articulo.articulo_id, # Recuperar el ID del registro/producto

                                        style = ft.ButtonStyle(
                                            bgcolor = "#c9a03d",  # Color de fondo
                                            side = {
                                                ft.ControlState.DEFAULT: 
                                                    ft.BorderSide(
                                                        width = 2,
                                                        color = "#926600"
                                                    ),
                                                # Borde rojo de 2 píxeles al pasar el mouse
                                                ft.ControlState.HOVERED: 
                                                    ft.BorderSide(
                                                        width = 2,
                                                        color = "#c9a03d"
                                                    )
                                            },
                                            color = "#ffffff",
                                            shape = ft.RoundedRectangleBorder(radius = 10)
                                        ),

                                        on_click = abrir_formulario_editar_modal # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                    ),

                                    # Boton Eliminar
                                    ft.OutlinedButton(
                                        f"Eliminar ID:{articulo.articulo_id}",
                                        data = articulo.articulo_id,

                                        style = ft.ButtonStyle(
                                            # Cambiar el color del fondo
                                            bgcolor = {
                                                ft.ControlState.HOVERED: "#de3b40",
                                                ft.ControlState.DEFAULT: "#f3f4f6" # Color por defecto
                                            },
                                            # Cambiar el color del borde
                                            side = {
                                                ft.ControlState.DEFAULT: 
                                                    ft.BorderSide(
                                                        width = 2,
                                                        color = "#de3b40"
                                                    ),
                                                # Borde rojo de 2 píxeles al pasar el mouse
                                                ft.ControlState.HOVERED: 
                                                    ft.BorderSide(
                                                        width = 2,
                                                        color = "#de3b40"
                                                    )
                                            },
                                            # Cambiar el color de texto
                                            color = {
                                                ft.ControlState.HOVERED: "#ffffff",
                                                ft.ControlState.DEFAULT: "#de3b40",
                                            },
                                            # Cambiar el redondeado del borde
                                            shape = ft.RoundedRectangleBorder(radius = 10)
                                        ),

                                        on_click = abrir_alerta_eliminar_articulo # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
    except Exception as error:
        mensaje.value = f"Error al consultar los productos: {error}"
        mensaje.color = ft.Colors.RED

    return pila