# ==============================================================================
# TRABAJO PRÁCTICO INTEGRADOR: Sistema de Gestión de Inventario
# Materia: Fundamentos de Informática - UADE
# Módulo: main.py (Interfaz de usuario por consola y flujo principal)
# ==============================================================================

import inventario

NOMBRE_ARCHIVO = "inventario.csv"


def imprimir_linea():
    """Imprime una línea divisoria para dar prolijidad a la consola."""
    print("-" * 65)


def mostrar_matriz(matriz, titulo="LISTADO DE INVENTARIO"):
    """
    Muestra la matriz de productos en un formato de tabla legible en consola.
    
    Parámetros:
        matriz (list): Lista de listas con los productos.
        titulo (str): Encabezado visual para la tabla.
    """
    imprimir_linea()
    print(f" {titulo} (Total: {len(matriz)} productos)")
    imprimir_linea()
    
    if len(matriz) == 0:
        print("El inventario está vacío actualmente.")
        imprimir_linea()
        return

    # Encabezados de columnas con ancho fijo
    print(f"{'CÓDIGO':<8} | {'NOMBRE':<25} | {'CATEGORÍA':<12} | {'PRECIO':>9} | {'STOCK':>6}")
    imprimir_linea()
    
    # Recorremos cada fila de la matriz e imprimimos sus 5 columnas
    for i in range(len(matriz)):
        p = matriz[i]
        codigo = p[0]
        nombre = p[1]
        categoria = p[2]
        precio = f"${p[3]:.2f}"
        stock = p[4]
        print(f"{codigo:<8} | {nombre:<25} | {categoria:<12} | {precio:>9} | {stock:>6}")
        
    imprimir_linea()


def mostrar_producto(producto):
    """Muestra los datos detallados de una única fila de producto."""
    print(f"  - Código:    {producto[0]}")
    print(f"  - Nombre:    {producto[1]}")
    print(f"  - Categoría: {producto[2]}")
    print(f"  - Precio:    ${producto[3]:.2f}")
    print(f"  - Stock:     {producto[4]} unidades")


# ==============================================================================
# SUB-MENÚS Y ACCIONES DEL USUARIO
# ==============================================================================

def accion_alta(matriz):
    """Solicita los datos al usuario y da de alta un nuevo producto."""
    print("\n--- ALTA DE NUEVO PRODUCTO ---")
    try:
        codigo = int(input("Ingrese código numérico (positivo y único): "))
        nombre = input("Ingrese nombre del producto: ").strip()
        categoria = input("Ingrese categoría: ").strip()
        precio = float(input("Ingrese precio unitario (>= 0): "))
        stock = int(input("Ingrese stock inicial (>= 0): "))
    except ValueError:
        print("Error: Ingrese valores numéricos válidos para código, precio y stock.")
        return

    # Invocamos la función de inventario.py
    exito = inventario.alta_producto(matriz, codigo, nombre, categoria, precio, stock)
    if exito:
        print(f"[OK] Producto '{nombre}' (Código: {codigo}) agregado con éxito.")
    else:
        print("[ERROR] No se pudo agregar. Verifique que el código no esté repetido y los datos sean válidos.")


def accion_baja(matriz):
    """Solicita el código y elimina el producto correspondiente."""
    print("\n--- BAJA DE PRODUCTO ---")
    try:
        codigo = int(input("Ingrese el código del producto a eliminar: "))
    except ValueError:
        print("Error: El código debe ser un número entero.")
        return

    exito = inventario.baja_producto(matriz, codigo)
    if exito:
        print(f"[OK] Producto con código {codigo} eliminado correctamente.")
    else:
        print(f"[ERROR] No se encontró ningún producto con el código {codigo}.")


def accion_modificar_stock(matriz):
    """Permite ingresar o egresar stock de un producto existente."""
    print("\n--- MODIFICAR STOCK ---")
    try:
        codigo = int(input("Ingrese el código del producto: "))
        cantidad = int(input("Ingrese cantidad a sumar (positivo) o restar (negativo): "))
    except ValueError:
        print("Error: Código y cantidad deben ser valores numéricos enteros.")
        return

    exito = inventario.modificar_stock(matriz, codigo, cantidad)
    if exito:
        print(f"[OK] Stock actualizado con éxito para el código {codigo}.")
    else:
        print("[ERROR] No se pudo actualizar el stock (producto inexistente o stock resultante negativo).")


def accion_buscar(matriz):
    """
    Busca un producto por código usando ambos métodos (secuencial y binario),
    e informa las comparaciones de cada uno para contrastar rendimientos.
    """
    print("\n--- BÚSQUEDA DE PRODUCTO POR CÓDIGO ---")
    try:
        codigo = int(input("Ingrese el código a buscar: "))
    except ValueError:
        print("Error: El código debe ser numérico.")
        return

    # 1. Búsqueda Secuencial (funciona en cualquier orden)
    pos_sec, pasos_sec = inventario.busqueda_secuencial(matriz, codigo)

    # 2. Búsqueda Binaria (requiere que la matriz esté ordenada por código)
    # Ordenamos la matriz por código (columna 0) usando burbuja para garantizar la precondición
    inventario.ordenar_burbuja(matriz, 0)
    pos_bin, pasos_bin = inventario.busqueda_binaria(matriz, codigo)

    imprimir_linea()
    if pos_sec != -1:
        print("[OK] PRODUCTO ENCONTRADO:")
        mostrar_producto(matriz[pos_bin])
    else:
        print(f"[INFO] El producto con código {codigo} NO existe en el inventario.")

    print("\nComparación de algoritmos (Clase 11):")
    print(f"  * Búsqueda Secuencial: {pasos_sec} comparaciones realizadas.")
    print(f"  * Búsqueda Binaria:    {pasos_bin} comparaciones realizadas.")
    imprimir_linea()


def accion_ordenar(matriz):
    """Permite al usuario elegir qué columna ordenar y qué método algorítmico aplicar."""
    print("\n--- ORDENAR INVENTARIO ---")
    print("Columnas disponibles:")
    print("1. Nombre (Alfabético)")
    print("2. Precio")
    print("3. Stock")
    print("4. Código")
    
    opc_col = input("Elija una columna (1-4): ").strip()
    columna_map = {"1": 1, "2": 3, "3": 4, "4": 0}
    
    if opc_col not in columna_map:
        print("Opción de columna inválida.")
        return
        
    columna_elegida = columna_map[opc_col]

    print("\nMétodos de ordenamiento disponibles:")
    print("1. Método de Selección")
    print("2. Método de Burbuja")
    print("3. Método de Inserción")
    opc_metodo = input("Elija un método (1-3): ").strip()

    if opc_metodo == "1":
        inventario.ordenar_seleccion(matriz, columna_elegida)
        metodo_nombre = "Selección"
    elif opc_metodo == "2":
        inventario.ordenar_burbuja(matriz, columna_elegida)
        metodo_nombre = "Burbuja"
    elif opc_metodo == "3":
        inventario.ordenar_insercion(matriz, columna_elegida)
        metodo_nombre = "Inserción"
    else:
        print("Método inválido.")
        return

    print(f"\n[OK] Matriz ordenada correctamente mediante '{metodo_nombre}'.")
    mostrar_matriz(matriz, f"INVENTARIO ORDENADO POR {metodo_nombre.upper()}")


def accion_reportes(matriz):
    """Muestra el submenú de análisis y reportes estadísticos del inventario."""
    print("\n--- REPORTES Y ANÁLISIS DE INVENTARIO ---")
    print("1. Filtrar productos con stock bajo")
    print("2. Ver valor total del inventario")
    print("3. Ver producto más caro y más barato")
    opcion = input("Seleccione un reporte (1-3): ").strip()

    if opcion == "1":
        try:
            umbral = int(input("Ingrese umbral de stock mínimo: "))
        except ValueError:
            print("Error: El umbral debe ser un número entero.")
            return

        productos_bajos = inventario.stock_bajo(matriz, umbral)
        mostrar_matriz(productos_bajos, f"PRODUCTOS CON STOCK MENOR A {umbral}")

    elif opcion == "2":
        total = inventario.valor_total(matriz)
        imprimir_linea()
        print(f"VALOR MONETARIO TOTAL DEL INVENTARIO: ${total:,.2f}")
        imprimir_linea()

    elif opcion == "3":
        mas_caro = inventario.producto_mas_caro(matriz)
        mas_barato = inventario.producto_mas_barato(matriz)

        imprimir_linea()
        if mas_caro is not None:
            print("[PRODUCTO MÁS CARO]")
            mostrar_producto(mas_caro)
        else:
            print("El inventario está vacío.")

        print()
        if mas_barato is not None:
            print("[PRODUCTO MÁS BARATO]")
            mostrar_producto(mas_barato)
        imprimir_linea()
    else:
        print("Opción de reporte no válida.")


# ==============================================================================
# BUCLE PRINCIPAL DEL PROGRAMA
# ==============================================================================

def main():
    """Función principal de inicio: carga el inventario y gestiona el menú."""
    print("=================================================================")
    print("  SISTEMA DE GESTIÓN DE INVENTARIO - FUNDAMENTOS DE INFORMÁTICA  ")
    print("=================================================================")
    
    # Carga inicial obligatoria desde CSV
    matriz = inventario.cargar_csv(NOMBRE_ARCHIVO)
    print(f"Carga inicial completada: {len(matriz)} productos leídos desde '{NOMBRE_ARCHIVO}'.")

    # Ciclo repetitivo del menú hasta que el usuario decida salir
    ejecutando = True
    while ejecutando:
        print("\n" + "=" * 45)
        print("              MENÚ PRINCIPAL                 ")
        print("=" * 45)
        print("1. Mostrar inventario completo")
        print("2. Dar de alta un producto")
        print("3. Dar de baja un producto")
        print("4. Modificar stock de un producto")
        print("5. Buscar producto por código (Secuencial vs Binaria)")
        print("6. Ordenar inventario (Selección, Burbuja, Inserción)")
        print("7. Reportes y análisis de inventario")
        print("8. Guardar cambios en el archivo CSV")
        print("9. Guardar y Salir")
        print("=" * 45)

        opcion = input("Seleccione una opción (1-9): ").strip()

        if opcion == "1":
            mostrar_matriz(matriz)
        elif opcion == "2":
            accion_alta(matriz)
        elif opcion == "3":
            accion_baja(matriz)
        elif opcion == "4":
            accion_modificar_stock(matriz)
        elif opcion == "5":
            accion_buscar(matriz)
        elif opcion == "6":
            accion_ordenar(matriz)
        elif opcion == "7":
            accion_reportes(matriz)
        elif opcion == "8":
            inventario.guardar_csv(matriz, NOMBRE_ARCHIVO)
            print(f"[OK] Cambios guardados correctamente en '{NOMBRE_ARCHIVO}'.")
        elif opcion == "9":
            inventario.guardar_csv(matriz, NOMBRE_ARCHIVO)
            print(f"\nGuardando datos en '{NOMBRE_ARCHIVO}'...")
            print("¡Gracias por utilizar el Sistema de Gestión de Inventario!")
            ejecutando = False
        else:
            print("Opción inválida. Por favor seleccione un número del 1 al 9.")


if __name__ == "__main__":
    main()
