from dao.articulo_dao import ArticuloDAO
from models.articulo import Articulo
from models.articulo import Articulo_eliminar

def insertar_articulo():
    articulo_id = None
    articulo_articulo = input("\nEscribe el nombre del artículo: ")
    
    print("\n-----------Categorías----------")
    print("1 - Tinto")
    print("2 - Blanco")
    print("3 - Rosado")
    print("4 - Joven")
    print("5 - Extra secos")
    print("6 - Secos")
    print("7 - Dulces ")
    print("8 - Finos") 
         
    articulo_categoria = int(input("\nEscribe el número correspondiente a la categoria: "))
    articulo_imagen = input("Escribe el nombre de la imagen: ")
    articulo_precio = float(input("Escribe el precio del producto:"))
    articulo_stock = int(input("Escribe el stock: "))
    articulo_proveedor = int(input("Escribe el ID del proveedor: "))

    try:
        articulo_dao = ArticuloDAO()
        articulo = Articulo(articulo_id ,articulo_articulo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor)
        articulo_dao.insertar(articulo)
        print("Artículo agregado exitosamente")
    except Exception as e:
        print("Error al insertar un artículo nuevo")
        print(e)

def ver_articulos():
    try:
        articulo_dao = ArticuloDAO()

        articulos = articulo_dao.obtener_todos()

        print("\n=== Articulos en la vinateria ===")

        if len(articulos) == 0:
            print("No hay articulos registrados.")
        else:
            for articulo in articulos:
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
                print(
                    f"ID: {articulo.articulo_id}   "
                    f"Nombre: {articulo.articulo_articulo}   "
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
        articulo_id = int(input("Introduce el ID del articulo a modificar: "))
        id_modificado = str(articulo_id)

        articulo_articulo = input("\nEscribe el nuevo nombre del producto: ")
        articulo_categoria = int(input("Escribe la nueva categoria del producto: "))
        articulo_imagen = input("Escribe la nueva imagen del producto: ")
        articulo_precio = float(input("Escribe el nuevo precio del producto: "))
        articulo_stock = int(input("Escribe el nuevo stock del producto: "))
        articulo_proveedor = int(input("Escribe el nuevo ID del proveedor: "))

        articulo = Articulo(articulo_id, articulo_articulo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor)
        articulo_dao.actualizar(articulo)    

        print("\nProducto "+id_modificado+" modificado exitosamente")
    except Exception as e:
        print("Error al modificar el producto")
        print(e)


def eliminar_articulo():
    try:
        articulo_dao = ArticuloDAO()

        articulos = articulo_dao.obtener_todos()

        print("\n=== Articulos en la vinateria ===")

        if len(articulos) == 0:
            print("No hay articulos registrados.")
        else:
            for articulo in articulos:
                print("---------------------------------------------------------------------------------------------------------------------")
                print(
                    f"ID: {articulo.articulo_id}   "
                    f"Nombre: {articulo.articulo_articulo}   "
                    f"Categoría: {articulo.articulo_categoria}   "
                    f"Imagen: {articulo.articulo_imagen}   "
                    f"Precio: {articulo.articulo_precio}   "
                    f"Stock: {articulo.articulo_stock}    "
                    f"Proveedor: {articulo.articulo_proveedor}"
                )
        print("---------------------------------------------------------------------------------------------------------------------")
        print("\n Conexión exitosa a la base de datos")

        articulo_id = int(input("\n\nEscribe el ID del artículo: "))
        id_eliminado = str(articulo_id)

        try:
            articulo_dao = ArticuloDAO()
            articulo = Articulo_eliminar(articulo_id)
            articulo_dao.eliminar(articulo)

            print("Artículo "+id_eliminado+" eliminado exitosamente")
        except Exception as e:
            print("Error al eliminar el articulo "+id_eliminado)
            print(e)

    except Exception as e:
        print("Error: ")
        print(e)

def main():
    print("\n=============== La Vinata | Vinos y Licores ===============")
    print("\nMenú de opciones")
    print("1. Ver todos los artículos")
    print("2. Insertar un nuevo artículo")
    print("3. Modificar un artículo")
    print("4. Eliminar un articulo")
    opcion =  int(input("Selecciones una opción (1-4): "))

    match opcion:
        case 1:
            ver_articulos()
        case 2:
            insertar_articulo()
        case 3:
            modificar_articulo()
        case 4:
            eliminar_articulo()

if __name__ == "__main__":
    main()