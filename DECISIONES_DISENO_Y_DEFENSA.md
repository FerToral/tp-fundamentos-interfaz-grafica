# ANÁLISIS DE LA CONSIGNA, DECISIONES DE DISEÑO Y GUÍA DE DEFENSA
### TP Integrador: Sistema de Gestión de Inventario
**Materia:** Fundamentos de Informática — UADE (FAIN)  
**Propósito:** Respuestas fundamentadas y técnicas ante las preguntas del docente: *«¿Por qué seguiste este camino?»* y *«¿Qué hiciste aquí?»*.

---

## 1. Mapa de Ambigüedades y Decisiones Técnicas

A continuación se analizan los puntos de la consigna que tenían interpretaciones libres, cómo se resolvieron y el argumento técnico para justificar cada elección:

---

### Decisión 1: Precondición de la Búsqueda Binaria
* **Lo que dice la consigna:**  
  `busqueda_binaria(matriz, codigo)`: *«Igual que la anterior, sobre la matriz ordenada por código»*. Y en funcionalidades: *«Búsqueda por código con los dos métodos, informando cuántas comparaciones hizo cada uno para poder compararlos»*.
* **La ambigüedad:**  
  ¿La función `busqueda_binaria` debe ordenar la matriz por su cuenta si le llega desordenada, o debe asumir que ya viene ordenada?
* **El camino elegido:**  
  La función asume que la matriz ya viene ordenada como **precondición**, tal como se enseña en la teoría algorítmica (Clase 11). Quien garantiza el orden es el llamador (`main.py` o `gui.py`), invocando previamente a `ordenar_burbuja(matriz, 0)`.
* **Cómo defenderlo ante el docente:**  
  > *«Elegí no ordenar dentro de `busqueda_binaria` para respetar el **Principio de Responsabilidad Única**. La responsabilidad de la búsqueda binaria es solo buscar en $O(\log n)$. Si ordenara adentro, el algoritmo pasaría a costar $O(n^2)$ debido al ordenamiento, perdiendo todo el sentido de la eficiencia comparativa frente a la búsqueda secuencial. Quien consume la función (`main.py` o `gui.py`) tiene la responsabilidad de suministrar la matriz ordenada por la clave de búsqueda»*.

---

### Decisión 2: Ordenamiento *In-Place* (En memoria original) vs. Nueva Copia
* **Lo que dice la consigna:**  
  *«Ordenan la matriz de menor a mayor según la columna indicada y la devuelven»*.
* **La ambigüedad:**  
  La frase *«y la devuelven»* puede interpretarse como devolver una lista nueva (`return matriz_nueva`) o mutar la original y devolver su referencia (`return matriz`).
* **El camino elegido:**  
  Se implementó el ordenamiento **in-place** (sobre la misma matriz) y al final se retorna la misma lista (`return matriz`).
* **Cómo defenderlo ante el docente:**  
  > *«En Fundamentos de Informática aprendimos que las listas en Python son objetos mutables que se pasan por referencia. Hacer una copia profunda (`deepcopy`) de toda la matriz en cada ordenamiento duplicaría innecesariamente el consumo de memoria RAM. Ordenar in-place es el estándar de eficiencia en algoritmos clásicos (como hace `.sort()` internamente), y el hecho de retornar la misma matriz permite que el llamador pueda encadenar operaciones si lo desea»*.

---

### Decisión 3: Implementación de los TRES Métodos de Ordenamiento
* **Lo que dice la consigna:**  
  *«Implementar al menos dos de las tres»*.
* **La ambigüedad / Libertad:**  
  El enunciado permitía elegir solo dos métodos (por ejemplo, Selección y Burbuja).
* **El camino elegido:**  
  Implementamos los **tres métodos** (`ordenar_seleccion`, `ordenar_burbuja`, `ordenar_insercion`).
* **Cómo defenderlo ante el docente:**  
  > *«Decidimos implementar los tres métodos para poder realizar un análisis comparativo real en el informe. Gracias a esto pudimos justificar empíricamente que **Inserción** es el algoritmo más conveniente en un sistema comercial real, ya que cuando ingresa un nuevo producto al final de un catálogo que ya está ordenado, Inserción solo realiza pasadas proporcionales a $O(n)$ para ubicarlo en su lugar, mientras que Selección y Burbuja realizan comparaciones redundantes»*.

---

### Decisión 4: Reglas de Negocio en `modificar_stock` y el Stock Cero
* **Lo que dice la consigna:**  
  *«Suma la cantidad (positiva o negativa) al stock. Devuelve False si el producto no existe o si el stock quedaría negativo»*.
* **La ambigüedad:**  
  ¿Qué ocurre si el stock final queda exactamente en 0?
* **El camino elegido:**  
  El stock igual a 0 **se permite** (`nuevo_stock >= 0`). Solo se rechaza si `nuevo_stock < 0`.
* **Cómo defenderlo ante el docente:**  
  > *«Desde el punto de vista del negocio de un comercio, tener stock 0 significa 'producto momentáneamente agotado', lo cual es una situación cotidiana válida. Lo que es físicamente imposible y causaría una inconsistencia contable es tener un stock negativo (deuda de mercadería física). Por eso validamos estrictamente `nuevo_stock < 0` para rechazar la operación»*.

---

### Decisión 5: Búsqueda Manual de Extremos (`mas_caro` y `mas_barato`) y Empates
* **Lo que dice la consigna:**  
  *«Devuelven la fila del producto correspondiente»*.
* **La ambigüedad:**  
  No especifica qué hacer si el inventario está vacío, ni cómo resolver empates si dos productos tienen el mismo precio máximo.
* **El camino elegido:**  
  - Si la matriz está vacía (`len(matriz) == 0`), retorna de forma segura `None`.
  - Si hay productos con precios empatados, retorna el primero que aparece en el orden actual del catálogo (debido a la comparación estricta `>`).
* **Cómo defenderlo ante el docente:**  
  > *«Para cumplir la restricción técnica de no usar las funciones prohibidas `max()` ni `min()`, aplicamos el algoritmo clásico: inicializamos una variable puntero con la primera fila `matriz[0]` y recorremos desde el índice `1` con un bucle `for`. Si la matriz estuviera vacía, acceder a `matriz[0]` provocaría un error `IndexError`; por eso agregamos la guarda defensiva `if len(matriz) == 0: return None`. Ante un empate, el comparador estricto conserva el primer registro hallado, garantizando un comportamiento determinista»*.

---

### Decisión 6: Eliminación en `baja_producto` sin Funciones Prohibidas
* **Lo que dice la consigna:**  
  *«Elimina el producto. Devuelve True si lo eliminó, False si no existe»*.
* **La ambigüedad:**  
  En Python existe el método `matriz.remove(...)` o buscar el índice con `matriz.index(...)`, pero el uso de `index()` está explícitamente prohibido por la cátedra.
* **El camino elegido:**  
  Recorremos con `for i in range(len(matriz)):` comparando `matriz[i][0] == codigo`. Al encontrarlo, eliminamos la posición con la instrucción elemental `del matriz[i]` y cortamos inmediatamente con `return True`.
* **Cómo defenderlo ante el docente:**  
  > *«No utilizamos `matriz.index()` ni el operador `in` porque forman parte de las funciones prohibidas por la consigna. En su lugar, programamos el algoritmo a mano: recorremos fila por fila por índice entero y, en cuanto encontramos la coincidencia del código primario, ejecutamos `del matriz[i]` y retornamos inmediatamente para no seguir iterando innecesariamente»*.

---

### Decisión 7: Desacoplamiento Arquitectónico (Consola vs. Tkinter vs. Lógica)
* **Lo que dice la consigna:**  
  Menú de texto obligatorio por consola y, en los desafíos opcionales, una *«interfaz gráfica simple con tkinter»*.
* **La ambigüedad:**  
  Muchos alumnos cometen el error de meter toda la lógica adentro de los botones de Tkinter o adentro de los `print()` de la consola.
* **El camino elegido:**  
  Separación en tres capas independientes:
  1. **Lógica de Negocio Pura ([inventario.py](file:///c:/Users/Fernando%20Toralez/Documents/UADE_Ing_en_Informatica/Fundamentos%20de%20Informática/TP%20-%20Interfaz%20gráfica/inventario.py)):** No tiene ningún `print()` ni ningún `import tkinter`. Solo recibe datos por parámetro y retorna valores.
  2. **Interfaz de Consola ([main.py](file:///c:/Users/Fernando%20Toralez/Documents/UADE_Ing_en_Informatica/Fundamentos%20de%20Informática/TP%20-%20Interfaz%20gráfica/main.py)):** Se encarga de pedir datos por teclado y mostrar menús de texto.
  3. **Interfaz Gráfica ([gui.py](file:///c:/Users/Fernando%20Toralez/Documents/UADE_Ing_en_Informatica/Fundamentos%20de%20Informática/TP%20-%20Interfaz%20gráfica/gui.py)):** Se encarga de las ventanas visuales.
* **Cómo defenderlo ante el docente:**  
  > *«Diseñamos el sistema bajo el principio de **alta cohesión y bajo acoplamiento**. `inventario.py` es completamente agnóstico a la interfaz: no sabe si se está usando desde una terminal de texto, desde una ventana gráfica o si lo está testeando un script automatizado como `test_casos_borde.py`. Esto permitió que tanto el menú obligatorio de consola como la interfaz de Tkinter compartan exactamente las mismas funciones sin duplicar ni una sola línea de lógica»*.

---

## 2. Simulador de Preguntas Rápidas del Docente («Fuego Cruzado»)

### P: *«¿Qué pasa si en el CSV hay una línea vacía al final?»*
**R:** En `cargar_csv`, al iterar sobre las líneas leídas hacemos `linea = lineas[i].strip()`. Si `linea == ""`, la ignoramos mediante un condicional. Además, validamos `if len(campos) == 5:` antes de hacer el casting para evitar errores de índice.

### P: *«¿Por qué en la búsqueda secuencial retornás una tupla y no solo el índice?»*
**R:** Porque la consigna de la cátedra y las diapositivas de la Clase 11 exigen explícitamente medir el rendimiento: *«Devuelve dos valores: el índice de la fila y la cantidad de comparaciones realizadas»*. Devolver `(indice, comparaciones)` nos permite desempaquetar ambos valores en la interfaz y comparar en pantalla la eficiencia contra la binaria.

### P: *«Si agrego 1.000 productos nuevos, ¿cuál de los métodos de ordenamiento tardaría menos?»*
**R:** Si los 1.000 productos se agregaron al final de un catálogo que ya estaba ordenado, el método de **Inserción** será el más rápido, porque cada producto casi no tendrá que desplazarse hacia atrás. Si los productos vinieran en orden totalmente inverso (el peor caso), **Selección** tardará menos en intercambios de memoria, aunque ambos sigan siendo teóricamente $O(n^2)$.

### P: *«¿Por qué protegiste los inputs con `try/except` si podías usar solo `if`?»*
**R:** Porque funciones como `int()` o `float()` lanzan una excepción fatal (`ValueError`) en tiempo de ejecución si el usuario ingresa texto (por ejemplo `"diez"` o `"abc"`). Un condicional `if` básico no puede prevenir ese error de conversión de tipos de forma nativa sin funciones prohibidas. Con `try/except` garantizamos que el sistema jamás se caiga ante un error de tipeo.
