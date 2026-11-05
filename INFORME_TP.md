# INFORME TÉCNICO: SISTEMA DE GESTIÓN DE INVENTARIO
**Materia:** Fundamentos de Informática (UADE - FAIN)  
**Comisión:** Viernes Noche — 2do Cuatrimestre 2026  

---

<!-- ESPACIO RESERVADO PARA CARÁTULA FINAL -->
> **[ESPACIO RESERVADO PARA CARÁTULA E INTEGRANTES]**  
> *Grupo:* [Completar N° de Grupo]  
> *Integrantes:*  
> - [Nombre y Apellido] - Legajo: [Número]  
> - [Nombre y Apellido] - Legajo: [Número]  
> - [Nombre y Apellido] - Legajo: [Número]  
> *Docente:* [Nombre del Docente]  
> *Fecha de Entrega:* 05/11/2026  

---

## 1. Introducción y Estructura de Datos

El presente proyecto consiste en el desarrollo de un **Sistema de Gestión de Inventario** modular en Python para un pequeño comercio. El sistema permite la administración completa del catálogo de productos (altas, bajas, modificación de stock), consultas mediante algoritmos de búsqueda y ordenamiento manuales, generación de reportes y persistencia en archivos CSV.

### Estructura de Datos Obligatoria
La información se gestiona en memoria a través de una **matriz (lista de listas)**, donde cada fila modela un producto único y respeta estrictamente cinco columnas homogéneas:

| Columna | Campo | Tipo de Dato | Restricción / Validación | Ejemplo |
| :---: | :--- | :---: | :--- | :--- |
| **0** | `codigo` | `int` | Entero positivo, clave única identificadora | `101` |
| **1** | `nombre` | `str` | Cadena de texto no vacía | `"Yerba Mate 1kg"` |
| **2** | `categoria`| `str` | Cadena de texto no vacía | `"Almacén"` |
| **3** | `precio` | `float` | Flotante mayor o igual a 0.0 | `3500.0` |
| **4** | `stock` | `int` | Entero mayor o igual a 0 | `15` |

La persistencia se realiza mediante el archivo `inventario.csv`, que almacena una fila de cabecera seguida por los registros separados por comas.

---

## 2. Descripción de las Funciones Principales

El sistema se diseñó de forma puramente procedural, separando la lógica de negocio en `inventario.py` y las interfaces de usuario en `main.py` (consola) y `gui.py` (interfaz visual Tkinter):

1. **Persistencia de Datos:**
   - `cargar_csv(nombre_archivo)`: Lee el archivo CSV omitiendo el encabezado, convierte cada valor al tipo requerido y construye la matriz. Maneja archivos inexistentes inicializando una matriz vacía.
   - `guardar_csv(matriz, nombre_archivo)`: Vuelca la matriz en disco con el encabezado reglamentario preservando el formato CSV.
2. **Gestión de Catálogo (ABM):**
   - `alta_producto(...)`: Valida integridad comercial (código > 0, textos no vacíos, valores no negativos y código no repetido) y añade el producto al inventario.
   - `baja_producto(...)`: Localiza el código por recorrido secuencial y elimina la fila de la matriz mediante `del`.
   - `modificar_stock(...)`: Suma ingresos (+) o egresos (-) de existencias, impidiendo modificaciones que dejen stock negativo.
3. **Algoritmos de Búsqueda:**
   - `busqueda_secuencial(matriz, codigo)`: Recorre linealmente la matriz comparando el código. Devuelve `(indice, comparaciones)`.
   - `busqueda_binaria(matriz, codigo)`: Búsqueda dicotómica sobre matriz ordenada por código mediante punteros `izq`, `der` y `medio`. Devuelve `(indice, comparaciones)`.
4. **Algoritmos de Ordenamiento:**
   - `ordenar_seleccion(matriz, columna)`: Algoritmo de selección de mínimos.
   - `ordenar_burbuja(matriz, columna)`: Intercambio de elementos adyacentes contiguos.
   - `ordenar_insercion(matriz, columna)`: Desplazamiento e inserción en sublista ordenada.
5. **Reportes y Estadísticas:**
   - `stock_bajo(matriz, umbral)`: Filtra productos por debajo de un umbral ingresado.
   - `valor_total(matriz)`: Totaliza la suma de `precio * stock`.
   - `producto_mas_caro(matriz)` y `producto_mas_barato(matriz)`: Algoritmos manuales de búsqueda de extremos (sin usar `min()` ni `max()`).

---

## 3. Análisis Comparativo de Búsqueda y Ordenamiento

### A. Búsqueda Secuencial vs. Búsqueda Binaria
- **Búsqueda Secuencial ($O(n)$):** Funciona sobre cualquier lista sin importar su orden. En el peor caso (elemento al final o inexistente) requiere revisar todos los elementos ($n$ comparaciones). Para nuestro lote inicial de 15 productos, demandó hasta 15 revisiones.
- **Búsqueda Binaria ($O(\log_2 n)$):** Requiere obligatoriamente que la matriz esté **previamente ordenada por código**. En cada paso divide el rango a la mitad, requiriendo a lo sumo $\lceil \log_2(n) \rceil$ iteraciones. En nuestras pruebas prácticas con 15 elementos, la búsqueda binaria resolvió la consulta en solo **2 a 4 comparaciones**, frente a las 15 de la secuencial.
- **Conclusión de Búsqueda:** Para consultas frecuentes o catálogos grandes, la búsqueda binaria es ampliamente superior. Sin embargo, para listas pequeñas o cuando el inventario sufre altas constantes sin ordenar, la búsqueda secuencial evita el costo previo de ordenamiento.

### B. Métodos de Ordenamiento
Se implementaron los tres algoritmos clásicos de complejidad temporal cuadrática $O(n^2)$:
1. **Burbuja:** Muy intuitivo conceptualmente, pero realiza la mayor cantidad de intercambios de memoria ante listas invertidas.
2. **Selección:** Realiza un número fijo de comparaciones, pero minimiza los intercambios de memoria al realizar como máximo un intercambio por ciclo exterior.
3. **Inserción:** Resulta el método más eficiente en la práctica para listas que ya se encuentran **parcialmente ordenadas** (por ejemplo, cuando se da de alta un producto nuevo al final de un catálogo ya ordenado), reduciendo drásticamente las comparaciones.
- **Recomendación para este caso:** El método de **Inserción** es el más adecuado para la operatoria comercial habitual, ya que permite reordenar el inventario de manera casi lineal cuando se agregan nuevos productos al catálogo existente.

---

## 4. División de Tareas y Trabajo en Equipo

El desarrollo del trabajo se organizó de manera colaborativa, asegurando que cada integrante domine la totalidad del código para el coloquio individual:
- **Integrante 1:** Diseño de la matriz, funciones de persistencia de archivos (`cargar_csv`, `guardar_csv`) y pruebas de validación de entradas de usuario.
- **Integrante 2:** Implementación de las funciones de ABM (`alta`, `baja`, `modificar_stock`) y desarrollo de los algoritmos de ordenamiento manual (Selección, Burbuja, Inserción).
- **Integrante 3:** Implementación de búsquedas con conteo de comparaciones (Secuencial y Binaria), reportes estadísticos, menú interactivo por consola (`main.py`) e interfaz gráfica opcional (`gui.py`).
- **Conjunto:** Batería de pruebas de casos borde, redacción del informe técnico y preparación para la defensa oral del proyecto.

---

## 5. Declaración de Uso de Inteligencia Artificial

En cumplimiento con las normativas de honestidad académica de la cátedra de Fundamentos de Informática (FAIN - UADE), se declara lo siguiente:

> Durante la elaboración de este proyecto se utilizó un Asistente de Inteligencia Artificial como herramienta de apoyo didáctico para:
> 1. Consultar dudas conceptuales sobre la sintaxis de widgets en Tkinter.
> 2. Diseñar la batería de pruebas de casos borde para verificar que no existieran fallos con entradas inválidas o matrices vacías.
> 3. Revisar el formato de presentación del menú y tablas en consola.
>
> **Declaración de Autoría y Dominio Técnico:**  
> La totalidad de la lógica procedural, las estructuras de control, los algoritmos manuales de ordenamiento y búsqueda, y las validaciones de negocio fueron comprendidos, verificados y testeados por los integrantes del grupo. Cada integrante se encuentra plenamente capacitado para explicar, defender y modificar cualquier sección del código en vivo durante el Segundo Parcial y el Coloquio Final.
