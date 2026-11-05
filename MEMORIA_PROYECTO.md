# MEMORIA Y ESTADO DEL PROYECTO: TP INTEGRADOR - SISTEMA DE GESTIÓN DE INVENTARIO

## 1. Contexto Académico y Proyecto
- **Institución:** UADE - Facultad de Ingeniería (FAIN).
- **Materia:** Fundamentos de Informática (Comisión Viernes Noche - 2do Cuatrimestre 2026).
- **Ubicación local del proyecto:**
  `C:\Users\Fernando Toralez\Documents\UADE_Ing_en_Informatica\Fundamentos de Informática\TP - Interfaz gráfica`
- **Archivos de referencia en la carpeta:**
  - `TP Integrador - Sistema de Gestión de Inventario.pdf` (consigna oficial completa).
  - `Clase 11 - Búsqueda Secuencial y Binaria.pdf` (código y nomenclatura de cátedra).
  - `inventario.csv` (archivo de prueba con 15 productos iniciales).
  - `inventario.py` (módulo de funciones de inventario).

---

## 2. Reglas de Interacción y Rol (Skill Obligatoria)

1. **Regla de Oro de Interacción:**
   - **NO HACER NADA POR DEFECTO.** Presentar siempre un plan de trabajo claro y solicitar aprobación explícita antes de crear o editar código.
   - Avanzar paso a paso, función por función o módulo por módulo, validando cada etapa.
   - Consultar cualquier alternativa algorítmica o de diseño con el usuario.

2. **Perfil del Programador (Developer Junior):**
   - Código simple, limpio, procedural y fácil de defender en un coloquio individual o examen práctico en computadora.
   - **SIN SOBREINGENIERÍA:** Prohibido el uso de Programación Orientada a Objetos (POO), lambdas, comprensiones de listas complejas o librerías externas no vistas en clase.
   - Nombres descriptivos y en español (`matriz_inventario`, `cantidad_comparaciones`, `izq`, `der`, `medio`, etc.).
   - Comentarios explicativos en español en cada función (qué hace, qué parámetros recibe y qué retorna).

3. **Restricciones Técnicas Obligatorias:**
   - **Estructura de datos obligatoria:** Matriz (lista de listas), donde cada fila representa un producto con 5 columnas fijas:
     - Columna 0: `codigo` (int, único)
     - Columna 1: `nombre` (str)
     - Columna 2: `categoria` (str)
     - Columna 3: `precio` (float, >= 0)
     - Columna 4: `stock` (int, >= 0)
   - **Prohibiciones algorítmicas:** ❌ Prohibido usar `sort()`, `sorted()`, `min()`, `max()`, `index()` ni el operador `in` para búsquedas, ordenamientos o extremos.
   - **Obligatorio:** Algoritmos manuales con bucles `for` / `while`, contadores y comparaciones condicionales directas vistas en clase.

4. **Decisiones de Diseño Acordadas:**
   - **Modularización:** Separar lógica en `inventario.py` y el menú de consola en `main.py`.
   - **Algoritmos de ordenamiento:** Se acordó implementar los **tres** métodos (`ordenar_seleccion`, `ordenar_burbuja`, `ordenar_insercion`).

---

## 3. Estado Actual de Avance

```
[Fase 1] Núcleo de Inventario (Funciones Obligatorias en inventario.py) [✔ COMPLETADO]
 ├── [✔] Paso 1.1: Archivo 'inventario.csv' creado con 15 productos de prueba válidos.
 ├── [✔] Paso 1.2: Persistencia: 'cargar_csv(nombre_archivo)' y 'guardar_csv(matriz, nombre_archivo)'.
 ├── [✔] Paso 1.3: ABM: 'alta_producto', 'baja_producto', 'modificar_stock'.
 ├── [✔] Paso 1.4: Búsquedas manuales: 'busqueda_secuencial' y 'busqueda_binaria'.
 ├── [✔] Paso 1.5: Ordenamientos manuales: 'ordenar_seleccion', 'ordenar_burbuja', 'ordenar_insercion'.
 └── [✔] Paso 1.6: Reportes: 'stock_bajo', 'valor_total', 'producto_mas_caro', 'producto_mas_barato'.
[Fase 2] Menú interactivo por consola ('main.py') [✔ COMPLETADO]
[Fase 3] Pruebas y validaciones de casos borde ('test_casos_borde.py') [✔ COMPLETADO - 0 errores]
[Fase 4] Interfaz Gráfica con Tkinter ('gui.py') [✔ COMPLETADO]
[Fase 5] Informe del TP ('INFORME_TP.md') y Guía Técnica ('GUIA_TECNICA_COLOQUIO.md') [✔ COMPLETADO]
```

---

## 4. Estructura Limpia del Proyecto (Reorganización Completada)

```
TP - Interfaz gráfica/
 ├── main.py                     # Programa principal interactivo por consola (obligatorio)
 ├── gui.py                      # Interfaz gráfica de usuario en Tkinter (desafío opcional)
 ├── inventario.py               # Lógica de negocio y funciones algorítmicas puras
 ├── inventario.csv              # Base de datos en CSV con 15 productos válidos
 ├── test_casos_borde.py         # Suite completa de pruebas automatizadas
 ├── INFORME_TP.md               # Informe reglamentario de 3 páginas para la entrega
 ├── GUIA_TECNICA_COLOQUIO.md    # Guía pedagógica de estudio para el coloquio y parcial
 ├── DECISIONES_DISENO_Y_DEFENSA.md # Análisis de ambigüedades, justificaciones y defensa oral
 ├── MEMORIA_PROYECTO.md         # Registro histórico del desarrollo
 ├── documentacion_catedra/      # Enunciado oficial y PDFs de teoría/práctica de UADE
 └── practicas_anteriores/       # Prácticas iniciales de clase y borradores
```
