import flet as ft

from models.venta import Venta
from dao.venta_dao import VentaDAO

from globals import venta_pendiente_global  # importar venta global

# from ui.proveedor_acciones.proveedor_alert_delete import alerta_eliminar
from ui.venta_acciones.venta_form_edit import venta_form_edit
from ui.venta_acciones.venta_alert_cancel_2 import alerta_cancelar_2

def ventas_list(regresar):
    # ---------------- Variables de estado -------------------
    capa_oscura_abierta_modal = False # Indica si el modal esta visible/activo
    capa_oscura_modal = None # Es el contenido con backgroud oscuro semitransparente (capa oscuara)
    pagina_referencia = None # Guardar la referencia a la pagina (contenido)
    
    todas_las_ventas = [] # Guardar todas las vetnas sin filtrar

    # -------------- Contenedor de capas ---------------------
    pila = ft.Stack(expand = True) # ft.Stack permite superponer widgets (elementos)
    # 'expand = True' hace que ocupe todo el espacio disponible
    
    # --------------- Tabla de ventas ---------------------
    # Tabla de ventas
    tabla = ft.DataTable(
        divider_thickness = 0,
        horizontal_lines = ft.BorderSide(1, "#e2dcd5"),
        columns = [
            ft.DataColumn(ft.Text("Nombre de la venta", color = "#926600", weight = ft.FontWeight.BOLD)), # Columna 1
            ft.DataColumn(ft.Text("Fecha", color = "#926600", weight = ft.FontWeight.BOLD)), # Columna 2
            ft.DataColumn(ft.Text("Ganancia", color = "#926600", weight = ft.FontWeight.BOLD)), # Columna 3
            ft.DataColumn(ft.Text("Empleado", color = "#926600", weight = ft.FontWeight.BOLD)), # Columna 4
            ft.DataColumn(ft.Text("Estado", color = "#926600", weight = ft.FontWeight.BOLD)), # Columna 5
            ft.DataColumn(ft.Text("Acciones", color = "#926600",text_align = ft.TextAlign.CENTER, weight = ft.FontWeight.BOLD, width = 170)) # Columna 5
        ],
        expand = True,
        rows = []
    )

    mensaje = ft.Text()


    # Función/meotod para crear botones segun el estado
    def crear_botones_para_venta(venta):
        # Determina los botones de accion que se mostraran al lado de los registros, dependiendo si el estado es "Concluido" o "Pendiente"
        valor = venta.venta_estado

        # Definir los botones para una venta en estado = "Pendiente"
        if valor == "Pendiente":
            boton_primario = ft.OutlinedButton( # Boton Continuar

                #f"Continuar ID:{venta.venta_id}",}
                "Continuar",
                data = venta.venta_id,

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
                    shape = ft.RoundedRectangleBorder(radius = 10),
                    padding = ft.Padding.symmetric(horizontal = 0, vertical = 8)
                ),
                width = 90,

                on_click = continuar_venta # Al hacer clic, sobre el boton de "Continuar" se abrira el modal
            )

            boton_secundario = ft.OutlinedButton( # Boton Cancelar

                #f"Cancelar ID:{venta.venta_id}",
                "Cancelar",
                data = venta.venta_id,

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
                    shape = ft.RoundedRectangleBorder(radius = 10),
                    padding = ft.Padding.symmetric(horizontal = 0, vertical = 8)
                ),
                width = 90,

                on_click = abrir_alerta_cancelar_venta # Al hacer clic, sobre el boton de "Cancelar" se abrira el modal
            )

        # Definir los botones para una venta en estado = "Concluida"
        elif valor == "Concluida":
            # Botón de resta (icono flecha abajo)
            boton_primario = ft.OutlinedButton( # Boton Ver

                #f"Ver ID:{venta.venta_id}",}
                "Ver",
                data = venta.venta_id,

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
                    shape = ft.RoundedRectangleBorder(radius = 10),
                    padding = ft.Padding.symmetric(horizontal = 0, vertical = 8)
                ),
                width = 90,

                on_click = ver_detalles_venta # Al hacer clic, sobre el boton de "Ver" se abrira el modal
            )

            boton_secundario = ft.OutlinedButton( # Boton Editar

                #f"Editar ID:{venta.venta_id}",
                "Editar",
                data = venta.venta_id,

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
                    shape = ft.RoundedRectangleBorder(radius = 10),
                    padding = ft.Padding.symmetric(horizontal = 0, vertical = 8)
                ),
                width = 90,

                on_click = abrir_formulario_editar_venta # Al hacer clic, sobre el boton de "Editar" se abrira el modal
            )
        else:
            # Estado desconocido
            boton_primario = ft.Text("Sin acción", color = "9095a0")
            boton_secundario = ft.Text("", color = "9095a0")

        return boton_primario, boton_secundario
    

    def continuar_venta(evento):
        # Continúa una venta "Pendiente" (redirige a punto_de_venta.py)
        
        venta_id = evento.control.data if evento.control else None

        if venta_id is None:
            print("No se pudo obtener el ID de la venta")
            return

        print(f"Continuando venta ID: {venta_id}")
        
        # === ASIGNAR A LA VARIABLE GLOBAL ===
        # Asignar a la variable global del módulo globals
        import globals
        globals.venta_pendiente_global = venta_id

        venta_pendiente_global = venta_id
        print(f"Venta ID {venta_pendiente_global} guardada en variable global")
        
        # Redirigir a punto_de_venta
        if regresar:
            regresar()  # Esto ejecuta mostrar_inicio que carga punto_de_venta
        else:
            print("No se pudo redirigir a punto_de_venta")


    def abrir_alerta_cancelar_venta(evento):
        # Crear y muestrar el modal con la alerta de "La Vinata dice: ¿Desea cancelar esta venta?"
        # evento: El evento del click en el boton "Cancelar"

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # ======== Obtener el ID de la venta desde el boton =========
        # El ID se guarda en la propiedad 'data' del boton
        venta_id = evento.control.data if evento.control else None # Obtener el venta_id del boton

        if venta_id is None:
            print("No se pudo obtener el ID de la venta")
            return
        
        try:
            # === Obtener los datos de la venta desde la BD ===
            venta_dao = VentaDAO()
            venta = venta_dao.obtener_id_de_la_venta(venta_id)

            if venta is None:
                print(f"No se encontro la venta con ID: {venta_id}")
                return
            
            # Preparar los datos para la alerta
            id_y_nombre = {
                'id': venta.venta_id,
                'nombre': venta.venta_venta
            }

            print(f"Datos cargados: {id_y_nombre}")

        except Exception as error:
            print(f"Error al obtener la información de la venta: {error}")
            return
        # ======= FIN Obtener el ID de la venta desde el boton ========
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = alerta_cancelar_2(
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

    def ver_detalles_venta(evento):
        # Muestra los detalles de una venta concluida
        venta_id = evento.control.data if evento.control else None

        if venta_id is None:
            print("No se pudo obtener el ID de la venta")
            return

        pila.page.update()

    def abrir_formulario_editar_venta(evento):
        # Crear y mostrar el modal con el formulario de "Editar venta"
        # evento: El evento del clic en el boton "Editar" del registro correspondiente

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # ======== Obtener el ID de la venta desde el boton =========
        # El ID se guarda en la propiedad 'data' del boton
        venta_id = evento.control.data if evento.control else None # Obtener el venta_id del boton

        if venta_id is None:
            print("No se pudo obtener el ID de la venta (editar)")
            return
        
        try:
            # === Obtener los datos de la venta desde la BD ===
            venta_dao = VentaDAO()
            venta = venta_dao.obtener_id_de_la_venta(venta_id)

            if venta is None:
                print(f"No se encontro la venta con ID: {venta_id}")
                return

            nombre_completo = venta.venta_venta

            # Eliminar 'VEN-' al inicio y '-VINATA' al final
            nombre_limpio = nombre_completo.replace("VEN-", "").replace("-VINATA", "")

            # Preparar los datos para el formulario
            registro = {
                'id': venta.venta_id,
                'nombre': nombre_limpio,
                'usuario_id': venta.venta_usuario
            }

            print(f"Datos cargados: {registro}")

        except Exception as error:
            print(f"Error al obtener la venta: {error}")
            return
        # ======= FIN Obtener el ID de la venta desde el boton ========
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = venta_form_edit(
            formulario_visible = True, # Activar el modal, mostrando el formulario
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

    def mostrar_ventas_en_tabla(ventas):
        # Muestra una lista de ventas en la tabla
        tabla.rows.clear()

        for venta in ventas:
            # Crear botones  segun el estado
            boton_primario, boton_secundario = crear_botones_para_venta(venta)

            bgcolor_estado = "#066945" if venta.venta_estado == "Concluida" else "#efb034"

            tabla.rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(
                            ft.Text(
                                venta.venta_venta, 
                                color = "#0d1b2a", 
                                weight = ft.FontWeight.BOLD,
                                overflow = ft.TextOverflow.ELLIPSIS,  # Agrega "..." al final
                                width = 250,  # Ancho aproximado para 20 caracteres
                            )
                        ),
                        ft.DataCell(ft.Text(str(venta.venta_fecha), color = "#0d1b2a")),
                        ft.DataCell(ft.Text(f"${venta.venta_ganancia:.2f}", color = "#6b1d41", weight = ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(venta.venta_usuario, color = "#0d1b2a", width = 150)),
                        ft.DataCell(
                            ft.Container(
                                content = ft.Text(
                                    venta.venta_estado, 
                                    color = "#ffffff",
                                    weight = ft.FontWeight.BOLD
                                ),
                                bgcolor = bgcolor_estado,
                                padding = ft.Padding.symmetric(horizontal = 10, vertical = 5),
                                border_radius = 10
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                controls = [
                                    # Boton primario (Continuar/Ver)
                                    boton_primario,

                                    # Boton secundario (Cancelar/Editar)
                                    boton_secundario,
                                ],
                                spacing = 4
                            )
                        )
                    ]
                )
            )
        
        # Actualizar la interfaz
        if pila.page:
            pila.update()
        elif pagina_referencia:
            pagina_referencia.update()

    # -----------------Función para cargar las ventas----------------------
    def cargar_ventas():
        # Cargar todas las ventas de la base de datos
        nonlocal todas_las_ventas

        try:
            venta_dao = VentaDAO()
            ventas = venta_dao.obtener_todos()

            # Guardar todas las ventas
            todas_las_ventas = ventas

            # Mostrar todas las ventas
            mostrar_ventas_en_tabla(ventas)
            

        except Exception as error:
            print(f"Error al consultar las ventas: {error}")
            
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()

        return ventas

    def buscar_ventas(e):
        # Filtrar las ventas en tiempo real mediante el campo de nombre

        texto_busqueda = busqueda_input.value.lower().strip() if busqueda_input.value else ""

        # Si el campo de busqueda esta vacio se mostraran todas las ventas (registros)
        if texto_busqueda == "":
            mostrar_ventas_en_tabla(todas_las_ventas)
            return
        
        # Filtrar ventas por nombre
        ventas_filtradas = [
            venta for venta in todas_las_ventas
            if texto_busqueda in venta.venta_venta.lower()
        ]

        # Mostrar las ventas filtradas
        mostrar_ventas_en_tabla(ventas_filtradas)

        # Mostrar mensaje si no hay resultados
        if not ventas_filtradas:
            print(f"No se encontraron ventas con '{texto_busqueda}'")
            if pila.page:
                pila.update()
            else:
                pagina_referencia.update()
        

    # ------------------- Función para cerrar la modal --------------------
    def cerrar_modal():
        # Cierra el modal, eliminando la capa oscura de la pila

        # 'nonlocal' permite modificar variables de la función padre (ventas_list)
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Varificar si el modal está abierto y la capa oscura exite en la pila
        if capa_oscura_abierta_modal and capa_oscura_modal in pila.controls:
            # Remover la capa uscura del Stack (la elimina visualemente)
            pila.controls.remove(capa_oscura_modal)

            # limpiar las capas
            capa_oscura_modal = None
            capa_oscura_abierta_modal = False

            # Volver a cargar la lista de las ventas
            cargar_ventas()

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
        hint_text = "Buscar mediante nombre de venta...",  # Esto es el placeholder
        label_style = estilo_de_label,
        on_focus = lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(), # Estilo del label en focus
        on_blur = lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(), # Estilo del label
        focused_border_color = "#c9a03d", # Borde al enfocar
        border_color = "#bcc1ca",
        color = "#424955",
        width = 400,
        height = 40,

        on_change = buscar_ventas, # Buscar en tiempo real

        # 'suffix_icon' Sirve para colocar un icono en el input despues del texto
        suffix_icon = ft.Icon(
            ft.Icons.SEARCH_OUTLINED, # Icono de $
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
                                    "Ventas",
                                    size = 24,
                                    weight = ft.FontWeight.BOLD,
                                    color = "#6b1d41"
                                ),

                                # Campo de busqueda
                                campo_de_busqueda,
                                
                                # Boton de exportar
                                ft.OutlinedButton(
                                    "Exportar",
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
                                                    
                                    icon = ft.Icons.FILE_DOWNLOAD,
                                    # on_click = abrir_formulario_registrar_modal # Al hacer clic, sobre el boton de "Registrar" se abrira el modal
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
                    ]
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

    # --------------- Agregar el contenido principal a la pila ----------------
    pila.controls.append(contenido_principal)

    # ---------------- Cargar datos iniciales (SIN actualizar) ------------------
    # Solo cargaran los datos, pero NO se hace update porque la pila aun no esta en la pagina. La actualización se hara cuando se agregue.
    try:
        ventas = cargar_ventas()

        tabla.rows.clear()
        for venta in ventas:
            # Crear botones  segun el estado
            boton_primario, boton_secundario = crear_botones_para_venta(venta)

            bgcolor_estado = "#066945" if venta.venta_estado == "Concluida" else "#efb034"

            tabla.rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(venta.venta_venta, color = "#0d1b2a", weight = ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(str(venta.venta_fecha), color = "#0d1b2a")),
                        ft.DataCell(ft.Text(f"${venta.venta_ganancia:.2f}", color = "#6b1d41", weight = ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(venta.venta_usuario, color = "#0d1b2a", width = 150)),
                        ft.DataCell(
                            ft.Container(
                                content = ft.Text(
                                    venta.venta_estado, 
                                    color = "#ffffff",
                                    weight = ft.FontWeight.BOLD
                                ),
                                bgcolor = bgcolor_estado,
                                padding = ft.Padding.symmetric(horizontal = 10, vertical = 5),
                                border_radius = 10
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                controls = [
                                    # Boton primario (Continuar/Ver)
                                    boton_primario,

                                    # Boton secundario (Cancelar/Editar)
                                    boton_secundario,
                                ],
                                spacing = 4
                            )
                        )
                    ]
                )
            )

    except Exception as error:
        print(f"Error al consultar las ventas: {error}")

    return pila