import flet as ft

from models.articulo import Articulo
from dao.articulo_dao import ArticuloDAO

def punto_de_venta(regresar=None):
    # ============================================================
    # ====== CONTENEDOR PRINCIPAL ================================
    # ============================================================
    pila = ft.Stack(expand=True)
    
    # ============================================================
    # ====== VARIABLES DE ESTADO =================================
    # ============================================================
    todos_los_articulos = []
    producto_seleccionado = None
    sugerencias_visibles = False

    # ============================================================
    # ====== FUNCIONES PARA CARGAR DATOS ==========================
    # ============================================================
    def cargar_articulos():
        """Carga todos los artículos desde la base de datos"""
        nonlocal todos_los_articulos
        try:
            articulo_dao = ArticuloDAO()
            todos_los_articulos = articulo_dao.obtener_todos()
            print(f"Artículos cargados: {len(todos_los_articulos)}")
        except Exception as error:
            print(f"Error al cargar artículos: {error}")

    # ============================================================
    # ====== FUNCIONES DE BÚSQUEDA ================================
    # ============================================================
    def obtener_sugerencias(texto, campo):
        """Obtiene sugerencias basadas en el texto y el campo de búsqueda"""
        if not texto or texto.strip() == "":
            return []
        
        texto = texto.lower().strip()
        sugerencias = []
        
        for articulo in todos_los_articulos:
            if campo == "codigo":
                valor = articulo.articulo_codigo.lower()
            else:  # nombre
                valor = articulo.articulo_articulo.lower()
            
            if texto in valor:
                sugerencias.append(articulo)
        
        return sugerencias[:10]

    def buscar_por_codigo(e):
        """Busca productos por código mientras el usuario escribe"""
        texto = e.control.value
        sugerencias = obtener_sugerencias(texto, "codigo")
        actualizar_sugerencias(sugerencias, "codigo")

    def buscar_por_nombre(e):
        """Busca productos por nombre mientras el usuario escribe"""
        texto = e.control.value
        sugerencias = obtener_sugerencias(texto, "nombre")
        actualizar_sugerencias(sugerencias, "nombre")

    def actualizar_sugerencias(sugerencias, tipo):
        """Actualiza la lista de sugerencias en el popup"""
        nonlocal sugerencias_visibles
        
        contenedor_sugerencias.content.controls.clear()
        
        if not sugerencias:
            contenedor_sugerencias.visible = False
            pila.page.update()
            return
        
        sugerencias_visibles = True
        
        for articulo in sugerencias:
            if tipo == "codigo":
                texto_mostrar = f"{articulo.articulo_codigo} - {articulo.articulo_articulo}"
            else:
                texto_mostrar = f"{articulo.articulo_articulo} ({articulo.articulo_codigo})"
            
            # === FUNCIÓN PARA HOVER ===
            def on_sugerencia_hover(e):
                """Cambia el color de fondo al pasar el mouse"""
                e.control.bgcolor = "#f9f6f0" if e.data == "true" else "#ffffff"
                e.control.update()
            
            sugerencia = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(texto_mostrar, size=14, color="#6b1d41"),
                        ft.Container(expand=True)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.Padding.symmetric(horizontal=15, vertical=10),
                bgcolor="#ffffff",
                border=ft.Border.only(bottom=ft.BorderSide(width=1, color="#f0eee9")),
                on_click=lambda e, a=articulo: seleccionar_producto(a, tipo),
                on_hover=on_sugerencia_hover,  # <--- Función separada
                animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            )
            contenedor_sugerencias.content.controls.append(sugerencia)
        
        contenedor_sugerencias.visible = True
        pila.page.update()

    # ============================================================
    # ====== FUNCIONES DE SELECCIÓN ===============================
    # ============================================================
    def seleccionar_producto(articulo, tipo):
        """Selecciona un producto y actualiza la interfaz"""
        nonlocal producto_seleccionado, sugerencias_visibles
        
        producto_seleccionado = articulo
        print(f"✅ Producto seleccionado: {articulo.articulo_articulo}")
        
        if tipo == "codigo":
            campo_codigo.value = articulo.articulo_codigo
            campo_nombre.value = articulo.articulo_articulo
        else:
            campo_nombre.value = articulo.articulo_articulo
            campo_codigo.value = articulo.articulo_codigo
        
        imagen_producto.src = "https://via.placeholder.com/150x150/6b1d41/ffffff?text=Producto"
        imagen_producto.visible = True
        
        texto_existencias.value = f"Existencias: {articulo.articulo_stock}"
        boton_agregar.disabled = False
        
        contenedor_sugerencias.visible = False
        sugerencias_visibles = False
        
        pila.page.update()

    def ocultar_sugerencias(e):
        """Oculta las sugerencias al perder el foco"""
        nonlocal sugerencias_visibles
        import time
        time.sleep(0.2)
        contenedor_sugerencias.visible = False
        sugerencias_visibles = False
        pila.page.update()

    # ============================================================
    # ====== BOTÓN AGREGAR ========================================
    # ============================================================
    def agregar_a_lista(e):
        if not producto_seleccionado:
            print("❌ No hay producto seleccionado")
            return
        
        cantidad = obtener_cantidad_valor()
        print(f"✅ Producto agregado: {producto_seleccionado.articulo_articulo} x{cantidad}")
        print(f"   Precio: ${producto_seleccionado.articulo_precio:.2f}")

    # ============================================================
    # ====== CARGAR DATOS INICIALES ==============================
    # ============================================================
    cargar_articulos()

    # ============================================================
    # ====== INTERFAZ DE USUARIO ================================
    # ============================================================
    
    titulo = ft.Text(
        "Punto de Venta",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="#6b1d41",
    )

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
    
    campo_codigo = ft.TextField(
        label="Código",
        hint_text="Buscar por código...", # Esto es el placeholder
        on_change=buscar_por_codigo,
        on_blur=ocultar_sugerencias,

        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_click = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        focused_border_color = "#c9a03d", # Borde al enfocar
        color = "#424955",

        fill_color = ft.Colors.WHITE, # Fondo del campo (requiere filled=True o estilo)
        filled = True, # Activa el relleno
        bgcolor = "#f9f6f0", # Fondo del menú desplegable
        width = 380,

        # suffix=ft.Icon(ft.Icons.SEARCH, color="#6b1d41"),
    )
    
    campo_nombre = ft.TextField(
        label="Nombre",
        hint_text="Buscar por nombre...",
        on_change=buscar_por_nombre,
        on_blur=ocultar_sugerencias,

        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_click = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        focused_border_color = "#c9a03d", # Borde al enfocar
        color = "#424955",

        fill_color = ft.Colors.WHITE, # Fondo del campo (requiere filled=True o estilo)
        filled = True, # Activa el relleno
        bgcolor = "#f9f6f0", # Fondo del menú desplegable
        width = 380,

        # suffix=ft.Icon(ft.Icons.SEARCH, color="#6b1d41"),
    )
    
    contenedor_sugerencias = ft.Container(
        content=ft.Column(
            controls=[],
            spacing=0,
        ),
        bgcolor="#f9f6f0",
        border=ft.Border.all(1, "#e2dcd5"),
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.BLACK26,
        ),
        visible=False,
        margin=ft.Margin.only(top=5),
        width = 380
    )
    
    imagen_producto = ft.Image(
        src = f"imagenes/imagenes_DB/a-bottle-of-wine-on-a-dark-background_acostada.jpg",
        expand = True
    )

    # Definir el valor inicial del campo Stock
    def reiniciar_valor(e):
        # Si el valor es vacío o no es un número válido, establecer 0
        if not e.control.value or not e.control.value.lstrip('-').isdigit():
            e.control.value = "1"
            e.page.update()
        else:
            # Opcional: convertir a int/float si se requiere cálculo
            pass

    cantidad_input = ft.TextField(
        label = "Stock: ",
        value = "1", # Valor inicial del stock
        # Habre un: Teclado numerico en telefonos o tablets sin decimales
        keyboard_type = ft.KeyboardType.NUMBER,
        # Filtro para permitir solo números (incluyendo signo negativo)
        input_filter = ft.InputFilter(
            allow = True,
            # No valores negativos ni caracteres
            regex_string = r"[0-9-]",
            replacement_string = ""
        ),
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(),
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        hint_text = "0",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        width = 200,
        color = "#424955",

        # Cuando se introduce un valor invalido, se reinicia el valor a 0
        on_change = reiniciar_valor
        # Actualizar la variable interna si el usuario borra todo
    )

    def obtener_cantidad_valor():
        try:
            if not cantidad_input.value or cantidad_input.value.strip() == "":
                return 1
            return int(cantidad_input.value)
        except ValueError:
            return 1
        
    # Definir el metodo para decrementar
    def decremento_click(e):
        valor = obtener_cantidad_valor()
        if valor > 1:
            # Restar 1 y convertir de nuevo a string
            cantidad_input.value = str(valor - 1)
            # Actualizar el estado del boton
            boton_decremento_activo()
            e.page.update()

    # Definir el metodo para incrementar
    def incremento_click(e):
        valor = obtener_cantidad_valor()
        # Convertir a entero, sumar 1 y convertir de nuevo a string
        cantidad_input.value = str(valor + 1)
        # Actualizar la interfaz para hacer el incremento
        boton_decremento_activo()
        e.page.update()

    def boton_decremento_activo():
        valor = obtener_cantidad_valor()
        esta_activo = valor > 1

        # Actualizar el boton de decremento
        if esta_activo:
            boton_decremento.content = ft.IconButton(
                # Botón de resta (icono flecha abajo)
                icon = ft.Icons.ARROW_DROP_DOWN,
                icon_size = 20, # Cambia el tamaño visual del ícono
                scale = 1.0, # Escala el botón completo
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                    padding = ft.Padding.symmetric(horizontal = 5, vertical = 2),
                ),
                bgcolor = "#6b1d41",
                icon_color = "#ffffff",
                tooltip = "Decrementar", # Texto que aparece al pasar el cursor
                # Tamaño definido
                width = 30,
                height = 20,
                                        
                on_click = decremento_click
            )
        else:
            boton_decremento.content = ft.IconButton(
                # Botón de resta (icono flecha abajo)
                icon = ft.Icons.ARROW_DROP_DOWN,
                icon_size = 20, # Cambia el tamaño visual del ícono
                scale = 1.0, # Escala el botón completo
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                    padding = ft.Padding.symmetric(horizontal = 5, vertical = 2),
                ),
                bgcolor = "#696768",
                icon_color = "#ffffff",
                tooltip = "Decrementar", # Texto que aparece al pasar el cursor
                # Tamaño definido
                width = 30,
                height = 20,
                                        
                # on_click = decremento_click
            ) # NO COLOCAR LA COMA, DE LO CONTRARIO EL ESTILO DE BOTON INACTIVO NO SE MOSTRARA
    
    # Crear el contenedor del boton
    boton_decremento = ft.Container()

    # Inicializar el estado del boton
    boton_decremento_activo()

    texto_existencias = ft.Text(
        "Existencias: ---",
        size=14,
        color="#9095a0",
        weight=ft.FontWeight.W_500,
        text_align = ft.TextAlign.CENTER,
        margin = ft.Margin.only(top = 12)
    )

    contenedor_existencias = ft.Container(
        content = texto_existencias,
        bgcolor = "#dee1e6", 
        border_radius = 4,
        border = ft.Border.all(
            1,
            "#c9a03d"
        ),
        height = 48,
        width = 240
    )
    
    boton_agregar = ft.ElevatedButton(
        "Agregar",
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
        # on_click=agregar_a_lista,
    )
    
    campos_con_sugerencias = ft.Stack(
        controls=[
            ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            campo_codigo,
                            campo_nombre,
                        ],
                        spacing = 15,
                    ),
                    contenedor_sugerencias,
                ],
                spacing=0,
            ),
        ]
    )

    campo_de_cantidad_existencias = ft.Column(
        controls = [
            ft.Row(
                controls = [
                    # Campo de cantidad
                    ft.Row(
                        controls = [
                            cantidad_input,
                        ]
                    ),
                    

                    # Botones de incremento y decremento
                    ft.Column(
                        controls = [
                            # Botón de suma (icono flecha arriba)
                            ft.IconButton(
                                icon = ft.Icons.ARROW_DROP_UP,
                                icon_size = 20, # Cambia el tamaño visual del ícono
                                scale = 1.0, # Escala el botón completo
                                style = ft.ButtonStyle(
                                    shape = ft.RoundedRectangleBorder(radius = 5),
                                    padding = ft.Padding.symmetric(horizontal = 5, vertical = 2),
                                ),
                                bgcolor = "#6b1d41",
                                icon_color = "#ffffff",
                                tooltip = "Incrementar", # Texto que aparece al pasar el cursor
                                # Tamaño definido
                                width = 30,
                                height = 20,

                                on_click = incremento_click
                            ),

                            # Botón de resta (dinamico)
                            boton_decremento,
                        ],
                        spacing = 6
                    ),
                ],
                margin = ft.Margin.only(bottom = 5)
            ),

            contenedor_existencias
        ],
    )
    
    formulario = ft.Container(
        content = ft.Row(
            controls = [
                ft.Row(
                    controls = [
                        campos_con_sugerencias,
                        campo_de_cantidad_existencias,
                        ft.Container(
                            content = imagen_producto,
                            border_radius = 10,
                            height = 110
                        )
                    ]
                ),
                
                boton_agregar,
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=15
        ),
        bgcolor="#ffffff",
        border=ft.Border.all(1, "#e2dcd5"),
        border_radius=10,
        padding=20,
    )

    contenido_principal = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                titulo,
                ft.Divider(height=10, color="transparent"),
                formulario,
            ],
            spacing=10,
            expand=True,
        ),
        expand=True,
    )

    pila.controls.append(contenido_principal)

    return pila