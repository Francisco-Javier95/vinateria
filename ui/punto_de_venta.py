import flet as ft

import math

from models.articulo import Articulo
from dao.articulo_dao import ArticuloDAO

import globals # Importar el archivo de la variable local "venta_pediente_global"

from ui.venta_acciones.venta_form_confirm import confirmar_form
from ui.venta_acciones.venta_form_save import guardar_form
from ui.venta_acciones.venta_alert_cancel import alerta_cancelar
from ui.venta_acciones.venta_alert_cancel_2 import alerta_cancelar_2

def punto_de_venta(regresar=None):
    # ---------------- Variables de estado -------------------
    todos_los_articulos = []
    lista_compra = []  # Lista de productos agregados
    producto_seleccionado = None
    sugerencias_visibles = False
    venta_actual_id = None

    capa_oscura_abierta_modal = False # Indica si el modal esta visible/activo
    capa_oscura_modal = None # Es el contenido con backgroud oscuro semitransparente (capa oscuara)
    pagina_referencia = None # Guardar la referencia a la pagina (contenido)

    # -------------- Contenedor de capas ---------------------
    pila = ft.Stack(expand = True) # ft.Stack permite superponer widgets (elementos)
    # 'expand = True' hace que ocupe todo el espacio disponible

    # Metodo de cargar articulos
    def cargar_articulos():
        # Carga todos los artículos desde la base de datos
        nonlocal todos_los_articulos
        try:
            articulo_dao = ArticuloDAO()
            todos_los_articulos = articulo_dao.obtener_todos()
            print(f"Artículos cargados: {len(todos_los_articulos)}")
        except Exception as error:
            print(f"Error al cargar artículos: {error}")

    # Función e 'Busqueda'
    def obtener_sugerencias(texto, campo):
        # Obtiene sugerencias basadas en el texto y el campo de búsqueda
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
        # Busca productos por código mientras el usuario escribe
        texto = e.control.value
        sugerencias = obtener_sugerencias(texto, "codigo")
        actualizar_sugerencias(sugerencias, "codigo")

    def buscar_por_nombre(e):
        # Busca productos por nombre mientras el usuario escribe
        texto = e.control.value
        sugerencias = obtener_sugerencias(texto, "nombre")
        actualizar_sugerencias(sugerencias, "nombre")

    def actualizar_sugerencias(sugerencias, tipo):
        # Actualiza la lista de sugerencias en el popup
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
            
            sugerencia = ft.Container(
                content = ft.Row(
                    controls = [
                        ft.Text(texto_mostrar, size = 14, color = "#6b1d41"),
                        ft.Container(expand = True)
                    ],
                    alignment = ft.MainAxisAlignment.START,
                ),
                padding = ft.Padding.symmetric(horizontal = 15, vertical = 10),
                bgcolor = "#ffffff",
                border = ft.Border.only(bottom = ft.BorderSide(width = 1, color = "#f0eee9")),
                on_click = lambda e, a = articulo: seleccionar_producto(a, tipo),
                animate = ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            )
            contenedor_sugerencias.content.controls.append(sugerencia)
        
        contenedor_sugerencias.visible = True
        if pila.page:
            pila.page.update()

    grid_lista = ft.GridView(
        controls = [],
        runs_count = 3,  # 3 columnas
        max_extent = 500,
        child_aspect_ratio = 3.00,  # Relación de aspecto (ancho/alto)
        spacing = 10,
        scroll = ft.ScrollMode.AUTO,
        width = 5000,
        height = 420
    )

    def cargar_venta_pendiente():
        # Carga una venta pendiente desde la variable global
        nonlocal lista_compra, venta_actual_id
        
        venta_id = globals.venta_pendiente_global
        globals.venta_pendiente_global = None

        # Obtener la función de SnackBar
        snackbar_func = globals.obtener_snackbar()
        
        if venta_id is None:
            print("No hay venta pendiente para cargar")
            return
        
        try:
            from dao.venta_dao import VentaDAO
            from dao.detalle_venta_dao import DetalleVentaDAO
            
            venta_dao = VentaDAO()
            venta = venta_dao.obtener_id_de_la_venta(venta_id)
            
            if venta is None:
                print(f"No se encontró la venta con ID: {venta_id}")
                return

            venta_actual_id = venta_id

            # OBTENER DETALLES DE LA VENTA (incluye cantidades)
            detalle_dao = DetalleVentaDAO()
            detalles = detalle_dao.obtener_por_venta(venta_id)
            
            if not detalles:
                print("La venta no tiene detalles asociados")
                return

            # Limpiar la lista actual
            lista_compra = []
            
            # Cargar los artículos con sus cantidades
            articulo_dao = ArticuloDAO()
            for detalle in detalles:
                articulo = articulo_dao.obtener_id_del_articulo_punto_v(detalle.detalle_articulo_id)
                if articulo:
                    item = Articulo(
                        articulo_id=articulo.articulo_id,
                        articulo_articulo=articulo.articulo_articulo,
                        articulo_codigo=articulo.articulo_codigo,
                        articulo_categoria=articulo.articulo_categoria,
                        articulo_imagen=articulo.articulo_imagen,
                        articulo_precio=articulo.articulo_precio,
                        articulo_stock=articulo.articulo_stock,
                        articulo_proveedor=articulo.articulo_proveedor,
                        articulo_vendidos=articulo.articulo_vendidos,
                    )
                    item.cantidad = detalle.detalle_cantidad  # Usar la cantidad del detalle
                    lista_compra.append(item)
                    print(f"Artículo cargado: {articulo.articulo_articulo} x{detalle.detalle_cantidad}")
            
            # ===== MOSTRAR SNACKBAR DE ÉXITO =====
            if snackbar_func:
                snackbar_func(f"Venta '{venta.venta_venta}' cargada exitosamente", "exito")
            
            # ===== AGREGAR NOTIFICACIÓN AL SISTEMA =====
            globals.agregar_notificacion(
                titulo=f"Venta '{venta.venta_venta}'",
                mensaje="cargada exitosamente",
                tipo="exito"
            )

            # Actualizar el contador de notificaciones
            try:
                if pila and hasattr(pila, 'actualizar_contador'):
                    pila.actualizar_contador()
            except:
                pass

            # Actualizar la interfaz
            actualizar_lista_compra()
            actualizar_resumen()
            print(f"Venta pendiente cargada: {len(lista_compra)} artículos")
            
        except Exception as error:
            print(f"Error al cargar la venta pendiente: {error}")
            import traceback
            traceback.print_exc()

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

            # Limpiar el ID de la venta actual después de cerrar
            venta_actual_id = None  # LIMPIAR

            # Volver a cargar la lista de los productos/articulos
            cargar_articulos()

            # Volver a rectificar
            cargar_venta_pendiente()

            # Actualizar la interfaz
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()

    def abrir_formulario_confirmar_modal(evento):
        # Crear y mostrar el modal con el formulario de "Pago"
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal, lista_compra, venta_actual_id

        if not lista_compra:
            print("Lista de compra vacía")
            grid_lista.controls.append(
                ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.Icon(ft.Icons.WARNING, size=26, color="#efb034"),
                            ft.Text("No se puede confirmar una lista de compras vacia", size = 20, color = "#efb034"),
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        spacing = 10,
                    )
                )
            )
            grid_lista.max_extent = 1500

            # Actualizar la interfaz
            if pila.page:
                pila.update()
            elif pagina_referencia:
                pagina_referencia.update()

            return

        # Guardar referencia a la página
        if evento and evento.page:
            pagina_referencia = evento.page

        if capa_oscura_abierta_modal:
            return
        
        # === CALCULAR TOTAL Y OBTENER IDs DE ARTÍCULOS ===
        total = sum(item.articulo_precio * item.cantidad for item in lista_compra)
        articulos_ids = [item.articulo_id for item in lista_compra]
        articulos_cantidades = [item.cantidad for item in lista_compra]
        
        usuario_actual = globals.obtener_sesion()
    
        if usuario_actual is not None:
            usuario_id = usuario_actual.usuario_id  # Obtener el ID del usuario
            nombre_usuario = usuario_actual.usuario_usuario  # Opcional: también puedes obtener el nombre
            print(f"Usuario actual: {nombre_usuario} (ID: {usuario_id})")
        else:
            # Si no hay sesión, usar un valor por defecto o manejar el error
            usuario_id = 1  # ID por defecto (temporal)
            print("No hay usuario autenticado, usando ID por defecto")

        def limpiar_despues_de_confirmar():
            # Limpiar la lista de compra despues de confirmar la venta
            nonlocal lista_compra
            lista_compra = []
            actualizar_lista_compra()
            actualizar_resumen()
            print("Lista de compra limpiada")
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = confirmar_form(
            formulario_visible = True,
            cerrando_modal = cerrar_modal,
            total = total,
            lista_articulos = articulos_ids,
            lista_cantidades = articulos_cantidades,
            usuario_id = usuario_id,
            limpiar_lista = limpiar_despues_de_confirmar,
            venta_id_actual = venta_actual_id, # PASAR EL VALOR DEL ID
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
        pila.controls.append(capa_oscura)
        capa_oscura_modal = capa_oscura
        capa_oscura_abierta_modal = True

        # Regresar a la normalida el tamaño maximo de las tarjetas de productos
        grid_lista.max_extent = 500

        # Actualizar la interfaz
        if pila.page:
            pila.update()
        elif pagina_referencia:
            pagina_referencia.update()

    def abrir_formulario_guardar_modal(evento):
        # Crear y mostrar el modal con el formulario de "Guardar venta"
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal, lista_compra

        # Guardar la compra (y limpia la lista de productos/articulos)
        if not lista_compra:
            print("Lista de compra vacía")
            grid_lista.controls.append(
                ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.Icon(ft.Icons.WARNING, size=26, color="#efb034"),
                            ft.Text("No se puede guardar una lista de compras vacia", size = 20, color = "#efb034"),
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        spacing = 10,
                    )
                )
            )
            grid_lista.max_extent = 1500

            # Actualizar la interfaz
            if pila.page:
                pila.update()
            elif pagina_referencia:
                pagina_referencia.update()

            return
        

        # Guardar referencia a la página
        if evento and evento.page:
            pagina_referencia = evento.page

        if capa_oscura_abierta_modal:
            return
        
        # === CALCULAR TOTAL Y OBTENER IDs DE ARTÍCULOS ===
        total = sum(item.articulo_precio * item.cantidad for item in lista_compra)
        articulos_ids = [item.articulo_id for item in lista_compra]
        articulos_cantidades = [item.cantidad for item in lista_compra]
        
        # === USUARIO (por ahora fijo, luego con login) ===
        usuario_id = 1  # Temporal, luego se obtendrá del login

        def limpiar_despues_de_confirmar():
            # Limpiar la lista de compra despues de confirmar la venta
            nonlocal lista_compra
            lista_compra = []
            actualizar_lista_compra()
            actualizar_resumen()
            print("Lista de compra limpiada")
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = guardar_form(
            formulario_visible = True,
            cerrando_modal = cerrar_modal,
            total = total,
            lista_articulos = articulos_ids,
            lista_cantidades = articulos_cantidades,
            usuario_id = usuario_id,
            limpiar_lista = limpiar_despues_de_confirmar,
            venta_id_actual = venta_actual_id, # PASAR EL VALOR DEL ID
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
        pila.controls.append(capa_oscura)
        capa_oscura_modal = capa_oscura
        capa_oscura_abierta_modal = True

        # Regresar a la normalida el tamaño maximo de las tarjetas de productos
        grid_lista.max_extent = 500

        # Actualizar la interfaz
        if pila.page:
            pila.update()
        elif pagina_referencia:
            pagina_referencia.update()

    def abrir_alerta_cancelar_venta(evento):
        # Crear y muestrar el modal con la alerta de "La Vinata dice: ¿Desea cancelar la venta?"
        # evento: El evento del clic en el boton "Cancelar"

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal, lista_compra

        if not lista_compra:
            print("Lista de compra vacía")
            return

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return

        def limpiar_despues_de_confirmar():
            # Limpiar la lista de compra despues de confirmar la venta
            nonlocal lista_compra
            lista_compra = []
            actualizar_lista_compra()
            actualizar_resumen()
            print("Lista de compra limpiada")

        venta_id_actual = venta_actual_id, # PASAR EL VALOR DEL ID

        if venta_id_actual is None:
            # --------------- Crear el contenido del modal -----------------
            contenido_modal = alerta_cancelar(
                formulario_visible = True, # Activar el modal, mostrando el formulario
                cerrando_modal = cerrar_modal,
                limpiar_lista = limpiar_despues_de_confirmar,
            )
        else:
            # Preparar los datos para la alerta
            id_y_nombre = {
                'id': venta_id_actual,
                'nombre': "Nombre_reyeno"
            }
            # --------------- Crear el contenido del modal -----------------
            contenido_modal = alerta_cancelar_2(
                formulario_visible = True, # Activar el modal, mostrando el formulario
                cerrando_modal = cerrar_modal,
                registro = id_y_nombre, # Enviar los datos a la alerta
                limpiar_lista = limpiar_despues_de_confirmar
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

    # ----------------- Funciones de selección ---------------
    def seleccionar_producto(articulo, tipo):
        # Selecciona un producto y actualiza la interfaz
        nonlocal producto_seleccionado, sugerencias_visibles
        
        producto_seleccionado = articulo
        print(f"Producto seleccionado: {articulo.articulo_articulo}")
        
        if tipo == "codigo":
            campo_codigo.value = articulo.articulo_codigo
            campo_nombre.value = articulo.articulo_articulo
        else:
            campo_nombre.value = articulo.articulo_articulo
            campo_codigo.value = articulo.articulo_codigo

        # Acutalizar imagen
        imagen_producto.src = f"assets/imagenes/imagenes_DB/{articulo.articulo_imagen}"
        imagen_producto.visible = True

        # Actualizar existencias
        texto_existencias.value = f"Existencias: {articulo.articulo_stock}"
        texto_existencias.color = "#926600"

        # Habilitar boton de agregar
        boton_agregar.disabled = False
        boton_agregar.bgcolor = "#6b1d41"

        # Resetear cantidad a 1
        cantidad_input.value = "1"
        actualizar_estado_botones()

        # Ocultar sugerencias
        contenedor_sugerencias.visible = False
        sugerencias_visibles = False
        
        if pila.page:
            pila.page.update()

    def ocultar_sugerencias(e):
        # Oculta las sugerencias al perder el foco
        nonlocal sugerencias_visibles
        import time
        time.sleep(0.2)
        contenedor_sugerencias.visible = False
        sugerencias_visibles = False
        if pila.page:
            pila.page.update()

    def actualizar_estado_botones():
        # Actualiza el estado de ambos botones (incremento y decremento)
        valor = obtener_cantidad_valor()
        stock = producto_seleccionado.articulo_stock if producto_seleccionado else 0

        # Actualizar botón de decremento (activo si valor > 1)
        if valor > 1:
            boton_decremento.content = ft.IconButton(
                # Botón de resta (icono flecha abajo)
                icon=ft.Icons.ARROW_DROP_DOWN,

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
            # Botón de resta (icono flecha abajo)
            boton_decremento.content = ft.IconButton(
                icon=ft.Icons.ARROW_DROP_DOWN,

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

        # Activo si valor < stock (y stock > 0)
        if producto_seleccionado and valor < stock:
            boton_incremento.content = ft.IconButton(
                icon=ft.Icons.ARROW_DROP_UP,
                icon_size=20,
                scale=1.0,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5),
                    padding=ft.Padding.symmetric(horizontal=5, vertical=2),
                ),
                bgcolor="#6b1d41",
                icon_color="#ffffff",
                tooltip="Incrementar",
                width=30,
                height=20,
                on_click=incremento_click
            )
        else:
            boton_incremento.content = ft.IconButton(
                icon=ft.Icons.ARROW_DROP_UP,
                icon_size=20,
                scale=1.0,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5),
                    padding=ft.Padding.symmetric(horizontal=5, vertical=2),
                ),
                bgcolor="#696768",
                icon_color="#ffffff",
                tooltip="Stock máximo alcanzado" if producto_seleccionado else "Selecciona un producto",
                width=30,
                height=20,
            )

        if pila.page:
            pila.page.update()

    def reiniciar_valor(e):
        if not e.control.value or not e.control.value.lstrip('-').isdigit():
            e.control.value = "1"
            actualizar_estado_botones()
            if pila.page:
                pila.page.update()
            return

        try:
            valor = int(e.control.value)
            stock = producto_seleccionado.articulo_stock if producto_seleccionado else 0

            if valor < 1:
                e.control.value = "1"
            elif producto_seleccionado and valor > stock:
                e.control.value = str(stock)
                texto_existencias.value = f"Máximo: {stock}"
                texto_existencias.color = "#de3b40"
            else:
                texto_existencias.value = f"Existencias: {stock}"
                texto_existencias.color = "#926600"

            actualizar_estado_botones()
            if pila.page:
                pila.page.update()
        except ValueError:
            e.control.value = "1"
            actualizar_estado_botones()
            if pila.page:
                pila.page.update()

    def obtener_cantidad_valor():
        try:
            if not cantidad_input.value or cantidad_input.value.strip() == "":
                return 1
            return int(cantidad_input.value)
        except ValueError:
            return 1

    def decremento_click(e):
        valor = obtener_cantidad_valor()
        if valor > 1:
            # Convertir a entero, sumar 1 y convertir de nuevo a string
            cantidad_input.value = str(valor - 1)
            # Actualizar la interfaz para actualizar el estado de los botones
            actualizar_estado_botones()

            if pila.page:
                pila.page.update()

    def incremento_click(e):
        valor = obtener_cantidad_valor()
        stock = producto_seleccionado.articulo_stock if producto_seleccionado else 0

        if producto_seleccionado and valor < stock:
            # Convertir a entero, sumar 1 y convertir de nuevo a string
            cantidad_input.value = str(valor + 1)
            texto_existencias.value = f"Existencias: {stock}"
            texto_existencias.color = "#926600"
            # Actualizar la interfaz para actualizar el estado de los botones
            actualizar_estado_botones()

            if pila.page:
                pila.page.update()
    
    titulo = ft.Text(
        "Punto de Venta",
        size = 28,
        weight = ft.FontWeight.BOLD,
        color = "#6b1d41",
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

        suffix_icon = ft.Icons.SEARCH
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

        suffix_icon = ft.Icons.SEARCH
    )
    
    contenedor_sugerencias = ft.Container(
        content = ft.Column(
            controls = [],
            spacing = 0,
        ),
        bgcolor = "#f9f6f0",
        border = ft.Border.all(1, "#e2dcd5"),
        border_radius = 10,
        shadow = ft.BoxShadow(
            spread_radius = 1,
            blur_radius = 5,
            color = ft.Colors.BLACK26,
        ),
        visible = False,
        margin = ft.Margin.only(top = 5),
        width = 380
    )
    
    imagen_producto = ft.Image(
        src = f"assets/imagenes/botella_negra_default_Punto_de_Venta.jpg",
        expand = True,
    )


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

    def agregar_a_lista(e):
        # Agrega el producto seleccionado a la lista de compra
        nonlocal lista_compra

        if not producto_seleccionado:
            print("No hay producto seleccionado")
            return

        cantidad = obtener_cantidad_valor()

        # Validar que no exceda el stock
        if cantidad > producto_seleccionado.articulo_stock:
            texto_existencias.value = f"Existencias: {producto_seleccionado.articulo_stock}"
            texto_existencias.color = "#de3b40"
            pila.page.update()
            return

        # Verificar si ya existe en la lista
        existente = next((p for p in lista_compra if p.articulo_id == producto_seleccionado.articulo_id), None)

        if existente:
            boton_agregar.disabled = True
            boton_agregar.bgcolor = "#696768"

            pila.page.update()
            return
        else:
            # Crear nuevo item
            item = Articulo(
                articulo_id = producto_seleccionado.articulo_id,
                articulo_articulo = producto_seleccionado.articulo_articulo,
                articulo_codigo = producto_seleccionado.articulo_codigo,
                articulo_categoria = producto_seleccionado.articulo_categoria,
                articulo_imagen = producto_seleccionado.articulo_imagen,
                articulo_precio = producto_seleccionado.articulo_precio,
                articulo_stock = producto_seleccionado.articulo_stock,
                articulo_proveedor = producto_seleccionado.articulo_proveedor,
                articulo_vendidos = producto_seleccionado.articulo_vendidos,
            )
            item.cantidad = cantidad
            lista_compra.append(item)

        print(f"Agregado: {item.articulo_articulo} x{cantidad}")

        # Limpiar selección
        limpiar_seleccion()
        actualizar_lista_compra()
        actualizar_resumen()

    def limpiar_seleccion():
        # Limpia la selección actual
        nonlocal producto_seleccionado
        producto_seleccionado = None
        imagen_producto.src = f"assets/imagenes/botella_negra_default_Punto_de_Venta.jpg"
        texto_existencias.value = "Existencias: ---"
        texto_existencias.color = "#9095a0"

        boton_agregar.disabled = True
        boton_agregar.bgcolor = "#696768"

        campo_codigo.value = ""
        campo_nombre.value = ""
        cantidad_input.value = "1"
        actualizar_estado_botones()
        pila.page.update()

    def actualizar_lista_compra():
        # Muestra los productos en la lista de compra
        grid_lista.controls.clear()

        if not lista_compra:
            grid_lista.controls.append(
                ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.Icon(ft.Icons.CANCEL, size=26, color="#9095a0"),
                            ft.Text("No hay productos en la lista", size = 20, color = "#9095a0"),
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        spacing = 10,
                    )
                )
            )
            grid_lista.max_extent = 1500
            pila.page.update()
            return
            

        for item in lista_compra:
            tarjeta = crear_tarjeta_lista(item)
            grid_lista.controls.append(tarjeta)

        grid_lista.max_extent = 500
        pila.page.update()

    def crear_tarjeta_lista(item):
        # Crea una tarjeta para un producto en la lista de compra

        def cambiar_cantidad(delta):
            if 1 <= item.cantidad + delta <= item.articulo_stock:
                item.cantidad += delta
                actualizar_lista_compra()
                actualizar_resumen()

        def eliminar_de_lista(e):
            nonlocal lista_compra
            lista_compra = [p for p in lista_compra if p.articulo_id != item.articulo_id]
            actualizar_lista_compra()
            actualizar_resumen()

        imagen_rotada = ft.Container(
            content=ft.Image(src=f"imagenes/imagenes_DB/{item.articulo_imagen}", width=110, height=110),
            bgcolor="#000000",
            border_radius = 5
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    imagen_rotada,
                    
                    ft.Column(
                        controls = [
                            ft.Text(item.articulo_articulo, size = 18, weight = ft.FontWeight.BOLD, color = "#6b1d41"),

                            ft.Row(
                                controls = [
                                    ft.Text(item.articulo_categoria, size = 12, color = "#9095a0"),

                                    ft.Container(content = ft.Text(""), height = 20, width = 1, bgcolor = "#e2dcd5"),

                                    ft.Text(item.articulo_proveedor, size = 12, color = "#9095a0")
                                ]
                            ),

                            ft.Row(
                                controls = [
                                    ft.IconButton(
                                        icon = ft.Icon(
                                            ft.Icons.REMOVE, # Icono de -
                                            color = "#6b1d41"
                                        ),
                                        icon_size = 16,
                                        on_click = lambda e: cambiar_cantidad(-1),
                                        disabled = item.cantidad <= 1,
                                    ),

                                    ft.Text(str(item.cantidad), size = 16, weight = ft.FontWeight.BOLD, color = "#424955", width = 30, text_align = ft.TextAlign.CENTER),

                                    ft.IconButton(
                                        icon = ft.Icon(
                                            ft.Icons.ADD, # Icono de +
                                            color = "#6b1d41"
                                        ),
                                        icon_size = 16,
                                        on_click = lambda e: cambiar_cantidad(1),
                                        disabled = item.cantidad >= item.articulo_stock,
                                    )
                                ]
                            )
                        ],
                        spacing=2,
                    ),

                    ft.Column(
                        controls = [
                            ft.OutlinedButton(
                                "",
                                icon = ft.Icon(
                                    ft.Icons.DELETE, # Nombre del icono (ej. FAVORITE)
                                    size=25, # Tamaño en píxeles
                                ),
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
                                    padding = ft.Padding.symmetric(horizontal = 8, vertical = 8)
                                ),
                                width = 40,
                                height = 40,
                                margin = ft.Margin.only(left = 50, bottom = 15),
                                on_click = eliminar_de_lista, 
                                tooltip = "Eliminar"
                            ),

                            ft.Text(
                                f"${item.articulo_precio * item.cantidad:.2f}",
                                size = 14,
                                weight = ft.FontWeight.BOLD, 
                                color = "#c9a03d", 
                                width = 80, 
                                text_align = ft.TextAlign.END
                            )
                        ],
                        alignment = ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor = "#ffffff",
            border = ft.Border.all(1, "#e2dcd5"),
            border_radius = 10,
            padding = ft.Padding.symmetric(horizontal = 10, vertical = 10),
            margin = ft.Margin.only(bottom = 5),
        )

    def actualizar_resumen():
        # Actualiza el resumen de la compra
        total_precio = sum(item.articulo_precio * item.cantidad for item in lista_compra)

        texto_total_precio.value = f"Total | ${total_precio:.2f}"
        pila.page.update()

    def limpiar_lista(e):
        # Limpia toda la lista de compra
        nonlocal lista_compra
        lista_compra = []
        actualizar_lista_compra()
        actualizar_resumen()
        grid_lista.controls = []

    # === FUNCIONES DE ACCIONES ===
    def confirmar_compra(e):
        # Confirma la compra (y limpia la lista de productos/articulos)
        if not lista_compra:
            print("Lista de compra vacía")
            return

        # Abrir el modal pago
        abrir_formulario_confirmar_modal(e)

    def guardar_compra(e):
        # Confirma la compra (y limpia la lista de productos/articulos)
        if not lista_compra:
            print("Lista de compra vacía")
            return

        print("Guardando compra...")
        for item in lista_compra:
            print(f"   - {item.articulo_articulo} x{item.cantidad} = ${item.articulo_precio * item.cantidad:.2f}")
        print(f"   Total: ${sum(item.articulo_precio * item.cantidad for item in lista_compra):.2f}")

        # Abrir el modal guardar
        abrir_formulario_guardar_modal(e)

    # Botones de incremento y decremento
    boton_decremento = ft.Container()
    boton_incremento = ft.Container()

    # ===== CARGAR DATOS INICIALES ====
    cargar_articulos()

    # ===== VERIFICAR SI HAY UNA VENTA PENDIENTE =====
    cargar_venta_pendiente()


    texto_existencias = ft.Text(
        "Existencias: ---",
        size = 14,
        color = "#9095a0",
        weight = ft.FontWeight.W_500,
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

        bgcolor = "#696768",  # Color de fondo
        style = ft.ButtonStyle(
            color = "#ffffff",
            shape = ft.RoundedRectangleBorder(radius = 10)
        ),
        height = 40,
        disabled = True,
        on_click = agregar_a_lista,
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
                            # Botón de suma (dinamico)
                            boton_incremento,

                            # Botón de resta (dinamico)
                            boton_decremento
                        ],
                        spacing = 6
                    ),
                ],
                margin = ft.Margin.only(bottom = 5)
            ),

            contenedor_existencias
        ],
    )

    # Formulario de "Agregar"
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

    # === LISTA DE COMPRA ===
    titulo_lista = ft.Text(
        "Productos",
        size = 24,
        weight = ft.FontWeight.BOLD,
        color = "#6b1d41",
    )

    

    texto_total_precio = ft.Text(
        "Total | $0.00",
        size = 28,
        weight = ft.FontWeight.BOLD,
        color = "#c9a03d",
    )
    

    # === BARRA DE ACCIONES INFERIOR ===
    barra_acciones = ft.Container(
        content = ft.Row(
            controls = [
                ft.ElevatedButton(
                    "Guardar",
                    icon = ft.Icons.SAVE,

                    style = ft.ButtonStyle(
                        # Borde sólido vino-caramelo de 2 píxeles por defecto
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
                        padding = 20,
                        shape = ft.RoundedRectangleBorder(radius = 10)
                    ),
                    bgcolor = "#c9a03d",
                    color = "#ffffff",
                    width = 130,
                    on_click = abrir_formulario_guardar_modal,
                ),

                texto_total_precio,

                ft.Row(
                    controls = [
                        ft.ElevatedButton(
                            "Confirmar",
                            icon = ft.Icons.CHECK,
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
                            on_click = abrir_formulario_confirmar_modal,
                        ),
                        ft.ElevatedButton(
                            "Cancelar",
                            icon = ft.Icons.CLOSE,
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
                                padding = 20,
                            ),
                            on_click = abrir_alerta_cancelar_venta,
                        ),
                    ]
                )
                
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing = 20,
        ),
        padding = ft.Padding.symmetric(vertical = 15, horizontal = 20),
        bgcolor = "#ffffff",
        border = ft.Border.all(1, "#e2dcd5"),
        border_radius = 10,
    )

    # ----------------- Contenido principal -------------------
    contenido_principal = ft.Container(
        padding = 20,
        content = ft.Column(
            controls = [
                titulo,
                formulario,

                ft.Container(
                    content = (
                        ft.Column(
                            controls = [
                                ft.Row(
                                    controls = [
                                        titulo_lista
                                    ],
                                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                                    margin = ft.Margin.only(left = 15, right = 15, top = 15, bottom = 5)
                                ),

                                ft.Divider(thickness = 20, color = "#f0eee9"),

                                ft.Column(
                                    controls = [
                                        grid_lista
                                    ],
                                    margin = ft.Margin.only(left = 15, right = 15, top = 5, bottom = 15)
                                )
                                
                            ]
                        )
                    ),
                    border = ft.Border.all(1, "#e2dcd5"),
                    border_radius = 10,
                    padding = 0,
                    bgcolor = "#ffffff",
                    expand = True,
                    height = 300,
                ),
                
                barra_acciones,
            ],
            spacing = 10,
            expand = True,
        ),
        expand = True,
    )

    # Agrega a la pila
    pila.controls.append(contenido_principal)

    def inicializar_botones():
        # Se ejecuta cuando el Stack se agrega a la página
        actualizar_estado_botones()
        cargar_articulos()
        cargar_venta_pendiente()

    pila.on_mount = inicializar_botones

    return pila