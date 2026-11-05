# GUÍA TÉCNICA DE ESTUDIO Y DEFENSA DEL TP
### Fundamentos de Informática — UADE (FAIN)
**Objetivo de esta guía:** Prepararte para explicar, justificar y modificar en vivo cualquier parte del código durante el **Segundo Parcial en computadora** y el **Coloquio Final individual**.

---

## 1. La Estructura de Datos: Matrices (Lista de Listas)

### ¿Qué es la matriz en este proyecto?
Una matriz en Python no es un tipo de dato especial, sino una **lista donde cada uno de sus elementos es otra lista**.
```python
matriz = [
    [101, "Yerba Mate 1kg", "Almacén", 3500.0, 15],  # Fila 0
    [102, "Detergente 750ml", "Limpieza", 1850.5, 8]  # Fila 1
]
```

### ¿Cómo se accede a la información?
Se utilizan dos índices entre corchetes: `matriz[fila][columna]`
- `matriz[0]` devuelve la fila completa del primer producto: `[101, "Yerba Mate 1kg", "Almacén", 3500.0, 15]`.
- `matriz[0][1]` devuelve el **nombre** del primer producto: `"Yerba Mate 1kg"`.
- `matriz[i][0]` representa siempre el **código** del producto en la fila `i`.
- `matriz[i][3]` representa el **precio**.
- `matriz[i][4]` representa el **stock**.

### Concepto Clave: Mutabilidad y Paso por Referencia
- **Pregunta típica de examen:** *¿Por qué cuando llamamos a `alta_producto(matriz, ...)` o `ordenar_burbuja(matriz, ...)` no hace falta poner `matriz = alta_producto(matriz, ...)` en el programa principal?*
- **Respuesta:** En Python, las listas son **mutables** y los argumentos compuestos se pasan por **referencia** (se pasa la dirección de memoria de la lista). Cualquier modificación realizada dentro de la función (como `.append()`, `del` o reordenar elementos) altera directamente la lista original que reside en la memoria.

---

## 2. Algoritmos de Búsqueda (Clase 11)

### A. Búsqueda Secuencial (Lineal)
- **Idea central:** Se recorre la lista elemento por elemento desde el índice `0` hasta el final mediante un bucle `for`.
- **Ventaja:** Funciona **siempre**, sin importar si la lista está desordenada o cómo fue cargada.
- **Complejidad:** $O(n)$.
  - *Mejor caso:* 1 comparación (si el producto buscado está en la primera fila).
  - *Peor caso:* $n$ comparaciones (si el producto está al final de todo o no existe en la lista).
- **Código conceptual:**
  ```python
  def busqueda_secuencial(matriz, codigo):
      comparaciones = 0
      for i in range(len(matriz)):
          comparaciones += 1
          if matriz[i][0] == codigo:
              return i, comparaciones
      return -1, comparaciones
  ```

### B. Búsqueda Binaria (Dicotómica)
- **Idea central:** Divide el espacio de búsqueda a la mitad en cada paso. Compara el valor del elemento central con el valor buscado.
- **Precondición Obligatoria:** **La matriz DEBE estar ordenada previamente por código**. Si la lista está desordenada, la búsqueda binaria fallará porque puede descartar la mitad donde realmente se encuentra el elemento.
- **Funcionamiento con punteros:**
  - `izq = 0` (inicio del rango)
  - `der = len(matriz) - 1` (fin del rango)
  - `medio = (izq + der) // 2` (posición central entera)
  - Si `matriz[medio][0] == codigo`: ¡Encontrado!
  - Si `matriz[medio][0] < codigo`: El buscado es más grande; descartamos la mitad izquierda haciendo `izq = medio + 1`.
  - Si `matriz[medio][0] > codigo`: El buscado es más chico; descartamos la mitad derecha haciendo `der = medio - 1`.
- **Complejidad:** $O(\log_2 n)$.
  - Crece de manera extremadamente lenta. Para 1.000 elementos solo requiere unas 10 comparaciones como máximo; para 1.000.000 de elementos solo 20 comparaciones.

---

## 3. Algoritmos de Ordenamiento (Clase 12)

Todos los algoritmos implementados trabajan de menor a mayor y tienen complejidad cuadrática $O(n^2)$, pero operan de formas distintas:

### 1. Método de Selección (`ordenar_seleccion`)
- **Cómo trabaja:** Recorre la matriz y en cada posición `i` busca cuál es el elemento mínimo de toda la parte restante (desde `i+1` hasta el final). Al hallarlo, lo intercambia con la posición `i`.
- **Técnica del intercambio manual (Swap):**
  ```python
  aux = matriz[i]
  matriz[i] = matriz[pos_minimo]
  matriz[pos_minimo] = aux
  ```
- **Ventaja:** Realiza muy pocos intercambios de memoria (a lo sumo un swap por pasada).

### 2. Método de Burbuja (`ordenar_burbuja`)
- **Cómo trabaja:** Compara pares vecinos adyacentes (`matriz[j]` con `matriz[j+1]`). Si el de la izquierda es mayor que el de la derecha, los intercambia.
- Al final de la primera pasada, el elemento más grande queda garantizado en la última posición (como una burbuja que sube).
- En pasadas sucesivas se achica el límite: `for j in range(n - 1 - i)`.

### 3. Método de Inserción (`ordenar_insercion`)
- **Cómo trabaja:** Similar a cómo una persona ordena un mazo de cartas en la mano. Toma un elemento `actual = matriz[i]` y lo compara hacia atrás contra los elementos ya ordenados (`while j >= 0 and matriz[j][columna] > actual[columna]`). Va desplazando los mayores hacia la derecha y finalmente "inserta" el valor en el hueco libre.
- **Ventaja práctica:** Es el más veloz si la lista ya está casi ordenada.

---

## 4. Persistencia y Archivos CSV

### ¿Cómo lee `cargar_csv`?
```python
archivo = open(nombre_archivo, "r", encoding="utf-8")
lineas = archivo.readlines()
archivo.close()
```
- `readlines()` devuelve una lista de strings con cada fila del archivo.
- Omitimos el encabezado empezando desde `1`: `for i in range(1, len(lineas)):`.
- `.strip()` limpia saltos de línea (`\n`) y espacios en los extremos.
- `.split(",")` separa la cadena por comas y devuelve una lista de textos.
- Convertimos manualmente cada valor: `int(campos[0])`, `float(campos[3])`, etc.

### ¿Cómo escribe `guardar_csv`?
```python
archivo = open(nombre_archivo, "w", encoding="utf-8")
archivo.write("codigo,nombre,categoria,precio,stock\n")
for i in range(len(matriz)):
    p = matriz[i]
    archivo.write(f"{p[0]},{p[1]},{p[2]},{p[3]},{p[4]}\n")
archivo.close()
```
- El modo `"w"` (write) sobreescribe el archivo limpiamente con el nuevo estado del inventario.

---

## 5. Búsqueda Manual de Extremos (Máximo y Mínimo sin funciones prohibidas)

- **Regla de oro:** No se pueden usar `min()` ni `max()`.
- **Estrategia algorítmica obligatoria:**
  1. Suponer que el primer elemento es el extremo: `mas_caro = matriz[0]`.
  2. Recorrer desde la posición `1` con un bucle:
     ```python
     for i in range(1, len(matriz)):
         if matriz[i][3] > mas_caro[3]:
             mas_caro = matriz[i]
     return mas_caro
     ```

---

## 6. Preguntas y Modificaciones Típicas en el Coloquio / Parcial

### Pregunta 1: *"¿Cómo hacés para que ordene de mayor a menor (descendente)?"*
- **Respuesta:** Solo cambiás el operador de comparación:
  - En Burbuja: cambiar `>` por `<` (`if matriz[j][columna] < matriz[j + 1][columna]`).
  - En Selección: buscar el mayor en lugar del menor (`matriz[j][columna] > matriz[pos_maximo][columna]`).
  - En Inserción: desplazar si es menor (`matriz[j][columna] < actual[columna]`).

### Pregunta 2: *"Escribí una función que cuente cuántos productos hay de la categoría 'Limpieza'"*
- **Respuesta en vivo:**
  ```python
  def contar_categoria(matriz, categoria_buscada):
      contador = 0
      for i in range(len(matriz)):
          if matriz[i][2].lower() == categoria_buscada.lower():
              contador += 1
      return contador
  ```

### Pregunta 3: *"¿Por qué usamos `try/except` al pedir datos al usuario?"*
- **Respuesta:** Si el usuario ingresa una letra cuando el programa espera un número entero (por ejemplo `"abc"` en el precio o código), la función `int("abc")` arrojaría una excepción `ValueError` y el programa se cerraría abruptamente. Con `try/except` capturamos el error a tiempo, mostramos un mensaje amigable y el programa continúa funcionando sin colapsar.
