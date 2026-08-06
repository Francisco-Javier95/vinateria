import flet as ft
from datetime import datetime

from models.venta import Venta
from dao.venta_dao import VentaDAO
from models.venta import Venta_confirmar
from models.detalle_venta import DetalleVenta
from dao.detalle_venta_dao import DetalleVentaDAO

from dao.articulo_dao import ArticuloDAO

def confirmar_form(regresar=None, formulario_visible=False, cerrando_modal=None, total=0.0, lista_articulos=None, lista_cantidades = None, usuario_id = None, limpiar_lista=None, venta_id_actual=None):
    # Estilos de los label
    estilo_de_label = ft.TextStyle(
        color="#926600",
        weight=ft.FontWeight.BOLD,
        size=14
    )
    estilo_del_label_focus = ft.TextStyle(
        color="#424955",
        weight=ft.FontWeight.BOLD,
        size=14
    )

    # Variables de estado
    cambio_actual = 0.0
    total_actual = total
    articulos_ids = lista_articulos if lista_articulos else []
    articulos_cantidades = lista_cantidades if lista_cantidades else []
    usuario_actual = usuario_id  # Ahora usuario_actual contiene el ID del usuario

    # Función/Metodo para calcular el cambio
    def calcular_cambio(e):
        # Calcula el cambio en tiempo real mientras el usuario escribe
        nonlocal cambio_actual
        
        try:
            # Obtener el valor del efectivo
            efectivo_texto = e.control.value.strip() if e.control.value else "0"
            efectivo = float(efectivo_texto) if efectivo_texto else 0.0
            
            # Calcular cambio
            cambio = efectivo - float(total_actual)
            
            # Actualizar texto del cambio
            if cambio >= 0:
                texto_cambio.value = f"{cambio:.2f}"
                texto_cambio.color = "#1B1C1D"
                # Habilitar botón de confirmar si el pago es suficiente
                boton_confirmar.disabled = False
                boton_confirmar.bgcolor = "#6b1d41"
            else:
                texto_cambio.value = f"{cambio:.2f}"
                boton_confirmar.disabled = True
                boton_confirmar.bgcolor = "#696768"
                            
            
            e.page.update()
            
        except ValueError:
            texto_cambio.value = "$0.00"
            texto_cambio.color = "#1B1C1D"
            boton_confirmar.disabled = True
            e.page.update()


    # ====== FUNCIÓN PARA CONFIRMAR LA VENTA =====
    def confirmar_venta(evento):
        # Guarda la venta en la base de datos
        try:
            # Obtener el valor del efectivo
            efectivo_texto = efectivo_input.value.strip() if efectivo_input.value else "0"
            efectivo = float(efectivo_texto) if efectivo_texto else 0.0

            
            # Validar que el pago sea suficiente
            if efectivo < total_actual:
                print("El pago es insuficiente")
                evento.page.update()
                return
            

            # # === ACTUALIZAR STOCK Y VENDIDOS ===
            # articulo_dao = ArticuloDAO()

            # for i, id_articulo in enumerate(articulos_ids):
            #     cantidad_vendida = articulos_cantidades[i]
            #     articulo = articulo_dao.obtener_id_del_articulo(id_articulo)
            #     if not articulo:
            #         raise Exception(f"Producto ID {id_articulo} no encontrado")
            #     if articulo.articulo_stock < cantidad_vendida:
            #         raise Exception(f"Stock insuficiente para '{articulo.articulo_articulo}'. "
            #                         f"Disponible: {articulo.articulo_stock}, solicitado: {cantidad_vendida}")
            #     # Descontar stock y sumar vendidos
            #     articulo.articulo_stock -= cantidad_vendida
            #     articulo.articulo_vendidos += cantidad_vendida
            #     articulo_dao.actualizar(articulo)
            #     print(f"Stock actualizado: {articulo.articulo_articulo} → "
            #         f"Stock: {articulo.articulo_stock}, Vendidos: {articulo.articulo_vendidos}")
                

            # Guardar la venta
            venta_dao = VentaDAO()
            # articulos_array = "{" + ",".join(str(id) for id in articulos_ids) + "}"
            
            
            # Crear el nombre de la venta con timestamp
            venta_nombre = f"VEN-{datetime.now().strftime('%Y%m%d_%H%M%S')}-VINATA"

            # Estado de la venta (al confirmarse es utomaticamente "Concluida")
            estado = "Concluida"
            
            # Insertar en la base de datos
            venta_dao = VentaDAO()

            # === VERIFICAR SI ES ACTUALIZACIÓN O INSERCIÓN ===
            if venta_id_actual is not None:
                # === ACTUALIZAR VENTA EXISTENTE ===
                venta_existente = venta_dao.obtener_id_de_la_venta(venta_id_actual)
                if venta_existente:
                    # Crear objeto con los datos actualizados
                    venta_actualizada = Venta(
                        venta_id = venta_id_actual,
                        venta_venta = venta_existente.venta_venta,  # Mantener el nombre original
                        venta_fecha = None,
                        venta_ganancia = total_actual,
                        venta_usuario = usuario_actual,
                        venta_articulo = None,
                        venta_estado = estado
                    )
                    venta_dao.actualizar(venta_actualizada)
                    print(f"Venta {venta_existente.venta_venta} actualizada exitosamente")
                else:
                    print("No se encontró la venta a actualizar")
                    evento.page.update()
                    return
            else:
                # === CREAR NUEVA VENTA ===
                nueva_venta = Venta_confirmar(
                    venta_id = None,
                    venta_venta = venta_nombre,
                    venta_ganancia = total_actual,
                    venta_usuario = usuario_actual,
                    venta_articulo = None,
                    venta_estado = estado
                )
                venta_dao.insertar(nueva_venta)
                print(f"Venta {venta_nombre} registrada exitosamente")

                # Obtener el ID de la venta recién insertada
                venta_id = venta_dao.obtener_ultimo_id()

                # Guardar los detalles de la venta
                detalle_dao = DetalleVentaDAO()
                for i, id_articulo in enumerate(articulos_ids):
                    cantidad = articulos_cantidades[i]
                    
                    # Obtener el precio del artículo
                    articulo_dao = ArticuloDAO()
                    articulo = articulo_dao.obtener_id_del_articulo(id_articulo)
                    precio_unitario = articulo.articulo_precio
                    subtotal = precio_unitario * cantidad
                    
                    detalle = DetalleVenta(
                        detalle_id = None,
                        detalle_venta_id = venta_id,
                        detalle_articulo_id = id_articulo,
                        detalle_cantidad = cantidad,
                        detalle_precio_unitario = precio_unitario,
                        detalle_subtotal = subtotal
                    )
                    detalle_dao.insertar(detalle)

                    # Actualizar stock y vendidos (como ya tenías)
                    articulo.articulo_stock -= cantidad
                    articulo.articulo_vendidos += cantidad
                    articulo_dao.actualizar(articulo)

                print(f"Venta {venta_nombre} registrada exitosamente")

            evento.page.update()

            import time
            time.sleep(0.5)

            # Limpiar lista
            if limpiar_lista:
                limpiar_lista()

            # Cerrar modal
            if formulario_visible and cerrando_modal:
                cerrando_modal()
                return
            
        except Exception as error:
            print(f"Error al registrar la venta: {error}")
            evento.page.update()


    # ====== CREAR LOS CONTROLES DESPUÉS DE LAS FUNCIONES ========

    # ------------ Campos del formulario ------------------
    efectivo_input = ft.TextField(
        label="Efectivo: ",
        label_style=estilo_de_label,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^[0-9]*\.?[0-9]*$",
            replacement_string=""
        ),
        on_focus=lambda e: setattr(e.control, 'label_style', estilo_del_label_focus) or e.control.update(),
        on_blur=lambda e: setattr(e.control, 'label_style', estilo_de_label) or e.control.update(),
        on_change=calcular_cambio,  # Calcular cambio dinamiacamente
        hint_text="0.00",
        focused_border_color="#c9a03d",
        expand=True,
        color="#424955",
        suffix_icon=ft.Icons.ATTACH_MONEY,
        max_length=10,
        counter=ft.Container(),
    )

    # Texto del total a pagar
    texto_total = ft.Text(
        f"${total_actual:.2f}",
        color="#1B1C1D",
        size=16
    )

    # Texto del cambio (dinámico)
    texto_cambio = ft.Text(
        "$0.00",
        color="#1B1C1D",
        size=16
    )

    # Botón confirmar
    boton_confirmar = ft.ElevatedButton(
        "Confirmar",
        style=ft.ButtonStyle(
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        bgcolor="#696768",
        color="#ffffff",
        width=500,
        disabled=True,  # Inicialmente deshabilitado
        on_click=confirmar_venta
    )

    # ------------- Construir el encabezado según el modo ------------------
    controles_encabezado = []

    if formulario_visible:
        controles_encabezado.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        style=ft.ButtonStyle(
                            side={
                                ft.ControlState.DEFAULT: ft.BorderSide(width=2, color="#a11e2f"),
                                ft.ControlState.HOVERED: ft.BorderSide(width=2, color="#6b1d41")
                            },
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        bgcolor="#6b1d41",
                        icon_color="#ffffff",
                        on_click=lambda e: cerrando_modal() if cerrando_modal else None,
                        tooltip="Cerrar"
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Pago",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color="#c9a03d"
                            )
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
            )
        )
    else:
        controles_encabezado.append(
            ft.Row(
                controls=[
                    ft.Container(
                        bgcolor="#6b1d41",
                    ),
                    ft.Text(
                        "Pago",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#c9a03d"
                    ),
                ]
            )
        )

    # ------------- Construir el formulario ----------------
    contenido_formulario = ft.Column(
        controls=[
            *controles_encabezado,

            # Fila total
            ft.Row(
                controls=[
                    ft.Text(
                        "Total:  ",
                        color="#424955",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Icon(
                        ft.Icons.ATTACH_MONEY,
                        size=22,
                        color="#efb034"
                    ),
                    texto_total,
                ],
                spacing=2,
            ),

            # Campo de efectivo
            efectivo_input,

            # Fila cambio
            ft.Row(
                controls=[
                    ft.Text(
                        "Cambio:  ",
                        color="#424955",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Icon(
                        ft.Icons.ATTACH_MONEY,
                        size=22,
                        color="#efb034"
                    ),
                    texto_cambio,
                ],
                spacing=2,
            ),

            boton_confirmar
        ],
        spacing=15,
        width = 300,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ---------------- Envolver en un contenedor con estilo ----------------
    if formulario_visible:
        
        return ft.Container(
            content = contenido_formulario,
            bgcolor = "#ffffff",
            border_radius = 20,
            padding = 30,
            shadow = ft.BoxShadow(
                spread_radius = 1,
                blur_radius = 20,
                color = ft.Colors.BLACK_38
            ),
            width = 300,
        )
    else:
        return ft.Container(
            padding = 30,
            content = contenido_formulario,
            expand = True
        )