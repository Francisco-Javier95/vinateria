import flet as ft
from database.conexion import Conexion
from datetime import datetime
import psycopg2

import flet.canvas as cv

import math
from math import pi

def informes(regresar):

    pila = ft.Stack(expand=True)

    def obtener_ingresos_totales():
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT COALESCE(SUM(venta_ganancia), 0) FROM ventas WHERE venta_estado = 'Concluida'")
        total = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        return float(total)  # Convertir a float

    def obtener_ventas_por_tipo(tipo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(a.articulo_vendidos), 0)
            FROM articulos_1 a
            INNER JOIN categorias c ON a.articulo_categoria = c.categoria_id
            WHERE c.categoria_tipo = %s
        """, (tipo,))
        total = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        return int(total)

    def obtener_ganancia_promedio():
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT COALESCE(AVG(venta_ganancia), 0) FROM ventas WHERE venta_estado = 'Concluida'")
        promedio = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        return float(promedio)  # Convertir a float

    def obtener_ventas_por_mes():
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT EXTRACT(MONTH FROM venta_fecha) as mes, 
                COALESCE(SUM(venta_ganancia), 0) as total
            FROM ventas 
            WHERE venta_estado = 'Concluida' 
            AND EXTRACT(YEAR FROM venta_fecha) = EXTRACT(YEAR FROM CURRENT_DATE)
            GROUP BY mes
            ORDER BY mes
        """)
        datos = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        ventas_por_mes = {i: 0.0 for i in range(1, 13)}  # Usar float
        for mes, total in datos:
            ventas_por_mes[int(mes)] = float(total)
        return ventas_por_mes

    def obtener_ventas_por_categoria():
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT c.categoria_categoria, COALESCE(SUM(a.articulo_vendidos), 0) as total
            FROM articulos_1 a
            INNER JOIN categorias c ON a.articulo_categoria = c.categoria_id
            WHERE a.articulo_vendidos > 0
            GROUP BY c.categoria_categoria
            ORDER BY total DESC
        """)
        datos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return [(nombre, int(total)) for nombre, total in datos]

    def obtener_top_productos():
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT a.articulo_id, a.articulo_articulo,
                c.categoria_categoria, a.articulo_imagen,
                a.articulo_vendidos as unidades_vendidas,
                a.articulo_vendidos * a.articulo_precio as ingresos
            FROM articulos_1 a
            INNER JOIN categorias c ON a.articulo_categoria = c.categoria_id
            WHERE a.articulo_vendidos > 0
            ORDER BY a.articulo_vendidos DESC
            LIMIT 5
        """)
        datos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return [(id_art, nombre, categoria, imagen, int(unidades), float(ingresos))
                for id_art, nombre, categoria, imagen, unidades, ingresos in datos]


    def obtener_ganancia_por_tipo(tipo):
        """
        Devuelve la ganancia total (ingresos) de productos
        que pertenecen a categorías del tipo especificado.
        Ganancia = precio * unidades_vendidas.
        """
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(a.articulo_precio * a.articulo_vendidos), 0)
            FROM articulos_1 a
            INNER JOIN categorias c ON a.articulo_categoria = c.categoria_id
            WHERE c.categoria_tipo = %s
        """, (tipo,))
        total = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        return float(total)




    def dibujar_pastel(categorias, total):
        """
        Dibuja una gráfica de pastel con ft.Canvas.
        categorias: lista de tuplas (nombre, cantidad)
        total: suma de cantidades (para calcular porcentajes)
        """
        colores = ["#6b1d41", "#c9a03d", "#926600", "#d30000", "#96C61B", "#AC0A32", "#33011C"]
        
        # Crear canvas
        canvas = cv.Canvas(width=350, height=350)
        
        # Centro y radio
        cx, cy = 125, 125
        radio = 1
        
        angulo_inicio = -90  # Comienza desde arriba (12 en punto)
        
        for i, (nombre, cantidad) in enumerate(categorias):
            if total == 0:
                break
            angulo = (cantidad / total) * 360
            color = colores[i % len(colores)]
            
            # Calcular ángulo de fin
            angulo_fin = angulo_inicio + angulo
            
            # Convertir a radianes
            inicio_rad = math.radians(angulo_inicio)
            fin_rad = math.radians(angulo_fin)
            
            # Calcular puntos para el arco
            # Usamos arcos con ft.Arc
            canvas.shapes.append(
                cv.Arc(
                    x=cx - radio,
                    y=cy - radio,
                    width=radio * 2,
                    height=radio * 2,
                    start_angle=inicio_rad,
                    sweep_angle=fin_rad - inicio_rad,
                    paint=ft.Paint(
                        style=ft.PaintingStyle.STROKE,
                        color=color,
                        stroke_width=210
                    ),
                )
            )
            
            # También podemos agregar una línea divisoria (opcional)
            # y un punto central (para que parezca un pastel)
            
            angulo_inicio = angulo_fin
        
        # Agregar un círculo interior blanco para efecto de anillo (opcional)
        canvas.shapes.append(
            cv.Circle(
                x=cx,
                y=cy,
                radius=radio * 0.5,
                paint=ft.Paint(
                    style=ft.PaintingStyle.FILL,
                    color="#ffffff",
                ),
            )
        )

        return canvas


    # === OBTENER DATOS ===
    ingresos_totales = obtener_ingresos_totales()
    ventas_vino = obtener_ventas_por_tipo("Vino")
    ventas_licor = obtener_ventas_por_tipo("Licor")
    ganancia_promedio = obtener_ganancia_promedio()
    ventas_por_mes = obtener_ventas_por_mes()
    ventas_por_categoria = obtener_ventas_por_categoria()
    top_productos = obtener_top_productos()

    ganancia_vino = obtener_ganancia_por_tipo("Vino")
    ganancia_licor = obtener_ganancia_por_tipo("Licor")

    # === TARJETAS DE RESUMEN ===
    tarjeta_ingresos = ft.Container(
        content = ft.Row(
            controls = [
                ft.Container(
                    content = ft.Container(
                        content = ft.Icon(
                            ft.Icons.ATTACH_MONEY,
                            size = 45,
                            color = "#c9a03d"
                        ),
                        bgcolor = "#fff6e5",
                        border = ft.Border.all(
                            1,
                            "#c9a03d"
                        ),
                        border_radius = 60,
                        width = 60,
                        height = 60,
                        alignment = ft.Alignment.CENTER
                    ),
                    bgcolor = "#ffe8b2",
                    padding = ft.Padding.symmetric(vertical=30, horizontal=5),
                ),
                ft.Column([
                    ft.Text(
                        "Ingresos Totales", 
                        size=16, 
                        color="#7c5700", 
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(f"${ingresos_totales:,.2f}", size=24, color="#6b1d41", weight=ft.FontWeight.BOLD),
                ], alignment = ft.MainAxisAlignment.CENTER, spacing=0)
            ],
            height = 200
        ),
        bgcolor="#ffffff",
        border=ft.Border.all(2, "#ffe8b2"),
        border_radius=10,
        height = 120, 
        expand=True,
    )

    tarjeta_vino = ft.Container(
        content = ft.Row(
            controls = [
                ft.Container(
                    content = ft.Container(
                        content = ft.Icon(
                            ft.Icons.WINE_BAR,
                            size = 45,
                            color = "#c9a03d"
                        ),
                        bgcolor = "#fff6e5",
                        border = ft.Border.all(
                            1,
                            "#c9a03d"
                        ),
                        border_radius = 60,
                        width = 60,
                        height = 60,
                        alignment = ft.Alignment.CENTER
                    ),
                    bgcolor = "#ffe8b2",
                    padding = ft.Padding.symmetric(vertical=30, horizontal=5),
                ),
                ft.Column([
                    ft.Text(
                        "Ventas de Vinos", 
                        size=16, 
                        color="#7c5700", 
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(f"${ganancia_vino:,.2f}", size = 24, color="#6b1d41", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Unidades: {ventas_vino}", size=18, color="#4c4c4c")
                ], alignment = ft.MainAxisAlignment.CENTER, spacing=0)
            ],
            height = 200
        ),
        bgcolor="#ffffff",
        border=ft.Border.all(2, "#ffe8b2"),
        border_radius=10,
        height = 120, 
        expand=True,
    )

    tarjeta_licor = ft.Container(
        content = ft.Row(
            controls = [
                ft.Container(
                    content = ft.Container(
                        content = ft.Icon(
                            ft.Icons.LOCAL_BAR,
                            size = 45,
                            color = "#c9a03d"
                        ),
                        bgcolor = "#fff6e5",
                        border = ft.Border.all(
                            1,
                            "#c9a03d"
                        ),
                        border_radius = 60,
                        width = 60,
                        height = 60,
                        alignment = ft.Alignment.CENTER
                    ),
                    bgcolor = "#ffe8b2",
                    padding = ft.Padding.symmetric(vertical=30, horizontal=5),
                ),
                ft.Column([
                    ft.Text(
                        "Ventas de Licores", 
                        size=16, 
                        color="#7c5700", 
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(f"${ganancia_licor:,.2f}", size = 24, color="#6b1d41", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Unidades: {ventas_licor}", size=18, color="#4c4c4c")
                ], alignment = ft.MainAxisAlignment.CENTER, spacing=0)
            ],
            height = 200
        ),
        bgcolor="#ffffff",
        border=ft.Border.all(2, "#ffe8b2"),
        border_radius=10,
        height = 120, 
        expand=True,
    )

    tarjeta_promedio = ft.Container(
        content = ft.Row(
            controls = [
                ft.Container(
                    content = ft.Container(
                        content = ft.Icon(
                            ft.Icons.RECEIPT,
                            size = 45,
                            color = "#c9a03d"
                        ),
                        bgcolor = "#fff6e5",
                        border = ft.Border.all(
                            1,
                            "#c9a03d"
                        ),
                        border_radius = 60,
                        width = 60,
                        height = 60,
                        alignment = ft.Alignment.CENTER
                    ),
                    bgcolor = "#ffe8b2",
                    padding = ft.Padding.symmetric(vertical=30, horizontal=5),
                ),
                ft.Column([
                    ft.Text(
                        "Ganancia Promedio", 
                        size=16, 
                        color="#7c5700",
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(f"${ganancia_promedio:,.2f}", size=24, color="#6b1d41", weight=ft.FontWeight.BOLD),
                ], alignment = ft.MainAxisAlignment.CENTER, spacing=0)
            ],
            height = 200
        ),
        bgcolor="#ffffff",
        border=ft.Border.all(2, "#ffe8b2"),
        border_radius=10,
        height = 120, 
        expand=True,
    )

    fila_tarjetas = ft.Row(
        controls=[tarjeta_ingresos, tarjeta_vino, tarjeta_licor, tarjeta_promedio],
        spacing=20,
        expand=True,
    )

    # === GRÁFICA DE BARRAS (VENTAS POR MES) ===
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    max_valor = max(ventas_por_mes.values()) if ventas_por_mes else 1.0

    barras = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        height=(ventas_por_mes[i+1] / max_valor) * 270 if max_valor > 0 else 0,
                        width=20,
                        gradient = ft.LinearGradient(
                            begin=ft.Alignment(-1, -1), # Punto de inicio (arriba-izquierda)
                            end=ft.Alignment(1, 1), # Punto final (abajo-derecha)
                            colors=["#c9a03d", "#7c5700"] # Lista de colores del degradado
                        ),
                        border_radius=0,
                        tooltip = f"${ventas_por_mes[i+1]:,.0f}"
                    ),

                    
                    ft.Container(content = ft.Text(""), height = 1, width = 35, bgcolor = "#e2dcd5"),

                    ft.Text(meses[i], size=15, color = "#171a1f")
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.END,
                spacing=0,
            ) for i in range(12)
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        expand=True,
    )

    contenedor_barras = ft.Container(
        content=ft.Row(
            controls = [
                ft.Column([
                    ft.Text("Ventas Mensuales (Año Actual)", size=18, weight=ft.FontWeight.BOLD, color="#6b1d41"),
                    ft.Container(
                        content = barras,
                        bgcolor = "#f9f6f0",
                        width=580,
                        expand= True
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ],
            width = 700,
            scroll=ft.ScrollMode.AUTO
        ),
        bgcolor="#f9f6f0",
        border=ft.Border.all(1, "#e2dcd5"),
        border_radius=10, 
        padding=20,
        expand=True,
    )

    # === GRÁFICA DE PASTEL (VENTAS POR CATEGORÍA) ===
    # total_categorias = sum(cantidad for _, cantidad in ventas_por_categoria) or 1
    # colores = ["#6b1d41", "#c9a03d", "#926600", "#de3b40", "#4CAF50"]

    # pastel = ft.Column(
    #     controls=[
    #         ft.Row(
    #             controls=[
    #                 ft.Container(width=20, height=20, bgcolor=colores[i % len(colores)], border_radius=25),
    #                 ft.Text(f"{nombre} ({cantidad})", size=12, color="#171a1f"),
    #             ],
    #             spacing=5,
    #         ) for i, (nombre, cantidad) in enumerate(ventas_por_categoria)
    #     ],
    #     alignment=ft.MainAxisAlignment.CENTER,
    #     height = 250,
    #     scroll = ft.ScrollMode.AUTO,
    #     spacing=10,
    #     margin=ft.Margin.only(bottom=50),
    # )

    # pastel_visual = ft.Container(
    #     width=250,
    #     height=250,
    #     margin=ft.Margin.only(bottom=50),

    #     bgcolor="#000000",
    #     border_radius=250,
    #     content=ft.Stack(
    #         controls=[
    #             ft.Container(
    #                 content=ft.Text("Ventas por\nCategoría", size=14, text_align=ft.TextAlign.CENTER),
    #                 alignment=ft.MainAxisAlignment.CENTER,
    #             )
    #         ]
    #     ),
    # )

    # contenedor_pastel = ft.Container(
    #     content=ft.Column([
    #         ft.Text("Ventas por Categoría", size=18, weight=ft.FontWeight.BOLD, color="#6b1d41"),
    #         ft.Row([
    #             pastel_visual,
    #             pastel,
    #         ], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
    #     ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    #     bgcolor="#f9f6f0",
    #     border=ft.Border.all(1, "#e2dcd5"),
    #     border_radius=10,
    #     padding=20,
    #     expand=True,
    # )

    # === GRÁFICA DE PASTEL (VENTAS POR CATEGORÍA) ===
    total_categorias = sum(cantidad for _, cantidad in ventas_por_categoria) or 1
    colores = ["#6b1d41", "#c9a03d", "#926600", "#d30000", "#96C61B", "#AC0A32", "#33011C"]

    # Dibujar la gráfica de pastel con Canvas
    pastel_canvas = ft.Container(
        content=dibujar_pastel(ventas_por_categoria, total_categorias),
        width=250,
        height=250,
    )

    # Leyenda de categorías
    leyenda = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(width=16, height=16, bgcolor=colores[i % len(colores)], border_radius=16),
                    ft.Text(f"{nombre} ({cantidad}) - {cantidad/total_categorias*100:.1f}%", size=12, color = "#171a1f"),
                ],
                spacing=8,
            ) for i, (nombre, cantidad) in enumerate(ventas_por_categoria)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        height = 200,
        scroll = ft.ScrollMode.AUTO,
        spacing=10,
        margin=ft.Margin.only(bottom=50),
    )

    contenedor_pastel = ft.Container(
        content=ft.Column([
            ft.Text("Ventas por Categoría", size=18, weight=ft.FontWeight.BOLD, color="#6b1d41", margin = ft.Margin.only(bottom = 20)),
            ft.Row([
                pastel_canvas,
                leyenda,
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=30, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ]),
        bgcolor="#f9f6f0",
        border=ft.Border.all(1, "#e2dcd5"),
        border_radius=10,
        padding=20,
        expand=True,
    )

    # === TABLA DE PRODUCTOS MÁS VENDIDOS ===
    tabla_top = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#", color="#926600", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre", color="#926600", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Categoría", color="#926600", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Unidades vendidas", color="#926600", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Ingresos", color="#926600", weight=ft.FontWeight.BOLD)),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Row( controls = [ ft.Text(f"{i+1}", color="#0d1b2a", weight=ft.FontWeight.BOLD), ft.Image(src = f"assets/imagenes/imagenes_DB/{imagen}", width=100, margin = ft.Margin.only(left = 80)) ])),
                    ft.DataCell(ft.Text(nombre, color="#0d1b2a")),
                    ft.DataCell(ft.Row(controls =[ft.Container(width=16, height=16, bgcolor=colores[i % len(colores)], border_radius=16), ft.Text(categoria, color="#0d1b2a") ])),
                    ft.DataCell(ft.Text(str(unidades), color="#0d1b2a", weight = ft.FontWeight.BOLD, text_align= ft.TextAlign.CENTER, width = 130, expand = True)),
                    ft.DataCell(ft.Row(controls = [ft.Icon(ft.Icons.ATTACH_MONEY, size = 20, color = "#c9a03d"), ft.Text(f"{ingresos:,.2f}", color="#0d1b2a") ], spacing = 0)),
                ]
            ) for i, (id_art, nombre, categoria, imagen, unidades, ingresos) in enumerate(top_productos)
        ],
        expand=True,
        divider_thickness=0,
        width = 5000 
    )

    contenedor_tabla = ft.Container(
        content=ft.Column([
            tabla_top,
        ]),
        bgcolor="#ffffff",
        border=ft.Border.all(1, "#e2dcd5"),
        border_radius=10,
        padding=20,
        expand=True,
        width = 5000
    )

    # === CONTENIDO PRINCIPAL ===
    contenido = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Row([
                    ft.Text(
                        "Informes", 
                        size=28, 
                        weight=ft.FontWeight.BOLD, 
                        color="#6b1d41"
                    ),
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
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),


                # Tarjetas de resumen
                fila_tarjetas,


                # Gráficas lado a lado
                ft.Row(
                    controls=[contenedor_barras, contenedor_pastel],
                    spacing=20,
                    height = 400,
                ),

                # Tabla de top productos
                contenedor_tabla,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
    )

    pila.controls.append(contenido)
    return pila