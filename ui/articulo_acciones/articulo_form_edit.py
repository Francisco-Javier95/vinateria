import flet as ft

import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

from models.articulo import Articulo
from models.articulo import Articulo_editar
from dao.articulo_dao import ArticuloDAO
from dao.categoria_dao import CategoriaDAO
from dao.proveedor_dao import ProveedorDAO

def articulo_form_edit(regresar = None, formulario_visible = False, cerrando_modal = None, registro = None):
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
    articulo_input = ft.TextField(
        label = "Nombre: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        hint_text = "Champagne",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        # Número máximo de caracteres
        max_length = 25, # Limita a 25 caracteres / crea un contador y lo muestra debajo del input (campo)
        counter = ft.Container(), # No mostrar contador

        value = registro.get('nombre') if registro else "" # Cargar datos
    )
    codigo_input = ft.TextField(
        label = "Código: ",
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label normal
        hint_text = "123-456-789",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        # Numero maximo de caracteres
        max_length = 10, # Limita a 10 caracteres / crea un contador y lo muestra debajo del input (campo)
        counter = ft.Container(), # No mostrar contador

        value = registro.get('codigo') if registro else "" # Cargar datos
    )

    # --------- Dropdown para categorìas ---------
    categoria_input = ft.Dropdown(
        label = "Categoría: ",
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        tooltip = "Selecciona una categoría...",
        options = [], # Mostrar las categorias
        expand = True,
        menu_height = 200, # ALTURA MÁXIMA (5 items aprox)

        color = "#6b1d41", # Color del texto
        fill_color = ft.Colors.WHITE, # Fondo del campo (requiere filled=True o estilo)
        filled = True, # Activa el relleno
        border_color = "#916500", # Color del borde
        focused_border_color = "#c9a03d", # Borde al enfocar
        bgcolor = "#f9f6f0", # Fondo del menú desplegable

        value = registro.get('categoria_id') if registro else None # Cargar datos
    )

    # Metodo para cargar las categorias desde la Base de Datos
    def cargar_categorias():
        try:
            categoria_nombre_dao = CategoriaDAO()
            categorias = categoria_nombre_dao.nombres_categorias()

            categoria_input.options.clear() # Limpia las opciones del dropdown

            for categoria in categorias:
                categoria_input.options.append(
                    ft.dropdown.Option(
                        key = categoria.categoria_id,
                        text = categoria.categoria_categoria,
                        style=ft.TextStyle(
                            color="#6b1d41",
                            size=14
                        )
                    ),
                )
                print(f"ID: {categoria.categoria_id}, Empleado: {categoria.categoria_categoria}")
            # Si hay categorias, seleccionar la primera por defecto
            if categoria_input.options:
                if registro and registro.get('categoria_id'):
                    # Buscar la categoria que coincida
                    for option in categoria_input.options:
                        if option.key == registro.get('categoria_id'):
                            categoria_input.value = option.key
                            break
                else:
                    categoria_input.value = categoria_input.options[0].key

        except Exception as error:
            mensaje.value = f"Error al consultar las categorías: {error}"
            mensaje.color = ft.Colors.RED

    # ----------------- Campo de imagen ---------------------
    CARPETA_IMAGENES = "assets/imagenes/imagenes_DB"
    if not os.path.exists(CARPETA_IMAGENES):
        os.makedirs(CARPETA_IMAGENES)

    # === VARIABLES DE ESTADO PARA LA IMAGEN ===
    nombre_imagen_antigua = registro.get('imagen') if registro else None  # Imagen actual en BD
    nombre_imagen_nueva = None  # Nueva imagen seleccionada (temporal)
    eliminar_imagen_actual = False  # Bandera para eliminar la imagen antigua al guardar

    # === FUNCIÓN PARA SELECCIONAR IMAGEN CON TKINTER ===
    def seleccionar_imagen_tkinter():
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        archivo = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.webp")]
        )
        root.destroy()
        return archivo

    # === FUNCIÓN PARA PROCESAR LA IMAGEN SELECCIONADA ===
    def on_seleccionar_imagen(e):
        nonlocal nombre_imagen_nueva, eliminar_imagen_actual

        archivo = seleccionar_imagen_tkinter()
        if archivo:
            # Generar nombre único para la nueva imagen
            nombre_original = os.path.basename(archivo)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_base, extension = os.path.splitext(nombre_original)
            nombre_nuevo = f"{nombre_base}_{timestamp}{extension}"

            # Guardar el nombre de la nueva imagen (aún no se copia físicamente)
            nombre_imagen_nueva = nombre_nuevo

            # Mostrar la vista previa (usando la ruta temporal del archivo original)
            imagen_previa.src = archivo  # Mostrar desde la ubicación original
            imagen_previa.visible = True
            e.page.update()

            # Si hay una imagen antigua y no se ha marcado para eliminar, la marcamos
            if nombre_imagen_antigua and not eliminar_imagen_actual:
                eliminar_imagen_actual = True
        else:
            print("Selección cancelada")

    # === CONTROLES DE INTERFAZ ===
    imagen_previa = ft.Image(
        src = f"assets/imagenes/imagenes_DB/{nombre_imagen_antigua}" if nombre_imagen_antigua else "",
        width=150,
        height=175,
        border_radius=10,
        visible=bool(nombre_imagen_antigua)
    )

    # Botón que actúa como contenedor de la imagen (fondo por defecto)
    btn_seleccionar = ft.OutlinedButton(
        content=imagen_previa,
        on_click=on_seleccionar_imagen,
        style=ft.ButtonStyle(
            bgcolor = {
                ft.ControlState.HOVERED: "#ede9e4",
                ft.ControlState.DEFAULT: "#ffffff",
            },
            side = {
                ft.ControlState.DEFAULT: ft.BorderSide(width=1, color="#ede9e4"),
                ft.ControlState.HOVERED: ft.BorderSide(width=1, color="#916500"),
            },
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=0,
        ),
        expand = True,
        tooltip = "Añadir imagen"
    )

    campo_imagen = ft.Column(
        controls=[
            ft.Row(controls=[btn_seleccionar], spacing=10),
        ],
        spacing=5,
    )
    
    # imagen_input = ft.TextField(
    #     label = "Imagen: ",
    #     label_style = estilo_de_label,
    #     on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(),
    #     on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
    #     hint_text = "imagen.jpg",  # Esto es el placeholder
    #     focused_border_color = "#c9a03d", # Borde al enfocar
    #     expand = True,
    #     color = "#424955",

    #     value = registro.get('imagen') if registro else "" # Cargar datos
    # )

    precio_input = ft.TextField(
        label = "Precio: ",
        label_style = estilo_de_label,
        # Habre un: Teclado numerico con decimal en telefonos o tablets
        keyboard_type=ft.KeyboardType.NUMBER,
        # Filtro para permitir solo numeros con . para decimales
        input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^[0-9]*\.?[0-9]*$",  # Permite números y punto decimal
            replacement_string=""
        ),
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(),
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        hint_text = "0.00",  # Esto es el placeholder
        focused_border_color = "#c9a03d", # Borde al enfocar
        expand = True,
        color = "#424955",

        # 'suffix_icon' Sirve para colocar un icono en el input despues del texto
        suffix_icon = ft.Icons.ATTACH_MONEY, # Icono de $

        value = registro.get('precio') if registro else "", # Cargar datos

        # Numero maximo de caracteres
        max_length = 10, # Limita a 10 caracteres
        counter = ft.Container() # No mostrar contador
    )

    # Definir el valor inicial del campo Stock
    def reiniciar_valor(e):
        # Si el valor es vacío o no es un número válido, establecer 0
        if not e.control.value or not e.control.value.lstrip('-').isdigit():
            e.control.value = "0"
            e.page.update()
        else:
            # Opcional: convertir a int/float si se requiere cálculo
            pass

    stock_input = ft.TextField(
        label = "Stock: ",
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
        expand = True,
        color = "#424955",

        value = registro.get('stock') if registro else "", # Cargar datos

        # Cuando se introduce un valor invalido, se reinicia el valor a 0
        on_change = reiniciar_valor
        # Actualizar la variable interna si el usuario borra todo
    )

    def obtener_stock_valor():
        try:
            if not stock_input.value or stock_input.value.strip() == "":
                return 0
            return int(stock_input.value)
        except ValueError:
            return 0
        
    # Definir el metodo para decrementar
    def decremento_click(e):
        valor = obtener_stock_valor()
        if valor > 0:
            # Restar 1 y convertir de nuevo a string
            stock_input.value = str(valor - 1)
            # Actualizar el estado del boton
            boton_decremento_activo()
            e.page.update()

    # Definir el metodo para incrementar
    def incremento_click(e):
        valor = obtener_stock_valor()
        # Convertir a entero, sumar 1 y convertir de nuevo a string
        stock_input.value = str(valor + 1)
        # Actualizar la interfaz para hacer el incremento
        boton_decremento_activo()
        e.page.update()

    def boton_decremento_activo():
        valor = obtener_stock_valor()
        esta_activo = valor > 0

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
    
    proveedor_input = ft.Dropdown(
        label = "Proveedor: ",
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        tooltip = "Selecciona un proveedor...",
        options = [], # Mostrar los proveedores
        expand = True,
        menu_height = 200, # ALTURA MÁXIMA (5 items aprox)

        color = "#6b1d41", # Color del texto
        fill_color = ft.Colors.WHITE, # Fondo del campo (requiere filled=True o estilo)
        filled = True, # Activa el relleno
        border_color = "#916500", # Color del borde
        focused_border_color = "#c9a03d", # Borde al enfocar
        bgcolor = "#f9f6f0", # Fondo del menú desplegable

        value = registro.get('proveedor_id') if registro else None # Cargar datos
    )

    # Metodo para cargar los proveedores desde la Base de Datos
    def cargar_proveedores():
        try:
            proveedor_nombre_dao = ProveedorDAO()
            proveedores = proveedor_nombre_dao.nombres_proveedores()

            proveedor_input.options.clear() # Limpia las opciones del dropdown

            for proveedor in proveedores:
                proveedor_input.options.append(
                    ft.dropdown.Option(
                        key = proveedor.proveedor_id,
                        text = proveedor.proveedor_proveedor,
                        style=ft.TextStyle(
                            color="#6b1d41",
                            size=14
                        )
                    ),
                )
                print(f"ID: {proveedor.proveedor_id}, Empleado: {proveedor.proveedor_proveedor}")
            # Si hay proveedores, seleccionar la primera por defecto
            if proveedor_input.options:
                if registro and registro.get('proveedor_id'):
                    for option in proveedor_input.options:
                        if option.key == registro.get('proveedor_id'):
                            proveedor_input.value = option.key
                            break
                else:
                    proveedor_input.value = proveedor_input.options[0].key

        except Exception as error:
            mensaje.value = f"Error al consultar los proveedores: {error}"
            mensaje.color = ft.Colors.RED
    

    mensaje = ft.Text(
        "",
        color = ft.Colors.GREEN
    )

    # # -------------- Función para limpiar el formulario -------------------
    # def limpiar_formualrio():
    #     articulo_input.value = ""
    #     codigo_input.value = ""
    #     categoria_input.value = categoria_input.options[0].key if categoria_input.options else ""
    #     imagen_input.value = ""
    #     precio_input.value = ""
    #     stock_input.value = ""
    #     proveedor_input.value = proveedor_input.options[0].key if proveedor_input.options else ""

    def editar_articulo(evento):
        nonlocal nombre_imagen_antigua, nombre_imagen_nueva, eliminar_imagen_actual

        # Recuperar los valores de los TextFile
        articulo_articulo = articulo_input.value
        articulo_codigo = codigo_input.value
        articulo_categoria = categoria_input.value # El valor seleccionado del Dropdown
        articulo_precio = precio_input.value
        articulo_stock = stock_input.value
        articulo_proveedor = proveedor_input.value # El valor seleccionado del Dropdown

        # --- Manejo de la imagen ---
        imagen_final = None

        # Si hay una nueva imagen seleccionada, la copiamos y eliminamos la antigua
        if nombre_imagen_nueva:
            # Copiar la nueva imagen a la carpeta assets
            ruta_origen = imagen_previa.src  # Ruta temporal de la imagen seleccionada
            if os.path.exists(ruta_origen):
                ruta_destino = os.path.join(CARPETA_IMAGENES, nombre_imagen_nueva)
                try:
                    shutil.copy2(ruta_origen, ruta_destino)
                    print(f"✅ Nueva imagen copiada: {ruta_destino}")
                    imagen_final = nombre_imagen_nueva
                except Exception as error:
                    print(f"❌ Error al copiar la nueva imagen: {error}")
                    mensaje.value = f"Error al copiar la imagen: {error}"
                    mensaje.color = ft.Colors.RED
                    evento.page.update()
                    return
            else:
                mensaje.value = "❌ No se encontró el archivo de imagen temporal"
                mensaje.color = ft.Colors.RED
                evento.page.update()
                return

            # Eliminar la imagen antigua si existe y está marcada para eliminar
            if eliminar_imagen_actual and nombre_imagen_antigua:
                ruta_antigua = os.path.join(CARPETA_IMAGENES, nombre_imagen_antigua)
                if os.path.exists(ruta_antigua):
                    try:
                        os.remove(ruta_antigua)
                        print(f"🗑️ Imagen antigua eliminada: {ruta_antigua}")
                    except Exception as error:
                        print(f"⚠️ No se pudo eliminar la imagen antigua: {error}")
                # Limpiar la bandera después de eliminar
                eliminar_imagen_actual = False
        # Si no hay cambios en la imagen, mantener la existente
        else:
            imagen_final = nombre_imagen_antigua

        # Validación de campos vacíos
        if articulo_articulo == "" or articulo_codigo == "" or articulo_categoria == None or articulo_precio == "" or articulo_stock == "" or articulo_proveedor == "":
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED
            # Actualizar la interfaz para mostrar el mensaje
            evento.page.update()
            return
        try:
            articulo_dao = ArticuloDAO()
            articulo_id = registro.get('id') if registro else None

            editar_articulo = Articulo_editar(
                articulo_id = articulo_id,
                articulo_articulo = articulo_articulo,
                articulo_codigo = articulo_codigo,
                articulo_categoria = int(articulo_categoria), # Convertir a entero
                articulo_imagen = imagen_final,
                articulo_precio = float(articulo_precio), # Convertir a numero real
                articulo_stock = int(articulo_stock), # Convertir a entero
                articulo_proveedor = int(articulo_proveedor), # Convertir a entero
            )

            print(articulo_id, articulo_articulo, articulo_codigo, articulo_categoria, imagen_final, articulo_precio, articulo_stock, articulo_proveedor)

            articulo_dao.editar_form(editar_articulo)

            mensaje.value = f"Articulo {articulo_articulo} ha sido editado exitosamente"
            mensaje.color = ft.Colors.GREEN
            
            # limpiar_formualrio()

            # # ---------------------- Si el modal esta activo y si existe la función para cerrar
            # if formulario_visible and cerrando_modal:
            #     evento.page.update()
            #     cerrando_modal()
            #     return

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
                                "Editar producto",
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

    # =============== Distribución del formulario en dos columnas ===============
    # ------------ Columna izquierda -------------------------
    columna_izquierda = ft.Column(
        controls = [
            # Campo Imagen (ocupara 3 celdas de alto)
            ft.Container(
                content = campo_imagen,
                height = 174,
                expand = True
            ),
            # Fila 4: Frecio
            precio_input,
            
            # Fila 5: Stock
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    # El campo de texto
                    stock_input,

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
                spacing = 6
            ) 
        ],
        spacing = 15,
        expand = True
    )

    # ----------- Columna derecha --------------------
    columna_derecha = ft.Column(
        controls = [
            # Fila 1: Nombre
            articulo_input,
            # Fila 2: Código
            codigo_input,
            # Fila 3: Categoria
            categoria_input,
            # Fila 4: Proveedor
            proveedor_input,
            # Fila 5: Boton Editar
            ft.Row(
                controls = [
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
                        on_click = editar_articulo
                    ),
                ],
                spacing = 10,
                expand = True
            ),
        ],
        spacing = 15,
        expand = True
    )

    # ----------- Contenedor principal con dos columnas ---------------
    contenido_dos_columnas = ft.Row(
        controls = [
            columna_izquierda,
            columna_derecha,
        ],
        spacing = 20,
        expand = True,
        vertical_alignment = ft.CrossAxisAlignment.START
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
                                "Siempre puedes",
                                ft.TextStyle()  # Estilo en negrita
                            ),
                            ft.TextSpan(
                                " editar",
                                ft.TextStyle(weight=ft.FontWeight.BOLD) # Este texto es normal
                            ),
                            ft.TextSpan(
                                " los datos de los ",
                                ft.TextStyle()  # Estilo en negrita
                            ),
                            ft.TextSpan(
                                "productos",
                                ft.TextStyle(weight=ft.FontWeight.BOLD)  # Este texto es normal
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
            
            contenido_dos_columnas,

            mensaje
        ],
        spacing = 15,
        expand = True
    )

    # Cargar las categorias
    cargar_categorias()

    # Cargar los proveedores
    cargar_proveedores()

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
    