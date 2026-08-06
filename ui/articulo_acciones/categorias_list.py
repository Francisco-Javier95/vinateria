import flet as ft

from models.categoria import Categoria
from dao.categoria_dao import CategoriaDAO
from ui.articulo_acciones.categoria_acciones.categoria_form_create import categoria_form_create
from ui.articulo_acciones.categoria_acciones.categoria_form_edit import categoria_form_edit
from ui.articulo_acciones.categoria_acciones.categoria_alert_delete import alerta_eliminar

def categorias_list(regresar = None, tabla_categoria_visible = False, cerrando_modal = None, registro = None):
    
    # ---------------- Variables de estado -------------------
    capa_oscura_abierta_modal = False # Indica si el modal esta visible/activo
    capa_oscura_modal = None # Es el contenido con backgroud oscuro semitransparente (capa oscuara)
    pagina_referencia = None # Guardar la referencia a la pagina (contenido)

    todas_las_categorias = [] # Guardar todas las categorias sin filtrar

    # -------------- Contenedor de capas ---------------------
    pila = ft.Stack(expand = True) # ft.Stack permite superponer widgets (elementos)
    # 'expand = True' hace que ocupe todo el espacio disponible
    
    # --------------- Tabla de categorías ---------------------
    # Tabla de categorías
    tabla = ft.DataTable(
        divider_thickness = 0,
        horizontal_lines = ft.BorderSide(1, "#e2dcd5"),
        columns = [
            ft.DataColumn(ft.Text("Nombre", color = "#926600", weight = ft.FontWeight.BOLD)), # Columna 1
            ft.DataColumn(ft.Text("Vino/Licor", color = "#926600", weight = ft.FontWeight.BOLD, text_align = ft.TextAlign.CENTER, width = 100, expand = True)), # Columna 2
            ft.DataColumn(ft.Text("Descripción", color = "#926600", weight = ft.FontWeight.BOLD, width = 300)), # Columna 3
            ft.DataColumn(ft.Text("Acciones", color = "#926600",text_align = ft.TextAlign.CENTER, weight = ft.FontWeight.BOLD, width = 170)) # Columna 4
        ],
        expand = True,
        rows = []
    )

    mensaje = ft.Text()

    def mostrar_categorias_en_tabla(categorias):
        # Muestra una lista de categorias en la tabla
        tabla.rows.clear()

        for categoria in categorias:
            row = ft.DataRow(
                cells = [
                    ft.DataCell(ft.Text(categoria.categoria_categoria, color = "#0d1b2a", weight = ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Container(ft.Text(categoria.categoria_tipo, color = "#926600", text_align = ft.TextAlign.CENTER, weight = ft.FontWeight.BOLD, width = 100, expand = True), bgcolor = "#ffde93", padding = ft.Padding.symmetric(vertical = 4, horizontal = 8), border_radius = 4, expand = True), expand = True),
                    ft.DataCell(ft.Text(categoria.categoria_descripcion, color = "#0d1b2a")),
                    ft.DataCell(
                        ft.Row(
                            controls = [
                                # Boton Editar
                                ft.OutlinedButton(
                                    #f"Editar ID:{categoria.categoria_id}",
                                    "Editar",
                                    data = categoria.categoria_id, # Recuperar el ID de la categoria

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
                                    expand = True,

                                    on_click = abrir_formulario_editar_categoria # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                ),

                                # Boton Eliminar
                                ft.OutlinedButton(
                                    #f"Eliminar ID:{categoria.categoria_id}",
                                    "Eliminar",
                                    data = categoria.categoria_id, # Recuperar el ID de la categoria

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

                                    on_click = abrir_alerta_eliminar_categoria # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                ) 
                            ],
                            margin = 0,
                            expand = True
                        ),
                    )
                ]
            )

            tabla.rows.append(row)
        
        # Actualizar la interfaz
        if pila.page:
            pila.update()
        elif pagina_referencia:
            pagina_referencia.update()

    # -----------------Función para cargar las categorias----------------------
    def cargar_categorias():
        # Cargar todas las categorias de la base de datos
        nonlocal todas_las_categorias

        try:
            categoria_dao = CategoriaDAO()
            categorias = categoria_dao.obtener_todos()

            # Guardar todas las categorias
            todas_las_categorias = categorias

            # Mostrar todas las categorias
            mostrar_categorias_en_tabla(categorias)

        except Exception as error:
            print(f"Error al consultar las categorías: {error}")
            
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()

        return categorias

    def buscar_categorias(e):
        # Filtrar las categorias en tiempo real mediante el campo de nombre

        texto_busqueda = busqueda_input.value.lower().strip() if busqueda_input.value else ""

        # Si el campo de busqueda esta vacio se mostraran todas las categorias (registros)
        if texto_busqueda == "":
            mostrar_categorias_en_tabla(todas_las_categorias)
            return
        
        # Filtrar categorias por nombre
        categorias_filtradas = [
            categoria for categoria in todas_las_categorias
            if texto_busqueda in categoria.categoria_categoria.lower()
        ]

        # Mostrar las categorias filtrados
        mostrar_categorias_en_tabla(categorias_filtradas)

        # Mostrar mensaje si no hay resultados
        if not categorias_filtradas:
            print(f"No se encontraron categorias con '{texto_busqueda}'")
            if pila.page:
                pila.update()
            else:
                pagina_referencia.update()
        
    # ------------------- Función para cerrar la modal --------------------
    def cerrar_modal():
        # Cierra el modal, eliminando la capa oscura de la pila

        # 'nonlocal' permite modificar variables de la función padre (categorias_list)
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Varificar si el modal está abierto y la capa oscura exite en la pila
        if capa_oscura_abierta_modal and capa_oscura_modal in pila.controls:
            # Remover la capa uscura del Stack (la elimina visualemente)
            pila.controls.remove(capa_oscura_modal)

            # limpiar las capas
            capa_oscura_modal = None
            capa_oscura_abierta_modal = False

            # Volver a cargar la lista de las categorias
            cargar_categorias()

            # Actualizar la interfaz
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()

    
    def abrir_formulario_crear_categoria_modal(evento):
        # Crear y muestrar el modal con el formulario de Registrar categoria"
        # evento: El evento del clic en el boton "Registrar"

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = categoria_form_create(
            tabla_categoria_visible = True, # Activar el modal, mostrando el formulario
            cerrando_modal = cerrar_modal
        )

        # --------------- Crear la capa oscura (OVERLAY) --------------
        capa_oscura = ft.Container(
            expand = True,
            bgcolor = ft.Colors.BLACK_45,
            content = ft.Column(
                controls = [contenido_modal],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.CENTER,
                expand = True,
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

    def abrir_formulario_editar_categoria(evento):
        # Crear y mostrar el modal con el formulario de "Editar categoria"
        # evento: El evento del clic en el boton "Editar" del registro correspondiente

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # ======== Obtener el ID del categoria desde el boton =========
        # El ID se guarda en la propiedad 'data' del boton
        categoria_id = evento.control.data if evento.control else None # Obtener la categoria_id del boton

        if categoria_id is None:
            print("No se pudo obtener el ID de la categoria")
            return
        
        try:
            # === Obtener los datos de la categoria desde la BD ===
            categoria_dao = CategoriaDAO()
            categoria = categoria_dao.obtener_id_de_la_categoria(categoria_id)

            if categoria is None:
                print(f"No se encontro la categoria con ID: {categoria_id}")
                return

            
            # Preparar los datos para el formulario
            registro = {
                'id': categoria.categoria_id,
                'nombre': categoria.categoria_categoria,
                'tipo': categoria.categoria_tipo,
                'descripcion': categoria.categoria_descripcion
            }

            print(f"Datos cargados: {registro}")

        except Exception as error:
            print(f"Error al obtener la categoria: {error}")
            return
        # ======= FIN Obtener el ID de la categoria desde el boton ========
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = categoria_form_edit(
            tabla_categoria_visible = True, # Activar el modal, mostrando el formulario
            cerrando_modal = cerrar_modal,
            registro = registro # Enviar los datos al formulario
        )

        # --------------- Crear la capa oscura (OVERLAY) --------------
        capa_oscura = ft.Container(
            expand = True,
            bgcolor = ft.Colors.BLACK_45,
            content = ft.Column(
                controls = [contenido_modal],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.CENTER,
                expand = True,
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

    def abrir_alerta_eliminar_categoria(evento):
        # Crear y muestrar el modal con la alerta de "La Vinata dice: ¿Desea eliminar esta categoria?"
        # evento: El evento del clic en el boton "Eliminar"

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # ======== Obtener el ID de la categoria desde el boton =========
        # El ID se guarda en la propiedad 'data' del boton
        categoria_id = evento.control.data if evento.control else None # Obtener la categoria_id del boton

        if categoria_id is None:
            print("No se pudo obtener el ID de la categoria")
            return
        
        try:
            # === Obtener los datos de la categoria desde la BD ===
            categoria_dao = CategoriaDAO()
            categoria = categoria_dao.obtener_id_de_la_categoria(categoria_id)

            if categoria is None:
                print(f"No se encontro la categoria con ID: {categoria_id}")
                return
            
            # Preparar los datos para el formulario
            id_y_nombre = {
                'id': categoria.categoria_id,
                'nombre': categoria.categoria_categoria
            }

            print(f"Datos cargados: {id_y_nombre}")

        except Exception as error:
            print(f"Error al obtener la categoria: {error}")
            return
        # ======= FIN Obtener el ID de la categoria desde el boton ========
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = alerta_eliminar(
            tabla_categoria_visible = True, # Activar el modal, mostrando el formulario
            cerrando_modal = cerrar_modal,
            registro = id_y_nombre # Enviar los datos a la alerta
        )

        # --------------- Crear la capa oscura (OVERLAY) --------------
        capa_oscura = ft.Container(
            expand = True,
            bgcolor = ft.Colors.BLACK_45,
            content = ft.Column(
                controls = [contenido_modal],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand = True,
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

    # Campo de Busqueda
    busqueda_input = ft.TextField(
        hint_text = "Buscar mediante nombre",  # Esto es el placeholder
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        focused_border_color = "#c9a03d", # Borde al enfocar
        border_color = "#bcc1ca",
        color = "#424955",
        width = 400,
        height = 40,

        on_change = buscar_categorias, # Buscar en tiempo real

        # 'suffix_icon' Sirve para colocar un icono en el input despues del texto
        suffix_icon = ft.Icon(
            ft.Icons.SEARCH_OUTLINED, # Icono de lupa
            color = "#6b1d41"

        ),
    )

    campo_de_busqueda = ft.Container(
        ft.Row(
            controls = [

                # Campo de busqueda
                ft.Container(
                    busqueda_input
                ),
            ],
        ),
        bgcolor = "#ffffff",
        border = ft.Border.all(
            1,
            "#e2dcd5"
        ),
        border_radius = 4
    )

    barra_de_acciones = ft.Container(
        ft.Row(
            controls = [
                ft.OutlinedButton(
                    "Crear",
                    style = ft.ButtonStyle(
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
                    height = 40,
                                    
                    icon = ft.Icons.LABEL,
                    on_click = abrir_formulario_crear_categoria_modal # Al hacer clic, sobre el boton de "Crear" se abrira el modal
                ),

                # Campo de busqueda
                busqueda_input,

            ]
        ),
        bgcolor = "#ffffff",
        border = ft.Border.all(
            1,
            "#e2dcd5"
        ),
        border_radius = 10,
        padding = 10
    )

    # ================= CONTENIDO PRINCIPAL =================
    contenido_principal = ft.Container(
        padding = 10,
        content = ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        ft.Row(
                            controls = [
                                # Titulo de la sección
                                ft.Text(
                                    "Categorías",
                                    size = 28,
                                    weight = ft.FontWeight.BOLD,
                                    color = "#6b1d41"
                                ),

                                # Barra de acciones
                                barra_de_acciones,

                                # Boton para cerrar la lista
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
                            ],
                            expand = True,
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        # ft.OutlinedButton(
                        #     "Regresar",
                        #     icon = ft.Icons.ARROW_BACK,
                        #     on_click = lambda e: regresar()
                        # )
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                
                ft.Container(
                    content = tabla,
                    border = ft.Border.all(
                        1,
                        "#ede9e4"
                    ),
                    expand = True,
                    border_radius = 10,
                    width = 5000,
                    padding = 0,
                    bgcolor = "#ffffff"
                ),

                mensaje
            ],
            spacing = 10,
            scroll = ft.ScrollMode.AUTO
        )
    )

    contenido_en_pila = ft.Container(
        content = contenido_principal,
        bgcolor = "#f9f6f0",
        border = ft.Border.all(
            1,
            "#e2dcd5"
        ),
        border_radius = 20,
        margin = ft.Margin.only(top = 70, left = 150),
        padding = 30,
        shadow = ft.BoxShadow(
            spread_radius = 1, # Expansión de la sombra
            blur_radius = 20, #Difuminado
            color = ft.Colors.BLACK_38
        ),
        width = 1000,
        height = 600
    )

    # --------------- Agregar el contenido principal a la pila ----------------
    pila.controls.append(contenido_en_pila)

    # ---------------- Cargar datos iniciales (SIN actualizar) ------------------
    # Solo cargaran los datos, pero NO se hace update porque la pila aun no esta en la pagina. La actualización se hara cuando se agregue.
    try:
        categorias = cargar_categorias()

        tabla.rows.clear()
        for categoria in categorias:

            tabla.rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(categoria.categoria_categoria, color = "#0d1b2a",)),
                        ft.DataCell(ft.Text(categoria.categoria_tipo, color = "#0d1b2a", text_align = ft.TextAlign.CENTER, weight = ft.FontWeight.BOLD, width = 100, expand = True)),
                        ft.DataCell(ft.Text(categoria.categoria_descripcion, color = "#0d1b2a",)),
                        ft.DataCell(
                            ft.Row(
                                controls = [
                                    # Boton Editar
                                    ft.OutlinedButton(
                                        #f"Editar ID:{categoria.categoria_id}",
                                        "Editar",
                                        data = categoria.categoria_id, # Recuperar el ID de la categoria

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

                                        on_click = abrir_formulario_editar_categoria # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                    ),

                                    # Boton Eliminar
                                    ft.OutlinedButton(
                                        #f"Eliminar ID:{categoria.categoria_id}",
                                        "Eliminar",
                                        data = categoria.categoria_id, # Recuperar el ID de la categoria
    
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
    
                                        on_click = abrir_alerta_eliminar_categoria # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                    ) 
                                ]
                            )
                        )
                    ]
                )
            )

    except Exception as error:
        print(f"Error al consultar las categorias: {error}")

    return pila
    