import flet as ft

from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO
from ui.usuario_acciones.usuario_form_create import usuario_form
from ui.usuario_acciones.usuario_form_edit import usuario_form_edit
from ui.usuario_acciones.usuario_alert_delete import alerta_eliminar

def usuarios_list(regresar):
    # ---------------- Variables de estado -------------------
    capa_oscura_abierta_modal = False # Indica si el modal esta visible/activo
    capa_oscura_modal = None # Es el contenido con backgroud oscuro semitransparente (capa oscuara)
    pagina_referencia = None # Guardar la referencia a la pagina (contenido)
    
    todos_los_usuarios = [] # Guardar todos los usuarios sin filtrar

    # -------------- Contenedor de capas ---------------------
    pila = ft.Stack(expand = True) # ft.Stack permite superponer widgets (elementos)
    # 'expand = True' hace que ocupe todo el espacio disponible
    
    # --------------- Tabla de usuarios ---------------------
    # Tabla de usuarios
    tabla = ft.DataTable(
        columns = [
            ft.DataColumn(ft.Text("Nombre", color = "#0d1b2a")), # Columna 1
            ft.DataColumn(ft.Text("Contraseña", color = "#0d1b2a")), # Columna 2
            ft.DataColumn(ft.Text("Número empleado", color = "#0d1b2a")), # Columna 3
            ft.DataColumn(ft.Text("Correo electrónico", color = "#0d1b2a")), # Columna 4
            ft.DataColumn(ft.Text("Privilegio", color = "#0d1b2a")), # Columna 5
            ft.DataColumn(ft.Text("Acciones", color = "#0d1b2a")) # Columna 6
        ],
        expand = True,
        rows = []
    )

    mensaje = ft.Text()

    def obtener_nombre_completo(usuario):
        # Concatenar el nombre completo de los usuarios
        return f"{usuario.usuario_usuario} {usuario.usuario_apaterno} {usuario.usuario_amaterno}".strip()

    def mostrar_usuarios_en_tabla(usuarios):
        # Muestra una lista de usuarios en la tabla
        tabla.rows.clear()

        for usuario in usuarios:
            usuario_nombre_completo = obtener_nombre_completo(usuario)

            tabla.rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(usuario_nombre_completo, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(usuario.usuario_contrasenia, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(usuario.usuario_nuempleado, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(usuario.usuario_correo, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(usuario.usuario_privilegio, color = "#0d1b2a")),
                        ft.DataCell(
                            ft.Row(
                                controls = [
                                    # Boton Editar
                                    ft.OutlinedButton(
                                        #f"Editar ID:{usuario.usuario_id}",}
                                        "Editar",
                                        data = usuario.usuario_id, # Recuperar el ID del registro/usuario

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
                                        #f"Eliminar ID:{usuario.usuario_id}",
                                        "Eliminar",
                                        data = usuario.usuario_id, # Recuperar el ID del registro/usuario

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

                                        on_click = abrir_alerta_eliminar_usuario # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                    )
                                ]
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

    # -----------------Función para cargar los usuarios----------------------
    def cargar_usuarios():
        # Cargar todos los usuarios de la base de datos
        nonlocal todos_los_usuarios

        try:
            usuario_dao = UsuarioDAO()
            usuarios = usuario_dao.obtener_todos()

            # Guardar todos los usuarios
            todos_los_usuarios = usuarios

            # Mostrar todos los usuarios
            mostrar_usuarios_en_tabla(usuarios)

        except Exception as error:
            print(f"Error al consultar los usuarios: {error}")
            
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()

        return usuarios

    def buscar_usuarios(e):
        # Filtrar los usuarios en tiempo real mediante el campo de nombre

        texto_busqueda = busqueda_input.value.lower().strip() if busqueda_input.value else ""

        # Si el campo de busqueda esta vacio se mostraran todos los usuarios (registros)
        if texto_busqueda == "":
            mostrar_usuarios_en_tabla(todos_los_usuarios)
            return
        
        # Filtrar usuarios por nombre
        usuarios_filtrados = [
            usuario for usuario in todos_los_usuarios
            if texto_busqueda in obtener_nombre_completo(usuario).lower()
        ]

        # Mostrar los usuarios filtrados
        mostrar_usuarios_en_tabla(usuarios_filtrados)

        # Mostrar mensaje si no hay resultados
        if not usuarios_filtrados:
            print(f"No se encontraron usuarios con '{texto_busqueda}'")
            if pila.page:
                pila.update()
            else:
                pagina_referencia.update()
        

    # ------------------- Función para cerrar la modal --------------------
    def cerrar_modal():
        # Cierra el modal, eliminando la capa oscura de la pila

        # 'nonlocal' permite modificar variables de la función padre (usuarios_list)
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Varificar si el modal está abierto y la capa oscura exite en la pila
        if capa_oscura_abierta_modal and capa_oscura_modal in pila.controls:
            # Remover la capa uscura del Stack (la elimina visualemente)
            pila.controls.remove(capa_oscura_modal)

            # limpiar las capas
            capa_oscura_modal = None
            capa_oscura_abierta_modal = False

            # Volver a cargar la lista de los usuarios
            cargar_usuarios()

            # Actualizar la interfaz
            if pila.page:
                pila.update() # Se actualiza la pila para mostrar cambios
            elif pagina_referencia:
                pagina_referencia.update()

    
    def abrir_formulario_registrar_modal(evento):
        # Crear y muestrar el modal con el formulario de Registrar usuario"
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
        contenido_modal = usuario_form(
            formulario_visible = True, # Activar el modal, mostrando el formulario
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

    def abrir_formulario_editar_modal(evento):
        # Crear y mostrar el modal con el formulario de "Editar usuario"
        # evento: El evento del clic en el boton "Editar" del registro correspondiente

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # ======== Obtener el ID del usuario desde el boton =========
        # El ID se guarda en la propiedad 'data' del boton
        usuario_id = evento.control.data if evento.control else None # Obtener el usuario_id del boton

        if usuario_id is None:
            print("No se pudo obtener el ID del usuario")
            return
        
        try:
            # === Obtener los datos del usuario desde la BD ===
            usuario_dao = UsuarioDAO()
            usuario = usuario_dao.obtener_id_del_usuario(usuario_id)

            if usuario is None:
                print(f"No se encontro el usuario con ID: {usuario_id}")
                return

            
            # Preparar los datos para el formulario
            registro = {
                'id': usuario.usuario_id,
                'nombre': usuario.usuario_usuario,
                'apellido_paterno': usuario.usuario_apaterno,
                'apellido_materno': usuario.usuario_amaterno,
                'contrasenia': usuario.usuario_contrasenia,
                'numero_empleado': usuario.usuario_nuempleado,
                'correo': usuario.usuario_correo,
                'privilegio_id': usuario.usuario_privilegio
            }

            print(f"Datos cargados: {registro}")

        except Exception as error:
            print(f"Error al obtener el usuario: {error}")
            return
        # ======= FIN Obtener el ID del usuario desde el boton ========
        
        # --------------- Crear el contenido del modal -----------------
        contenido_modal = usuario_form_edit(
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

    def abrir_alerta_eliminar_usuario(evento):
        # Crear y muestrar el modal con la alerta de "La Vinata dice: ¿Desea eliminar este usuario?"
        # evento: El evento del clic en el boton "Eliminar"

        # "nonlocal" para modificar variables de la función padre
        nonlocal capa_oscura_abierta_modal, capa_oscura_modal

        # Guardar referencia a la pagina desde el evento
        if evento and evento.page:
            pagina_referencia = evento.page

        # Si el modal ya esta abierto, no hacer nada
        if capa_oscura_abierta_modal:
            return
        
        # ======== Obtener el ID del usuario desde el boton =========
        # El ID se guarda en la propiedad 'data' del boton
        usuario_id = evento.control.data if evento.control else None # Obtener el usuario_id del boton

        if usuario_id is None:
            print("No se pudo obtener el ID del usuario")
            return
        
        try:
            # === Obtener los datos del usuario desde la BD ===
            usuario_dao = UsuarioDAO()
            usuario = usuario_dao.obtener_id_del_usuario(usuario_id)

            if usuario is None:
                print(f"No se encontro el usuario con ID: {usuario_id}")
                return
            
            # Preparar los datos para el formulario
            id_y_nombre = {
                'id': usuario.usuario_id,
                'nombre': usuario.usuario_usuario
            }

            print(f"Datos cargados: {id_y_nombre}")

        except Exception as error:
            print(f"Error al obtener el usuario: {error}")
            return
        # ======= FIN Obtener el ID del usuario desde el boton ========
        
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

        on_change = buscar_usuarios, # Buscar en tiempo real

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
                                    "Usuarios",
                                    size = 24,
                                    weight = ft.FontWeight.BOLD,
                                    color = "#6b1d41"
                                ),

                                # Campo de busqueda
                                campo_de_busqueda,
                                
                                # Boton de crear
                                ft.OutlinedButton(
                                    "Registrar",
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
                                                    
                                    icon = ft.Icons.PERSON,
                                    on_click = abrir_formulario_registrar_modal # Al hacer clic, sobre el boton de "Registrar" se abrira el modal
                                ),
                            ],
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
                
                ft.Divider(),
                
                ft.Container(
                    content = tabla,
                    border = ft.Border.all(
                        1,
                        ft.Colors.BLUE_900
                    ),
                    expand = True,
                    border_radius = 10,
                    width = 5000,
                    padding = 10
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
        usuarios = cargar_usuarios()

        tabla.rows.clear()
        for usuario in usuarios:
            # Concatenar nombre completo
            usuario_nombre_completo = obtener_nombre_completo(usuario)

            tabla.rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(usuario_nombre_completo, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(usuario.usuario_contrasenia, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(usuario.usuario_nuempleado, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(usuario.usuario_correo, color = "#0d1b2a")),
                        ft.DataCell(ft.Text(usuario.usuario_privilegio, color = "#0d1b2a")),
                        ft.DataCell(
                            ft.Row(
                                controls = [
                                    # Boton Editar
                                    ft.OutlinedButton(
                                        #f"Editar ID:{usuario.usuario_id}",
                                        "Editar",
                                        data = usuario.usuario_id, # Recuperar el ID del usuario

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
                                        #f"Eliminar ID:{usuario.usuario_id}",
                                        "Eliminar",
                                        data = usuario.usuario_id,

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

                                        on_click = abrir_alerta_eliminar_usuario # Al hacer clic, sobre el boton de "Editar" se abrira el modal
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

    except Exception as error:
        print(f"Error al consultar los usuarios: {error}")

    return pila