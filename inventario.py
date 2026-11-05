# ==============================================================================
# TRABAJO PRÁCTICO INTEGRADOR: Sistema de Gestión de Inventario
# Materia: Fundamentos de Informática - UADE
# Módulo: inventario.py (Lógica de negocio y funciones del inventario)
#
# Estructura de la Matriz de Inventario (lista de listas):
# Cada fila representa un producto con 5 columnas fijas:
#   Columna 0: codigo (int, único)
#   Columna 1: nombre (str)
#   Columna 2: categoria (str)
#   Columna 3: precio (float, mayor o igual a 0)
#   Columna 4: stock (int, mayor o igual a 0)
# ==============================================================================


def cargar_csv(nombre_archivo):
    """
    Lee un archivo en formato CSV y devuelve la matriz con los productos cargados.
    Convierte cada campo al tipo de dato correspondiente.
    
    Parámetros:
        nombre_archivo (str): Ruta o nombre del archivo CSV a leer.
        
    Retorna:
        list: Matriz (lista de listas) con los productos cargados.
              Si el archivo no existe o ocurre un error, retorna una lista vacía.
    """
    matriz = []
    
    try:
        archivo = open(nombre_archivo, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
        
        # Verificamos que el archivo tenga al menos la cabecera y una fila de datos
        if len(lineas) > 1:
            # Empezamos desde el índice 1 para saltear la fila de encabezado
            for i in range(1, len(lineas)):
                linea = lineas[i].strip()
                
                # Ignoramos líneas vacías que puedan quedar al final del archivo
                if linea != "":
                    campos = linea.split(",")
                    
                    # Verificamos que tenga exactamente las 5 columnas requeridas
                    if len(campos) == 5:
                        codigo = int(campos[0].strip())
                        nombre = campos[1].strip()
                        categoria = campos[2].strip()
                        precio = float(campos[3].strip())
                        stock = int(campos[4].strip())
                        
                        producto = [codigo, nombre, categoria, precio, stock]
                        matriz.append(producto)
                        
    except FileNotFoundError:
        # Si el archivo no existe todavía, se inicializa como matriz vacía
        print(f"Aviso: El archivo '{nombre_archivo}' no fue encontrado. Se iniciará un inventario vacío.")
        matriz = []
        
    return matriz


def guardar_csv(matriz, nombre_archivo):
    """
    Guarda el contenido de la matriz de productos en un archivo CSV,
    incluyendo el encabezado obligatorio.
    
    Parámetros:
        matriz (list): Lista de listas con los datos de los productos.
        nombre_archivo (str): Ruta o nombre del archivo donde se guardará.
        
    Retorna:
        None
    """
    archivo = open(nombre_archivo, "w", encoding="utf-8")
    
    # Escribimos el encabezado obligatorio
    archivo.write("codigo,nombre,categoria,precio,stock\n")
    
    # Recorremos cada producto de la matriz y escribimos sus datos separados por comas
    for i in range(len(matriz)):
        producto = matriz[i]
        linea = f"{producto[0]},{producto[1]},{producto[2]},{producto[3]},{producto[4]}\n"
        archivo.write(linea)
        
    archivo.close()

def producto_valido(matriz, codigo, nombre, categoria, precio, stock):
    """
    Valida los datos de un producto según las reglas de negocio.
    
    Parámetros:
        matriz (list): Lista de listas con el inventario actual.
        codigo (int): Código numérico identificador único del producto.
        nombre (str): Nombre descriptivo del producto.
        categoria (str): Categoría a la que pertenece.
        precio (float): Precio unitario (debe ser mayor o igual a 0).
        stock (int): Cantidad en stock (debe ser mayor o igual a 0).
        
    Retorna:
        bool: True si todos los datos son válidos, False en caso contrario.
    """

    # Validamos que los datos tengan sentido comercial
    return codigo > 0 and nombre != "" and categoria != "" and precio >= 0 and stock >= 0 and not codigo_existente(matriz, codigo)

def codigo_existente(matriz, codigo):
    try:
        codigo_int = int(codigo)
    except (ValueError, TypeError):
        return False

    for i in range(len(matriz)):
        if matriz[i][0] == codigo_int:
            return True
    return False

def alta_producto(matriz, codigo, nombre, categoria, precio, stock):
    """
    Agrega un nuevo producto a la matriz de inventario previa validación de datos.
    Verifica que el código no exista previamente en la matriz.
    
    Parámetros:
        matriz (list): Lista de listas con el inventario actual.
        codigo (int): Código numérico identificador único del producto.
        nombre (str): Nombre descriptivo del producto.
        categoria (str): Categoría a la que pertenece.
        precio (float): Precio unitario (debe ser mayor o igual a 0).
        stock (int): Cantidad en stock (debe ser mayor o igual a 0).
        
    Retorna:
        bool: True si el producto fue agregado con éxito, False si ya existe
              o si alguno de los datos es inválido.
    """
    producto_agregado = False
    try:
        codigo_int = int(codigo)
        precio_float = float(precio)
        stock_int = int(stock)
        nombre_str = str(nombre).strip()
        categoria_str = str(categoria).strip()
    except (ValueError, TypeError):
        return False

    producto_valido_de_agregar = producto_valido(matriz, codigo_int, nombre_str, categoria_str, precio_float, stock_int) 

    if producto_valido_de_agregar:
        nuevo_producto = [codigo_int, nombre_str, categoria_str, precio_float, stock_int]
        matriz.append(nuevo_producto)

    return producto_valido_de_agregar


def baja_producto(matriz, codigo):
    """
    Elimina un producto de la matriz de inventario según su código.
    
    Parámetros:
        matriz (list): Lista de listas con el inventario.
        codigo (int): Código del producto que se desea eliminar.
        
    Retorna:
        bool: True si el producto existía y fue eliminado, False si no se encontró.
    """
    try:
        codigo_int = int(codigo)
    except (ValueError, TypeError):
        return False

    # Recorremos la matriz buscando la coincidencia manual del código
    for i in range(len(matriz)):
        if matriz[i][0] == codigo_int:
            del matriz[i]
            return True

    # Si se recorrió toda la matriz sin encontrar el código
    return False


def modificar_stock(matriz, codigo, cantidad):
    """
    Modifica el stock de un producto sumando la cantidad especificada
    (positiva para ingresos o negativa para egresos/ventas).
    Verifica que el producto exista y que el stock final no resulte negativo.
    
    Parámetros:
        matriz (list): Lista de listas con el inventario.
        codigo (int): Código del producto a modificar.
        cantidad (int): Valor a sumar al stock actual (puede ser negativo).
        
    Retorna:
        bool: True si se modificó correctamente el stock, False si el producto
              no existe o si el stock resultante quedaría menor a 0.
    """
    try:
        codigo_int = int(codigo)
        cantidad_int = int(cantidad)
    except (ValueError, TypeError):
        return False

    # Buscamos el producto en la matriz
    for i in range(len(matriz)):
        if matriz[i][0] == codigo_int:
            stock_actual = matriz[i][4]
            nuevo_stock = stock_actual + cantidad_int

            # El stock nunca puede quedar negativo
            if nuevo_stock < 0:
                return False

            matriz[i][4] = nuevo_stock
            return True

    # Producto no encontrado
    return False


# ==============================================================================
# SECCIÓN 1.4: MÉTODOS DE BÚSQUEDA (Clase 11)
# ==============================================================================

def busqueda_secuencial(matriz, codigo):
    """
    Busca un producto por su código recorriendo la matriz elemento por elemento.
    No requiere que los productos estén ordenados.
    
    Parámetros:
        matriz (list): Lista de listas con los productos.
        codigo (int): Código numérico a buscar.
        
    Retorna:
        tuple: (indice, comparaciones)
               indice es la posición en la matriz (o -1 si no existe),
               comparaciones es la cantidad de revisiones realizadas.
    """
    comparaciones = 0
    try:
        codigo_int = int(codigo)
    except (ValueError, TypeError):
        return -1, 0

    for i in range(len(matriz)):
        comparaciones += 1
        if matriz[i][0] == codigo_int:
            return i, comparaciones

    return -1, comparaciones


def busqueda_binaria(matriz, codigo):
    """
    Busca un producto por su código dividiendo el rango a la mitad en cada paso.
    Precondición: La matriz debe estar ordenada previamente por código (columna 0).
    
    Parámetros:
        matriz (list): Lista de listas ordenada por código.
        codigo (int): Código numérico a buscar.
        
    Retorna:
        tuple: (indice, comparaciones)
               indice es la posición encontrada (o -1 si no está),
               comparaciones es el número de iteraciones realizadas.
    """
    try:
        codigo_int = int(codigo)
    except (ValueError, TypeError):
        return -1, 0

    izq = 0
    der = len(matriz) - 1
    comparaciones = 0

    while izq <= der:
        medio = (izq + der) // 2
        comparaciones += 1

        if matriz[medio][0] == codigo_int:
            return medio, comparaciones
        elif matriz[medio][0] < codigo_int:
            izq = medio + 1
        else:
            der = medio - 1

    return -1, comparaciones


# ==============================================================================
# SECCIÓN 1.5: MÉTODOS DE ORDENAMIENTO (Clase 12)
# ==============================================================================

def ordenar_seleccion(matriz, columna):
    """
    Ordena la matriz de menor a mayor por la columna indicada usando el algoritmo de Selección.
    Busca el menor elemento en la parte desordenada y lo ubica al inicio.
    
    Parámetros:
        matriz (list): Lista de listas con los productos.
        columna (int): Índice de columna según la cual ordenar (0 a 4).
        
    Retorna:
        list: La matriz ordenada.
    """
    n = len(matriz)
    for i in range(n - 1):
        pos_minimo = i
        for j in range(i + 1, n):
            if matriz[j][columna] < matriz[pos_minimo][columna]:
                pos_minimo = j

        # Intercambiamos si encontramos uno menor
        if pos_minimo != i:
            aux = matriz[i]
            matriz[i] = matriz[pos_minimo]
            matriz[pos_minimo] = aux

    return matriz


def ordenar_burbuja(matriz, columna):
    """
    Ordena la matriz de menor a mayor por la columna indicada usando el algoritmo de Burbuja.
    Compara pares adyacentes y los intercambia si están desordenados.
    
    Parámetros:
        matriz (list): Lista de listas con los productos.
        columna (int): Índice de columna según la cual ordenar (0 a 4).
        
    Retorna:
        list: La matriz ordenada.
    """
    n = len(matriz)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if matriz[j][columna] > matriz[j + 1][columna]:
                aux = matriz[j]
                matriz[j] = matriz[j + 1]
                matriz[j + 1] = aux

    return matriz


def ordenar_insercion(matriz, columna):
    """
    Ordena la matriz de menor a mayor por la columna indicada usando el algoritmo de Inserción.
    Toma cada elemento y lo inserta en su posición adecuada entre los ya ordenados.
    
    Parámetros:
        matriz (list): Lista de listas con los productos.
        columna (int): Índice de columna según la cual ordenar (0 a 4).
        
    Retorna:
        list: La matriz ordenada.
    """
    n = len(matriz)
    for i in range(1, n):
        actual = matriz[i]
        j = i - 1
        while j >= 0 and matriz[j][columna] > actual[columna]:
            matriz[j + 1] = matriz[j]
            j -= 1
        matriz[j + 1] = actual

    return matriz


# ==============================================================================
# SECCIÓN 1.6: REPORTES DEL INVENTARIO
# ==============================================================================

def stock_bajo(matriz, umbral):
    """
    Devuelve una lista con los productos cuyo stock es estrictamente menor al umbral.
    
    Parámetros:
        matriz (list): Lista de listas con los productos.
        umbral (int): Límite numérico de stock.
        
    Retorna:
        list: Subconjunto de filas de productos con stock < umbral.
    """
    resultado = []
    try:
        umbral_int = int(umbral)
    except (ValueError, TypeError):
        return resultado

    for i in range(len(matriz)):
        if matriz[i][4] < umbral_int:
            resultado.append(matriz[i])

    return resultado


def valor_total(matriz):
    """
    Calcula y devuelve la suma acumulada de precio * stock de todos los productos.
    
    Parámetros:
        matriz (list): Lista de listas con los productos.
        
    Retorna:
        float: Valor monetario total del inventario.
    """
    total = 0.0
    for i in range(len(matriz)):
        precio = matriz[i][3]
        stock = matriz[i][4]
        total += precio * stock

    return total


def producto_mas_caro(matriz):
    """
    Busca manualmente el producto con el mayor precio unitario (sin usar max()).
    
    Parámetros:
        matriz (list): Lista de listas con los productos.
        
    Retorna:
        list o None: Fila del producto más caro, o None si la matriz está vacía.
    """
    if len(matriz) == 0:
        return None

    mas_caro = matriz[0]
    for i in range(1, len(matriz)):
        if matriz[i][3] > mas_caro[3]:
            mas_caro = matriz[i]

    return mas_caro


def producto_mas_barato(matriz):
    """
    Busca manualmente el producto con el menor precio unitario (sin usar min()).
    
    Parámetros:
        matriz (list): Lista de listas con los productos.
        
    Retorna:
        list o None: Fila del producto más barato, o None si la matriz está vacía.
    """
    if len(matriz) == 0:
        return None

    mas_barato = matriz[0]
    for i in range(1, len(matriz)):
        if matriz[i][3] < mas_barato[3]:
            mas_barato = matriz[i]

    return mas_barato

