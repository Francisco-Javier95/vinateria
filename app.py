import flet as ft
from ui.main_window import main_window

from dao.articulo_dao import ArticuloDAO
from dao.categoria_dao import CategoriaDAO
from dao.proveedor_dao import ProveedorDAO
from dao.usuario_dao import UsuarioDAO
from models.articulo import Articulo
from models.categoria import Categoria
from models.proveedor import Proveedor
from models.usuario import Usuario
from models.articulo import Articulo_eliminar
from models.categoria import Categoria_eliminar
from models.proveedor import Proveedor_eliminar
from models.usuario import Usuario_eliminar

from datetime import datetime


# ------------------------------------CRUD Artículos------------------------------------
def insertar_articulo():
    articulo_id = None
    articulo_articulo = input("\nEscribe el nombre del artículo: ")
    articulo_codigo = input("\nEscribe el código del artículo: ")
    
    ver_nombres_categorias()
         
    articulo_categoria = int(input("\nEscribe el número correspondiente a la categoria: "))
    articulo_imagen = input("Escribe el nombre de la imagen: ")
    articulo_precio = float(input("Escribe el precio del producto: "))
    articulo_stock = int(input("Escribe el stock: "))
    articulo_proveedor = int(input("Escribe el ID del proveedor: "))

    try:
        articulo_dao = ArticuloDAO()
        articulo = Articulo(articulo_id ,articulo_articulo, articulo_codigo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor)
        articulo_dao.insertar(articulo)
        print("Producto agregado exitosamente")
    except Exception as e:
        print("Error al insertar el producto nuevo")
        print(e)

def ver_articulos():
    try:
        articulo_dao = ArticuloDAO()

        articulos = articulo_dao.obtener_todos()

        print("\n=== Productos en la vinateria ===")

        if len(articulos) == 0:
            print("No hay Productos registrados.")
        else:
            for articulo in articulos:
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
                print(
                    f"ID: {articulo.articulo_id}   "
                    f"Nombre: {articulo.articulo_articulo}   "
                    f"Código: {articulo.articulo_codigo}   "
                    f"Categoría: {articulo.articulo_categoria}   "
                    f"Imagen: {articulo.articulo_imagen}   "
                    f"Precio: {articulo.articulo_precio}   "
                    f"Stock: {articulo.articulo_stock}   "
                    f"Proveedor: {articulo.articulo_proveedor}"
                )
        print("--------------------------------------------------------------------------------------------------------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error: ")
        print(e)

def modificar_articulo():
    ver_articulos() # Mandar a traer todos los registros de los articulos
    print("\n")

    try:
        articulo_dao = ArticuloDAO()
        articulo_id = int(input("Introduce el ID del producto a modificar: "))
        id_modificado = str(articulo_id)

        articulo_articulo = input("\nEscribe el nuevo nombre del producto: ")
        articulo_codigo = input("\nEscribe el nuevo código del producto: ")
        articulo_categoria = int(input("Escribe la nueva categoria del producto: "))
        articulo_imagen = input("Escribe la nueva imagen del producto: ")
        articulo_precio = float(input("Escribe el nuevo precio del producto: "))
        articulo_stock = int(input("Escribe el nuevo stock del producto: "))
        articulo_proveedor = int(input("Escribe el nuevo ID del proveedor: "))

        articulo = Articulo(articulo_id, articulo_articulo, articulo_codigo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor)
        articulo_dao.actualizar(articulo)    

        print("\nProducto "+id_modificado+" modificado exitosamente")
    except Exception as e:
        print("Error al modificar el producto")
        print(e)

def eliminar_articulo():
    try:
        articulo_dao = ArticuloDAO()

        articulos = articulo_dao.obtener_todos()

        print("\n=== Productos en la vinateria ===")

        if len(articulos) == 0:
            print("No hay Prodcutos registrados.")
        else:
            for articulo in articulos:
                print("---------------------------------------------------------------------------------------------------------------------")
                print(
                    f"ID: {articulo.articulo_id}   "
                    f"Nombre: {articulo.articulo_articulo}   "
                    f"Código: {articulo.articulo_codigo}    "
                    f"Categoría: {articulo.articulo_categoria}   "
                    f"Imagen: {articulo.articulo_imagen}   "
                    f"Precio: {articulo.articulo_precio}   "
                    f"Stock: {articulo.articulo_stock}    "
                    f"Proveedor: {articulo.articulo_proveedor}"
                )
        print("---------------------------------------------------------------------------------------------------------------------")
        print("\n Conexión exitosa a la base de datos")

        articulo_id = int(input("\n\nEscribe el ID del producto: "))
        id_eliminado = str(articulo_id)

        try:
            articulo_dao = ArticuloDAO()
            articulo = Articulo_eliminar(articulo_id)
            articulo_dao.eliminar(articulo)

            print("Producto "+id_eliminado+" eliminado exitosamente")
        except Exception as e:
            print("Error al eliminar el producto "+id_eliminado)
            print(e)

    except Exception as e:
        print("Error: ")
        print(e)
# ----------------------------------Fin CRUD Artículos----------------------------------

# ------------------------------------CRUD Catgorías------------------------------------
def insertar_categoria():
    categoria_id = None
    categoria_categoria = input("\nEscribe el nombre de la categoría: ")

    print("\n--------Tipo--------")
    print("Vino")
    print("Licor")
    categoria_tipo = input("\nEscribe el tipo de categoria: ")

    categoria_descripcion = input("Escribe la descripción de la categoría: ")

    try:
        categoria_dao = CategoriaDAO()
        categoria = Categoria(categoria_id, categoria_categoria, categoria_tipo, categoria_descripcion)
        categoria_dao.insertar(categoria)
        print("Categoría agregada exitosamente")
    except Exception as e:
        print("Error al insertar la categoría nueva")
        print(e)

def ver_categorias():
    try:
        categoria_dao = CategoriaDAO()

        categorias = categoria_dao.obtener_todos()

        print("\n-----------Categorías----------")

        if len(categorias) == 0:
            print("No hay categorías registradas.")
        else:
            for categoria in categorias:
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
                print(
                    f"ID: {categoria.categoria_id}   "
                    f"Nombre: {categoria.categoria_categoria}   "
                    f"Tipo: {categoria.categoria_tipo}   "
                    f"Descripción: {categoria.categoria_descripcion}   "
                )
        print("--------------------------------------------------------------------------------------------------------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error: ")
        print(e)

def ver_nombres_categorias():
    try:
        categoria_dao = CategoriaDAO()

        categorias = categoria_dao.nombres_categorias()

        print("\n------Categorias------")

        if len(categorias) == 0:
            print("No hay categorias registradas")
        else:
            for categoria in categorias:
                print(categoria.categoria_categoria)
            print("\nConexion exitosa a la base de datos")
    except Exception as e:
        print("Error: ")
        print(e)


def modificar_categoria():
    ver_categorias() # Mandar a traer todos los registros de las categorías
    print("\n")

    try:
        categoria_dao = CategoriaDAO()
        categoria_id = int(input("Introduce el ID de la categoría a modificar: "))
        id_modificado = str(categoria_id)

        categoria_categoria = input("\nEscribe el nuevo nombre de la categoría: ")

        print("\n--------Tipo--------")
        print("Vino")
        print("Licor")

        categoria_tipo = input("\nEscribe el nuevo tipo de categoría: ")
        categoria_descripcion = input("Escribe la nueva descripción de la categoría: ")

        categoria = Categoria(categoria_id, categoria_categoria, categoria_tipo, categoria_descripcion)
        categoria_dao.actualizar(categoria)    

        print("\nCategoría "+id_modificado+" modificada exitosamente")
    except Exception as e:
        print("Error al modificar la categoría")
        print(e)

def eliminar_categoria():
    try:

        ver_categorias()

        categoria_id = int(input("\n\nEscribe el ID de la categoria: "))
        id_eliminado = str(categoria_id)

        try:
            categoria_dao = CategoriaDAO()
            categoria = Categoria_eliminar(categoria_id)
            categoria_dao.eliminar(categoria)

            print("Categoría "+id_eliminado+" eliminada exitosamente")
        except Exception as e:
            print("Error al eliminar la categoría "+id_eliminado)
            print(e)

    except Exception as e:
        print("Error: ")
        print(e)
# ----------------------------------Fin CRUD Catgorías----------------------------------

# -----------------------------------CRUD Proveedores-----------------------------------
def insertar_proveedor():
    proveedor_id = None
    proveedor_proveedor = input("\nEscribe el nombre del proveedor: ")
    proveedor_aPaterno = input("Escribe el apellido paterno: ")
    proveedor_aMaterno = input("Escribe el apellido materno: ")
    proveedor_telefono = input("Escribe el telefono: ")
    proveedor_direccion = input("Escribe la direccion: ") 
    proveedor_correo = input("Escribe el correo electrónico: ") 

    try:
        proveedor_dao = ProveedorDAO()
        proveedor = Proveedor(proveedor_id, proveedor_proveedor, proveedor_aPaterno, proveedor_aMaterno, proveedor_telefono, proveedor_direccion, proveedor_correo)
        proveedor_dao.insertar(proveedor)
        print("Proveedor agregado exitosamente")
    except Exception as e:
        print("Error al insertar el nuevo proveedor")
        print(e)

def ver_proveedores():
    try:
        proveedor_dao = ProveedorDAO()

        proveedores = proveedor_dao.obtener_todos()

        print("\n-----------Proveedor----------")

        if len(proveedores) == 0:
            print("No hay proveedores registrados.")
        else:
            for proveedor in proveedores:
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
                print(
                    f"ID: {proveedor.proveedor_id}   "
                    f"Nombre: {proveedor.proveedor_proveedor}   "
                    f"Apellido paterno: {proveedor.proveedor_aPaterno}   "
                    f"Apellido materno: {proveedor.proveedor_aMaterno}   "
                    f"Teléfono: {proveedor.proveedor_telefono}   "
                    f"Dirección: {proveedor.proveedor_direccion}   "
                    f"Correo: {proveedor.proveedor_correo}   "
                )
        print("--------------------------------------------------------------------------------------------------------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error: ")
        print(e)

def modificar_proveedor():
    ver_proveedores() # Mandar a traer todos los registros de los proveedores
    print("\n")

    try:
        proveedor_dao = ProveedorDAO()
        proveedor_id = int(input("Introduce el ID del proveedor a modificar: "))
        id_modificado = str(proveedor_id)

        proveedor_proveedor = input("\nEscribe el nuevo nombre del proveedor: ")
        proveedor_aPaterno = input("Escribe el nuevo apellido paterno: ")
        proveedor_aMaterno = input("Escribe el nuevo apellido materno: ")
        proveedor_telefono = input("Escribe el nuevo telefono: ")
        proveedor_direccion = input("Escribe la nueva direccion: ") 
        proveedor_correo = input("Escribe el nuevo correo electrónico: ") 

        proveedor = Proveedor(proveedor_id, proveedor_proveedor, proveedor_aPaterno, proveedor_aMaterno, proveedor_telefono, proveedor_direccion, proveedor_correo)
        proveedor_dao.actualizar(proveedor)    

        print("\nProveedor "+id_modificado+" modificado exitosamente")
    except Exception as e:
        print("Error al modificar el proveedor")
        print(e)

def eliminar_proveedor():
    try:

        ver_proveedores()

        proveedor_id = int(input("\n\nEscribe el ID del proveedor: "))
        id_eliminado = str(proveedor_id)

        try:
            proveedor_dao = ProveedorDAO()
            proveedor = Proveedor_eliminar(proveedor_id)
            proveedor_dao.eliminar(proveedor)

            print("Proveedor "+id_eliminado+" eliminado exitosamente")
        except Exception as e:
            print("Error al eliminar el proveedor "+id_eliminado)
            print(e)

    except Exception as e:
        print("Error: ")
        print(e)
# ---------------------------------Fin CRUD Proveedores---------------------------------

# -------------------------------------CRUD Usuarios------------------------------------
def insertar_usuario():
    usuario_id = None
    usuario_usuario = input("\nEscribe el nombre del usuario: ")
    usuario_apaterno = input("Escribe el apellido paterno: ")
    usuario_amaterno = input("Escribe el apellido materno: ")
    usuario_nuempleado = input("Escribe el número de empleado: ")
    usuario_correo = input("Escribe el correo electrónico: ")
    usuario_contrasenia = input("Escribe el contraseña: ")

    print("\n--------Privilegio--------")
    print("1 - Admin")
    print("2 - Supervisor")
    print("3 - Cajero")
    
    usuario_privilegio = input("\nEscribe el ID del privilegio: ") 

    try:
        usuario_dao = UsuarioDAO()
        usuario = Usuario(usuario_id, usuario_usuario, usuario_apaterno, usuario_amaterno, usuario_nuempleado, usuario_correo, usuario_contrasenia, usuario_privilegio)
        usuario_dao.insertar(usuario)
        print("Usuario agregado exitosamente")
    except Exception as e:
        print("Error al insertar el nuevo usuario")
        print(e)

def ver_usuarios():
    try:
        usuario_dao = UsuarioDAO()

        usuarios = usuario_dao.obtener_todos()

        print("\n-----------Usuario----------")

        if len(usuarios) == 0:
            print("No hay usuarios registrados.")
        else:
            for usuario in usuarios:
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
                print(
                    f"ID: {usuario.usuario_id}   "
                    f"Nombre: {usuario.usuario_usuario}   "
                    f"Apellido paterno: {usuario.usuario_apaterno}   "
                    f"Apellido materno: {usuario.usuario_amaterno}   "
                    f"Número de empleado: {usuario.usuario_nuempleado}   "
                    f"Correo: {usuario.usuario_correo}   "
                    f"Contraseña: {usuario.usuario_contrasenia}   "
                    f"Privilegio: {usuario.usuario_privilegio}   "
                )
        print("--------------------------------------------------------------------------------------------------------------------------------------------")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error: ")
        print(e)

def modificar_usuario():
    ver_usuarios() # Mandar a traer todos los registros de los usuarios
    print("\n")

    try:
        usuario_dao = UsuarioDAO()
        usuario_id = int(input("Introduce el ID del usuario a modificar: "))
        id_modificado = str(usuario_id)

        usuario_usuario = input("\nEscribe el nombre del usuario: ")
        usuario_apaterno = input("Escribe el apellido paterno: ")
        usuario_amaterno = input("Escribe el apellido materno: ")
        usuario_nuempleado = input("Escribe el número de empleado: ")
        usuario_correo = input("Escribe el correo electrónico: ")
        usuario_contrasenia = input("Escribe el contraseña: ")

        print("\n--------Privilegio--------")
        print("1 - Admin")
        print("2 - Supervisor")
        print("3 - Cajero")
        
        usuario_privilegio = input("\nEscribe el ID del privilegio: ") 

        usuario = Usuario(usuario_id, usuario_usuario, usuario_apaterno, usuario_amaterno, usuario_nuempleado, usuario_correo, usuario_contrasenia, usuario_privilegio)
        usuario_dao.insertar(usuario)

        print("\nUsuario "+id_modificado+" modificado exitosamente")
    except Exception as e:
        print("Error al modificar el usuario")
        print(e)

def eliminar_usuario():
    try:

        ver_usuarios()

        usuario_id = int(input("\n\nEscribe el ID del usuario: "))
        id_eliminado = str(usuario_id)

        try:
            usuario_dao = UsuarioDAO()
            usuario = Usuario_eliminar(usuario_id)
            usuario_dao.eliminar(usuario)

            print("Usuario "+id_eliminado+" eliminado exitosamente")
        except Exception as e:
            print("Error al eliminar el usuario "+id_eliminado)
            print(e)

    except Exception as e:
        print("Error: ")
        print(e)
# ----------------------------------Fin CRUD Usuarios-----------------------------------

# -----------------------------------Lista de compras-----------------------------------
def lista_de_compras():
    valor = 1

    venta_id = None
    venta_venta = f"No.1 - Prueba"
    venta_usuario = 'Francisco Javier'
    venta_ganancia = 0

    ahora = datetime.now()
    venta_fecha = ahora.strptime("%d-%m-%Y")
    venta_articulo = []
    
    while valor >= 1:
        try:
            opcion = int(input(f"{valor}.- "))
            venta_articulo.append(opcion)
            valor += 1
        except Exception as e:
            if opcion == 'GUARDAR':
                try:
                    venta_dao = VentaDAO()
                    venta = Venta(venta_id, venta_venta, venta_usuario, venta_ganancia, venta_fecha, venta_articulo)
                    venta_dao.guardar()

                    print("Venta guardada exitosamente")
                except Exception as e:
                    print("Error al guardar la venta")
                    print(e)
            else:
                if opcion == 'CANCELAR':
                    print("Venta cancelada")
                else:
                    if opcion == 'CONFIRMAR':
                        try:
                            venta_dao = VentaDAO()
                            venta = Venta(venta_id, venta_venta, venta_usuario, venta_ganancia, venta_fecha, venta_articulo)
                            venta_dao.confirmar()

                            print("Venta confirmada exitosamente")
                        except Exception as e:
                            print("Error al cofirmar la venta")
                            print(e)
# ---------------------------------Fin Lista de compras---------------------------------


def menu_articulos():
    print("\n================Productos================")
    print("\n--------------Menú de opciones--------------")
    print("1. Ver todos los artículos")
    print("2. Insertar un nuevo artículo")
    print("3. Modificar un artículo")
    print("4. Eliminar un articulo")
    opcion =  int(input("Selecciona una opción (1-4): "))

    match opcion:
        case 1:
            ver_articulos()
        case 2:
            insertar_articulo()
        case 3:
            modificar_articulo()
        case 4:
            eliminar_articulo()

def menu_categorias():
    print("\n================Categorías================")
    print("\n--------------Menú de opciones--------------")
    print("1. Ver todas las categorías")
    print("2. Insertar una nueva categoría")
    print("3. Modificar una categoría")
    print("4. Eliminar una categoría")
    opcion =  int(input("Selecciona una opción (1-4): "))

    match opcion:
        case 1:
            ver_categorias()
        case 2:
            insertar_categoria()
        case 3:
            modificar_categoria()
        case 4:
            eliminar_categoria()

def menu_proveedor():
    print("\n================Proveedores================")
    print("\n--------------Menú de opciones--------------")
    print("1. Ver todos los proveedores")
    print("2. Insertar un nuevo proveedor")
    print("3. Modificar un proveedor")
    print("4. Eliminar un proveedor")
    opcion =  int(input("Selecciona una opción (1-4): "))

    match opcion:
        case 1:
            ver_proveedores()
        case 2:
            insertar_proveedor()
        case 3:
            modificar_proveedor()
        case 4:
            eliminar_proveedor()

def menu_usuario():
    print("\n================Usuarios================")
    print("\n--------------Menú de opciones--------------")
    print("1. Ver todos los usuarios")
    print("2. Insertar un nuevo usuario")
    print("3. Modificar un usuario")
    print("4. Eliminar un usuario")
    opcion =  int(input("Selecciona una opción (1-4): "))

    match opcion:
        case 1:
            ver_usuarios()
        case 2:
            insertar_usuario()
        case 3:
            modificar_usuario()
        case 4:
            eliminar_usuario()
        
def punto_de_venta():
    print("\n================Punto de venta================")
    print("\n--------------Menú de opciones--------------")
    print("Núm - Agregar un producto a la lista")
    print("GUARDAR")
    print("CANCELAR")
    print("CONFIRMAR")

    print("\n--------------Lista de productos--------------")

    lista_de_compras()
    
# def main():
#     print("\n=============== La Vinata | Vinos y Licores ===============")
#     print("\nBienvenido a La Vinata, ¿qué deseas hacer?")
#     print("1 - Gestionar productos")
#     print("2 - Gestionar categorías")
#     print("3 - Gestionar proveedores")
#     print("4 - Gestionar usuarios")
#     print("5 - Gestionar ventas")
#     opcion = int(input("Selecciona en una opción: "))

#     match opcion:
#         case 1:
#             menu_articulos()
#         case 2:
#             menu_categorias()
#         case 3:
#             menu_proveedor()
#         case 4:
#             menu_usuario()
#         case 5:
#             punto_de_venta()

# if __name__ == "__main__":
#     main()

# Es obligatorio declarar assets_dir para que Flet pueda encontrar la carpeta donde se encuetra la imagen del Logotipo
ft.app(target = main_window, assets_dir = "assets")