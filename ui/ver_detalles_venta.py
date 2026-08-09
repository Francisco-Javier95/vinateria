import flet as ft
from datetime import datetime

from dao.detalle_venta_dao import DetalleVentaDAO
from dao.venta_dao import VentaDAO
from dao.articulo_dao import ArticuloDAO

def ver_detalles(venta_id, regresar):
    # ============================================================
    # === OBTENER DATOS DE LA VENTA ===
    # ============================================================
    venta_dao = VentaDAO()
    venta = venta_dao.obtener_id_de_la_venta(venta_id)
    
    if venta is None:
        # Si no se encuentra la venta, mostrar un mensaje de error
        return ft.Container(
            content=ft.Column([
                ft.Text("Venta no encontrada", size=20, color="#de3b40"),
                ft.ElevatedButton("Regresar", on_click=lambda e: regresar()),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
        )

    # Obtener los IDs de los productos de la venta
    # venta.venta_articulo es un array de IDs (puede ser lista o string con formato {1,2,3})
    if isinstance(venta.venta_articulo, list):
        articulos_ids = [int(id) for id in venta.venta_articulo]
    elif isinstance(venta.venta_articulo, str):
        # Formato: '{1,2,3}'
        ids_str = venta.venta_articulo.strip("{}")
        articulos_ids = [int(id) for id in ids_str.split(",")] if ids_str else []
    else:
        articulos_ids = []

    # === OBTENER NOMBRES, PRECIOS Y SUBTOTALES ===
    articulo_dao = ArticuloDAO()
    productos = []
    for id_art in articulos_ids:
        articulo = articulo_dao.obtener_id_del_articulo(id_art)
        if articulo:
            # Por ahora, cantidad = 1 (puedes ajustar si tienes cantidades reales)
            cantidad = 1
            subtotal = articulo.articulo_precio * cantidad
            productos.append({
                'nombre': articulo.articulo_articulo,
                'precio': articulo.articulo_precio,
            })

    # Obtener detalles de la venta
    detalle_dao = DetalleVentaDAO()
    detalles = detalle_dao.obtener_por_venta(venta_id)
    
    articulo_dao = ArticuloDAO()
    productos_detalle = []

    for detalle in detalles:
        articulo = articulo_dao.obtener_id_del_articulo(detalle.detalle_articulo_id) 
        if articulo:
            productos_detalle.append({
                'nombre': articulo.articulo_articulo,
                'cantidad': detalle.detalle_cantidad, 
                'precio_unitario': detalle.detalle_precio_unitario, 
                'subtotal': detalle.detalle_subtotal
            })

    # ============================================================
    # === CONSTRUIR EL TICKET ===
    # ============================================================
    
    # === DATOS FIJOS ===
    telefono = "+52-247-124-####"  # Teléfono estático (puedes cambiarlo)
    fecha = venta.venta_fecha if venta.venta_fecha else datetime.now().strftime("%d/%m/%Y")
    empleado = venta.venta_usuario if venta.venta_usuario else "Empleado #1"
    total = venta.venta_ganancia

    # === CONTENIDO DEL TICKET ===
    ticket_content = ft.Column(
        controls=[
            ft.Column(
                controls = [
                    # ft.Text("La Vinata", size=28, color="#6b1d41", expand=True, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
                    # ft.Text("Vinos y Licores  ", size=20, color="#c9a03d", expand=True, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)

                    ft.Image(
                        src = f"imagenes/Texto_descripcion_Logotipo.png",
                        width = 200,
                        border_radius = 10,
                    )
                ], width= 800, spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment = ft.CrossAxisAlignment.CENTER
            ),

            # === ENCABEZADO: Teléfono y Fecha ===
            ft.Container(
                content = ft.Row(
                    controls=[
                        ft.Text(f"Teléfono: {telefono}", size=14, color="#9095a0"),
                        ft.Text(f"Fecha: {str(fecha)}", size=14, color="#9095a0", weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.Padding.symmetric(vertical=5, horizontal=0),
            ),
            
            
            ft.Text("****************************************", size=18, color="#9095a0", weight=ft.FontWeight.BOLD),
            
            # === TÍTULO ===
            ft.Text("Ticket de compras", size=20, weight=ft.FontWeight.BOLD, color="#9095a0"),
            
            ft.Text("****************************************", size=18, color="#9095a0", weight=ft.FontWeight.BOLD),
            
            # === LISTA DE PRODUCTOS ===
            ft.Row(
                controls = [
                    ft.Text("Producto", size = 12, weight = ft.FontWeight.BOLD, color = "#926600"),
                    ft.Text("Cantidad", size = 12, weight = ft.FontWeight.BOLD, color = "#926600"),
                    ft.Column(
                        controls = [
                            ft.Text("Precio", size = 12, weight = ft.FontWeight.BOLD, color = "#926600", text_align = ft.TextAlign.CENTER),
                            ft.Text("unitario", size = 12, weight = ft.FontWeight.BOLD, color = "#926600",  text_align = ft.TextAlign.CENTER)
                        ],
                        spacing = 0,
                        margin = 0
                    ),
                    ft.Text("Subtotal", size = 12, weight = ft.FontWeight.BOLD, color = "#926600")
                ],
                alignment= ft.MainAxisAlignment.SPACE_BETWEEN
            ),

            ft.Text("---------------------------------------------", size = 18, color="#c9a03d"),

            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(f"- {item['nombre']}", size=12, color="#0d1b2a", expand=2),
                            ft.Text(f"{item['cantidad']}", size=12, color="#0d1b2a", expand=2, margin = ft.Margin.only(left = 25)),
                            ft.Row( controls = [ ft.Icon(ft.Icons.ATTACH_MONEY, size = 18, color = "#c9a03d"), ft.Text(f"{item['precio_unitario']:,.2f}", size=12, color="#0d1b2a", expand=1) ], spacing=0, margin = ft.Margin.only(right = 20)),
                            ft.Row( controls = [ ft.Icon(ft.Icons.ATTACH_MONEY, size = 18, color = "#c9a03d"), ft.Text(f"{item['subtotal']:,.2f}", size=12, color="#0d1b2a", expand=1) ], spacing=0),
                        ],
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                    ) 
                    for item in productos_detalle
                ] if productos_detalle else [
                    ft.Text("No hay productos en esta venta", size=14, color="#9095a0")
                ],
                spacing=5,
                height=225,
                scroll=ft.ScrollMode.AUTO,
            ),
            
            ft.Text("****************************************", size=18, color="#9095a0", weight=ft.FontWeight.BOLD, margin=ft.Margin.only(top=10)),
            
            # === TOTAL Y EMPLEADO ===
            ft.Row(
                controls=[
                    ft.Row(
                        controls = [
                            ft.Text("Empleado:", size=14, color="#424955"),
                            ft.Text(empleado, size=14, color="#2E3239", weight=ft.FontWeight.W_400),
                        ]
                    ),
                    
                    ft.Row(
                        controls = [
                            ft.Text("Total:", size=14, weight=ft.FontWeight.BOLD, color="#6b1d41"),
                            ft.Text(f"${total:,.2f}", size=14, weight=ft.FontWeight.BOLD, color="#c9a03d"),
                        ]
                    )
                    
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            
             ft.Text("****************************************", size=18, color="#9095a0", weight=ft.FontWeight.BOLD, margin=ft.Margin.only(top=10)),
            
            # === PIE DE PÁGINA ===
            ft.Text("¡Gracias por tu preferencia!", size=20, color="#6b1d41", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_500),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # === CONTENEDOR DEL TICKET (estilo de ticket físico) ===
    ticket = ft.Container(
        content=ticket_content,
        bgcolor="#ffffff",
        border=ft.Border.all(1, "#e2dcd5"),
        border_radius=5,
        padding=30,
        width=400,
        height=650,
    )

    # === BOTÓN REGRESAR ===
    btn_regresar = ft.ElevatedButton(
        "Regresar",
        icon=ft.Icons.ARROW_BACK,
        style=ft.ButtonStyle(
            bgcolor="#6b1d41",
            color="#ffffff",
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=lambda e: regresar(),
    )

    # === CONTENEDOR PRINCIPAL (centrado) ===
    contenido = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[btn_regresar],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=ticket,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            spacing=20,
            expand=True,
        ),
        padding=20,
        expand=True,
    )

    return contenido