import flet as ft

from models.articulo import Articulo
from dao.articulo_dao import ArticuloDAO
from ui.articulo_acciones.articulo_form_create import articulo_form
from ui.articulo_acciones.articulo_form_edit import articulo_form_edit
from ui.articulo_acciones.articulo_alert_delete import alerta_eliminar

from ui.articulo_acciones.categorias_list import categorias_list

def articulos_list(regresar):
    # ---------------- Variables de estado -------------------
    capa_oscura_abierta_modal = False # Indica si el modal esta visible/activo
    capa_oscura_modal = None # Es el contenido con backgroud oscuro semitransparente (capa oscuara)
    pagina_referencia = None # Guardar la referencia a la pagina (contenido)
    
    todos_los_articulos = [] # Guardar todos los articulos sin filtrar

    # -------------- Contenedor de capas ---------------------
    pila = ft.Stack(expand = True) # ft.Stack permite superponer widgets (elementos)
    # 'expand = True' hace que ocupe todo el espacio disponible
    
    # ======= CONTENEDOR PARA TARJETAS (GRID) =======
    # Grid de productos

    grid_articulos = ft.GridView(
        expand = True,
        runs_count = 5,  # 5 columnas
        max_extent = 300,
        child_aspect_ratio = 0.75,  # Relación de aspecto (ancho/alto)
        spacing = 15,
        run_spacing = 15,
        padding = 0,
        auto_scroll = True,
    )

    mensaje = ft.Text()

    # Metodo para crear las tarjetas
    def crear_tarjeta_articulo(articulo):
        # Crea una tarjeta para un artículo individual
        
        # --- IMAGEN (estática por ahora) ---
        imagen = ft.Image(
            src = f"assets/imagenes/imagenes_DB/{articulo.articulo_imagen}",  # Imagen estática de ejemplo
            expand = True
        )
        
        # --- NOMBRE ---
        nombre = ft.Text(
            articulo.articulo_articulo,
            size = 20,
            weight = ft.FontWeight.BOLD,
            color = "#6b1d41",
            max_lines = 2
        )
        
        # --- CATEGORÍA Y PROVEEDOR ---
        categoria_proveedor = ft.Row(
            controls = [
                ft.Container(
                    content = ft.Text(
                        str(articulo.articulo_categoria),
                        size = 16,
                        color = "#9095a0",
                    ),
                ),

                ft.Container(content = ft.Text(""), height = 20, width = 1, bgcolor = "#e2dcd5"),

                ft.Container(
                    content = ft.Text(
                        str(articulo.articulo_proveedor),
                        size = 16,
                        color="#9095a0",
                        text_align = ft.TextAlign.CENTER,
                        expand = True
                    ),
                ),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing = 0,
        )
        
        # --- STOCK Y PRECIO ---
        stock_precio = ft.Row(
            controls = [
                ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.Text(
                                f"Stock: {articulo.articulo_stock}",
                                size = 16,
                                color = "#424955",
                                weight = ft.FontWeight.W_500,
                            ),
                        ],
                        spacing = 2,
                    ),
                    padding = ft.Padding.symmetric(horizontal = 0, vertical = 2),
                ),
                ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.Icon(
                                ft.Icons.ATTACH_MONEY,
                                size = 18,
                                color = "#c9a03d"
                            ),
                            ft.Text(
                                f"{articulo.articulo_precio:.2f}",
                                size = 18,
                                color = "#c9a03d",
                                weight = ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing = 2,
                    ),
                    padding = ft.Padding.symmetric(horizontal = 0, vertical = 2),
                ),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing = 0,
        )

        # Juntar categoria_proveedor y stock_precio
        categoria_proveedor_stock_precio = ft.Column(
            controls = [
                categoria_proveedor,
                stock_precio
            ],
            margin = 0,
            spacing = 0
        )
        
        # --- BOTONES DE ACCIONES ---
        acciones = ft.Row(
            controls = [
                ft.OutlinedButton(
                    "Editar",
                    data = articulo.articulo_id,
                    style = ft.ButtonStyle(
                        bgcolor = "#c9a03d",
                        side = {
                            ft.ControlState.DEFAULT: ft.BorderSide(width = 2, color = "#926600"),
                            ft.ControlState.HOVERED: ft.BorderSide(width = 2, color = "#c9a03d"),
                        },
                        color = "#ffffff",
                        shape = ft.RoundedRectangleBorder(radius = 10),
                        padding = ft.Padding.symmetric(horizontal = 10, vertical = 17),
                    ),
                    expand = True,
                    on_click = abrir_formulario_editar_modal,
                ),
                ft.OutlinedButton(
                    "Eliminar",
                    data = articulo.articulo_id,
                    style = ft.ButtonStyle(
                        bgcolor = {
                            ft.ControlState.HOVERED: "#de3b40",
                            ft.ControlState.DEFAULT: "#f3f4f6",
                        },
                        side = {
                            ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#de3b40"),
                            ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#de3b40"),
                        },
                        color = {
                            ft.ControlState.HOVERED: "#ffffff",
                            ft.ControlState.DEFAULT: "#de3b40",
                        },
                        shape = ft.RoundedRectangleBorder(radius = 10),
                        padding = ft.Padding.symmetric(horizontal = 10, vertical = 17),
                    ),
                    expand = True,
                    on_click = abrir_alerta_eliminar_articulo,
                ),
            ],
            spacing = 10,
            alignment = ft.MainAxisAlignment.CENTER,
        )
        
        # --- TARJETA COMPLETA ---
        tarjeta = ft.Container(
            content = ft.Column(
                controls = [
                    # Imagen
                    ft.Container(
                        content = (
                            imagen
                        ),
                        border_radius = 5,
                        height = 170,
                        width = 275,
                        bgcolor = "#000000",
                        align=ft.Alignment.CENTER
                    ),
                    # Contenido de la tarjeta
                    ft.Container(
                        content = ft.Column(
                            controls = [
                                nombre,
                                categoria_proveedor_stock_precio
                            ],
                            spacing = 8,
                        ),
                        padding = ft.Padding.symmetric(horizontal = 2, vertical = 5),
                        expand = True,
                    ),
                    # Acciones
                    ft.Container(
                        content = (
                            acciones
                        )
                    )
                ],
                spacing = 4,
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                # horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            ),
            padding = 4,
            bgcolor = "#ffffff",
            border = ft.Border.all(
                1,
                "#e2dcd5"
            ),
            border_radius = 10,
            height = 900
        )
        
        return tarjeta

    # GRID de las tarjetas de los productos
    def mostrar_articulos_en_grid(articulos):
        """Muestra una lista de artículos en el grid de tarjetas"""
        grid_articulos.controls.clear()

        for articulo in articulos:
            tarjeta = crear_tarjeta_articulo(articulo)
            grid_articulos.controls.append(tarjeta)
        
        # Actualizar la interfaz
        if pila.page:
            pila.update()
        elif pagina_referencia:
            pagina_referencia.update()

    # -----------------Función para cargar los productos/articulos----------------------
    def cargar_articulos():
        # Cargar todos los articulos de la base de datos
        nonlocal todos_los_articulos

        try:
            articulo_dao = ArticuloDAO()
            articulos = articulo_dao.obtener_todos()

            # Guardar todos los articulos
            todos_los_articulos = articulos

            # Mostrar todos los articulos
            mostrar_articulos_en_grid(articulos)

        except Exception as error:
            print(f"Error al consultar los productos: {error}")
            
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()

        return articulos

    def buscar_articulos(e):
        # Filtrar los articulo en tiempo real mediante el campo de nombre

        texto_busqueda = busqueda_input.value.lower().strip() if busqueda_input.value else ""

        # Si el campo de busqueda esta vacio se mostraran todos los articulos (registros)
        if texto_busqueda == "":
            mostrar_articulos_en_grid(todos_los_articulos)
            return
        
        # Filtrar articulos por nombre
        articulos_filtrados = [
            articulo for articulo in todos_los_articulos
            if texto_busqueda in articulo.articulo_articulo.lower()
        ]

        # Mostrar los articulos filtrados
        mostrar_articulos_en_grid(articulos_filtrados)

        # Mostrar mensaje si no hay resultados
        if not articulos_filtrados:
            print(f"No se encontraron articulos con '{texto_busqueda}'")
            if pila.page:
                pila.update()
            else:
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

    def abrir_tabla_categoria_model(evento):
        # Crear y muestrar el modal con la tabla de "Categorías"
        # evento: El evento del clic en el boton "Categorías"

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = categorias_list(
            tabla_categoria_visible = True, # Activar el modal, mostrando el formulario
            cerrando_modal = cerrar_modal
        )

        # --------------- Crear la capa oscura (OVERLAY) --------------
        capa_oscura = ft.Container(
            expand = True,
            bgcolor = ft.Colors.BLACK_45,
            content = ft.Column(
                controls = [contenido_modal],
                alignment = ft.MainAxisAlignment.CENTER,
                width = 5000,
                height = 5000
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

        on_change = buscar_articulos, # Buscar en tiempo real

        # 'suffix_icon' Sirve para colocar un icono en el input despues del texto
        suffix_icon = ft.Icon(
            ft.Icons.SEARCH_OUTLINED, # Icono de $
            color = "#6b1d41"

        ),
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
                                    
                    icon = ft.Icons.WINE_BAR,
                    on_click = abrir_formulario_crear_modal # Al hacer clic, sobre el boton de "Crear" se abrira el modal
                ),

                # Campo de busqueda
                busqueda_input,

            ],
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
                                # Titulo del segmento
                                ft.Text(
                                    "Inventario",
                                    size = 28,
                                    weight = ft.FontWeight.BOLD,
                                    color = "#6b1d41"
                                ),
                                # Mostrar la barra de acciones
                                barra_de_acciones,

                                # Boton de la lista de categorías
                                ft.OutlinedButton(
                                    "Categorías",
                                    style = ft.ButtonStyle(
                                        bgcolor = "#c9a03d", # Color de fondo
                                        side = {
                                            ft.ControlState.DEFAULT:
                                            ft.BorderSide(
                                                width = 2,
                                                color = "#926600"
                                            ),
                                            ft.ControlState.HOVERED:
                                            ft.BorderSide(
                                                width = 2,
                                                color = "#c9a03d"
                                            )
                                        },
                                        color = "#ffffff",
                                        shape = ft.RoundedRectangleBorder(radius = 10)
                                    ),
                
                                    height = 40,
                
                                    on_click = abrir_tabla_categoria_model # Al hacer click, sobre el boton de "Categorías"
                                )
                            ],
                            expand = True,
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        # ft.OutlinedButton(
                        #     "Regresar",
                        #     icon = ft.Icons.ARROW_BACK,
                        #     on_click = lambda e: regresar()
                        # )
                    ]
                ),
                
                ft.Container(
                    content = grid_articulos,
                    expand = True,
                    width = 5000
                ),

                mensaje
            ],
            spacing = 10,
            scroll = ft.ScrollMode.AUTO
        )
    )

    # --------------- Agregar el contenido principal a la pila ----------------
    pila.controls.append(contenido_principal)

    # ---------------- Cargar datos iniciales (SIN actualizar) ------------------
    # Solo cargaran los datos, pero NO se hace update porque la pila aun no esta en la pagina. La actualización se hara cuando se agregue.
    try:
        articulos = cargar_articulos()

        grid_articulos.controls.clear()
        for articulo in articulos:
            tarjeta = crear_tarjeta_articulo(articulo)
            grid_articulos.controls.append(tarjeta)

    except Exception as error:
        print(f"Error al consultar los productos: {error}")

    return pila