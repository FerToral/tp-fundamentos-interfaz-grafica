# ==============================================================================
# TRABAJO PRÁCTICO INTEGRADOR: Sistema de Gestión de Inventario
# Materia: Fundamentos de Informática - UADE
# Módulo: gui.py (Interfaz Gráfica de Usuario con Tkinter - Estilo Violeta Ejecutivo)
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import inventario

NOMBRE_ARCHIVO = "inventario.csv"

# Matriz global en memoria para la interfaz
matriz_inventario = []


# ==============================================================================
# FUNCIONES DE INTERACCIÓN Y LÓGICA DE LA INTERFAZ
# ==============================================================================

def cargar_datos_iniciales():
    """Carga los productos desde el CSV al iniciar la interfaz."""
    global matriz_inventario
    matriz_inventario = inventario.cargar_csv(NOMBRE_ARCHIVO)
    refrescar_tabla(matriz_inventario)
    actualizar_barra_estado(f"Listo. Se cargaron {len(matriz_inventario)} productos desde '{NOMBRE_ARCHIVO}'.")


def refrescar_tabla(datos):
    """
    Limpia y vuelve a cargar los datos en la tabla (Treeview).
    """
    # Limpiamos las filas actuales
    for item in tabla.get_children():
        tabla.delete(item)

    # Insertamos las filas de la matriz
    for prod in datos:
        precio_formateado = f"${prod[3]:.2f}"
        tabla.insert("", tk.END, values=(prod[0], prod[1], prod[2], precio_formateado, prod[4]))


def limpiar_campos():
    """Vacía los campos de entrada del formulario."""
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)


def seleccionar_fila(event):
    """Al hacer clic en un producto de la tabla, copia sus datos al formulario."""
    seleccion = tabla.selection()
    if not seleccion:
        return

    item_id = seleccion[0]
    valores = tabla.item(item_id, "values")
    if valores:
        limpiar_campos()
        entry_codigo.insert(0, valores[0])
        entry_nombre.insert(0, valores[1])
        entry_categoria.insert(0, valores[2])
        # Quitamos el símbolo '$' para editar el precio con comodidad
        precio_limpio = valores[3].replace("$", "").strip()
        entry_precio.insert(0, precio_limpio)
        entry_stock.insert(0, valores[4])


def boton_alta():
    """Toma los datos de los Entry y da de alta un producto usando inventario.py."""
    codigo_txt = entry_codigo.get().strip()
    nombre_txt = entry_nombre.get().strip()
    cat_txt = entry_categoria.get().strip()
    precio_txt = entry_precio.get().strip()
    stock_txt = entry_stock.get().strip()

    if not codigo_txt or not nombre_txt or not cat_txt or not precio_txt or not stock_txt:
        messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
        return

    try:
        cod = int(codigo_txt)
        pr = float(precio_txt)
        st = int(stock_txt)
    except ValueError:
        messagebox.showerror("Error de datos", "Código y stock deben ser enteros; precio debe ser numérico.")
        return

    exito = inventario.alta_producto(matriz_inventario, cod, nombre_txt, cat_txt, pr, st)
    if exito:
        refrescar_tabla(matriz_inventario)
        limpiar_campos()
        actualizar_barra_estado(f"Producto {cod} ('{nombre_txt}') agregado con éxito.")
        messagebox.showinfo("Éxito", f"Producto '{nombre_txt}' agregado con éxito.")
    else:
        messagebox.showerror("Error", "No se pudo agregar. Verifique que el código no exista y los valores sean positivos.")


def boton_baja():
    """Elimina el producto seleccionado en la tabla o según el código del campo."""
    codigo_txt = entry_codigo.get().strip()
    if not codigo_txt:
        messagebox.showwarning("Atención", "Seleccione un producto de la lista o ingrese un código para eliminar.")
        return

    try:
        cod = int(codigo_txt)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero.")
        return

    confirmar = messagebox.askyesno("Confirmar baja", f"¿Está seguro de que desea eliminar el producto con código {cod}?")
    if not confirmar:
        return

    exito = inventario.baja_producto(matriz_inventario, cod)
    if exito:
        refrescar_tabla(matriz_inventario)
        limpiar_campos()
        actualizar_barra_estado(f"Producto {cod} eliminado.")
        messagebox.showinfo("Baja Exitosa", f"Producto con código {cod} eliminado correctamente.")
    else:
        messagebox.showerror("Error", f"No se encontró el producto con código {cod}.")


def boton_modificar_stock():
    """Modifica el stock sumando o restando una cantidad."""
    codigo_txt = entry_codigo.get().strip()
    if not codigo_txt:
        messagebox.showwarning("Atención", "Seleccione un producto o ingrese un código.")
        return

    try:
        cod = int(codigo_txt)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser numérico.")
        return

    cantidad = simpledialog.askinteger(
        "Modificar Stock",
        "Ingrese la cantidad a ingresar (positiva) o egresar (negativa):",
        parent=root
    )

    if cantidad is None:
        return

    exito = inventario.modificar_stock(matriz_inventario, cod, cantidad)
    if exito:
        refrescar_tabla(matriz_inventario)
        actualizar_barra_estado(f"Stock actualizado para el producto {cod} (variación: {cantidad}).")
        messagebox.showinfo("Éxito", "Stock modificado correctamente.")
    else:
        messagebox.showerror("Error", "No se pudo actualizar el stock (producto inexistente o stock resultante negativo).")


def boton_buscar():
    """
    Busca por código y compara la búsqueda secuencial con la binaria,
    mostrando las comparaciones realizadas por cada una (Clase 11).
    """
    codigo_txt = simpledialog.askstring("Buscar Producto", "Ingrese el código numérico a buscar:", parent=root)
    if not codigo_txt:
        return

    try:
        cod = int(codigo_txt)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser numérico.")
        return

    # 1. Búsqueda Secuencial
    pos_sec, pasos_sec = inventario.busqueda_secuencial(matriz_inventario, cod)

    # 2. Búsqueda Binaria (requiere ordenar por código previamente)
    inventario.ordenar_burbuja(matriz_inventario, 0)
    pos_bin, pasos_bin = inventario.busqueda_binaria(matriz_inventario, cod)

    refrescar_tabla(matriz_inventario)

    if pos_sec != -1:
        prod = matriz_inventario[pos_bin]
        # Resaltamos en la tabla
        for item in tabla.get_children():
            if str(tabla.item(item, "values")[0]) == str(cod):
                tabla.selection_set(item)
                tabla.see(item)
                break

        msg = (
            f"PRODUCTO ENCONTRADO:\n\n"
            f"Código: {prod[0]}\n"
            f"Nombre: {prod[1]}\n"
            f"Categoría: {prod[2]}\n"
            f"Precio: ${prod[3]:.2f}\n"
            f"Stock: {prod[4]} unidades\n\n"
            f"----------------------------------------\n"
            f"Comparación Algorítmica (Clase 11):\n"
            f"• Búsqueda Secuencial: {pasos_sec} comparaciones\n"
            f"• Búsqueda Binaria:    {pasos_bin} comparaciones"
        )
        messagebox.showinfo("Resultado de Búsqueda", msg)
    else:
        msg = (
            f"El producto con código {cod} NO existe en el inventario.\n\n"
            f"Comparaciones realizadas:\n"
            f"• Secuencial: {pasos_sec}\n"
            f"• Binaria:    {pasos_bin}"
        )
        messagebox.showwarning("No encontrado", msg)


def boton_ordenar():
    """Ventana emergente para seleccionar columna y algoritmo de ordenamiento."""
    col_str = combo_columna.get()
    met_str = combo_metodo.get()

    map_cols = {"Código": 0, "Nombre": 1, "Categoría": 2, "Precio": 3, "Stock": 4}
    col_idx = map_cols.get(col_str, 0)

    if met_str == "Selección":
        inventario.ordenar_seleccion(matriz_inventario, col_idx)
    elif met_str == "Burbuja":
        inventario.ordenar_burbuja(matriz_inventario, col_idx)
    elif met_str == "Inserción":
        inventario.ordenar_insercion(matriz_inventario, col_idx)

    refrescar_tabla(matriz_inventario)
    actualizar_barra_estado(f"Inventario ordenado por '{col_str}' usando algoritmo de {met_str}.")


def boton_stock_bajo():
    """Filtra y muestra productos con stock menor a un umbral."""
    umbral = simpledialog.askinteger("Stock Bajo", "Ingrese el umbral mínimo de stock:", parent=root, initialvalue=10)
    if umbral is None:
        return

    bajos = inventario.stock_bajo(matriz_inventario, umbral)
    refrescar_tabla(bajos)
    actualizar_barra_estado(f"Mostrando {len(bajos)} productos con stock menor a {umbral}. Presione 'Ver Todo' para restablecer.")


def boton_ver_todo():
    """Restablece la tabla para mostrar todos los productos."""
    refrescar_tabla(matriz_inventario)
    actualizar_barra_estado(f"Mostrando todos los productos ({len(matriz_inventario)}).")


def boton_valor_total():
    """Muestra el valor monetario total calculado del inventario."""
    total = inventario.valor_total(matriz_inventario)
    messagebox.showinfo("Valor Total de Inventario", f"El valor total valorizado del stock actual es:\n\n${total:,.2f}")


def boton_extremos():
    """Muestra el producto más caro y el más barato hallados manualmente."""
    caro = inventario.producto_mas_caro(matriz_inventario)
    barato = inventario.producto_mas_barato(matriz_inventario)

    if caro is None or barato is None:
        messagebox.showwarning("Atención", "El inventario está vacío.")
        return

    msg = (
        f"PRODUCTO MÁS CARO:\n"
        f"• {caro[1]} (Código {caro[0]}) -> ${caro[3]:.2f}\n\n"
        f"PRODUCTO MÁS BARATO:\n"
        f"• {barato[1]} (Código {barato[0]}) -> ${barato[3]:.2f}"
    )
    messagebox.showinfo("Extremos de Precios", msg)


def boton_guardar():
    """Guarda los cambios de la matriz en el archivo CSV."""
    inventario.guardar_csv(matriz_inventario, NOMBRE_ARCHIVO)
    actualizar_barra_estado(f"Archivo '{NOMBRE_ARCHIVO}' guardado correctamente.")
    messagebox.showinfo("Guardado", f"Datos guardados exitosamente en '{NOMBRE_ARCHIVO}'.")


def actualizar_barra_estado(mensaje):
    """Actualiza el texto informativo al pie de la ventana."""
    lbl_estado.config(text=f"  Estado: {mensaje}")


# ==============================================================================
# CONSTRUCCIÓN DE LA INTERFAZ VISUAL (PALETA VIOLETA EJECUTIVA)
# ==============================================================================

# Paleta de colores sobria y armónica
COLOR_FONDO = "#F4F2F9"          # Gris violáceo suave
COLOR_HEADER = "#2D1B4E"         # Violeta oscuro noche
COLOR_PRIMARIO = "#5B21B6"       # Violeta real para botones destacados
COLOR_HOVER = "#4C1D95"          # Violeta más profundo
COLOR_SECUNDARIO = "#EDE9FE"     # Lavanda claro para paneles
COLOR_TEXTO = "#1F2937"          # Gris carbón para máxima legibilidad
COLOR_BLANCO = "#FFFFFF"

root = tk.Tk()
root.title("Sistema de Gestión de Inventario - Fundamentos de Informática")
root.geometry("1020x680")
root.minsize(920, 600)
root.configure(bg=COLOR_FONDO)

# Encabezado Superior Elegante
frame_header = tk.Frame(root, bg=COLOR_HEADER, height=65)
frame_header.pack(fill=tk.X, side=tk.TOP)
frame_header.pack_propagate(False)

lbl_titulo = tk.Label(
    frame_header, 
    text="SISTEMA DE GESTIÓN DE INVENTARIO", 
    font=("Segoe UI", 14, "bold"), 
    bg=COLOR_HEADER, 
    fg="#FFFFFF"
)
lbl_titulo.pack(anchor="w", padx=20, pady=(10, 0))

lbl_subtitulo = tk.Label(
    frame_header, 
    text="UADE · Facultad de Ingeniería · Fundamentos de Informática", 
    font=("Segoe UI", 9), 
    bg=COLOR_HEADER, 
    fg="#DDD6FE"
)
lbl_subtitulo.pack(anchor="w", padx=20)

# Contenedor Principal (Panel izquierdo: Formulario | Panel derecho: Tabla y Reportes)
frame_cuerpo = tk.Frame(root, bg=COLOR_FONDO)
frame_cuerpo.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

# ------------------------------------------------------------------------------
# PANEL IZQUIERDO: FORMULARIO Y ACCIONES DE ABM
# ------------------------------------------------------------------------------
frame_izq = tk.LabelFrame(
    frame_cuerpo, 
    text=" Gestión de Producto ", 
    font=("Segoe UI", 10, "bold"),
    bg=COLOR_BLANCO, 
    fg=COLOR_PRIMARIO, 
    padx=15, 
    pady=15,
    relief="solid",
    bd=1
)
frame_izq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

# Campos de entrada
labels = ["Código:", "Nombre:", "Categoría:", "Precio ($):", "Stock:"]
entries = []

for i, texto in enumerate(labels):
    lbl = tk.Label(frame_izq, text=texto, font=("Segoe UI", 9, "bold"), bg=COLOR_BLANCO, fg=COLOR_TEXTO, anchor="w")
    lbl.grid(row=i, column=0, sticky="w", pady=(8, 2))
    ent = tk.Entry(frame_izq, font=("Segoe UI", 9), relief="solid", bd=1, width=22)
    ent.grid(row=i, column=1, sticky="w", pady=(8, 2), padx=(5, 0))
    entries.append(ent)

entry_codigo, entry_nombre, entry_categoria, entry_precio, entry_stock = entries

# Botonera de ABM
frame_botones_abm = tk.Frame(frame_izq, bg=COLOR_BLANCO)
frame_botones_abm.grid(row=5, column=0, columnspan=2, pady=(20, 0), sticky="ew")

btn_alta = tk.Button(
    frame_botones_abm, 
    text="Agregar Producto", 
    bg=COLOR_PRIMARIO, 
    fg=COLOR_BLANCO, 
    font=("Segoe UI", 9, "bold"),
    relief="flat", 
    cursor="hand2",
    command=boton_alta,
    padx=8, pady=6
)
btn_alta.pack(fill=tk.X, pady=3)

btn_modificar = tk.Button(
    frame_botones_abm, 
    text="Modificar Stock (+ / -)", 
    bg="#6D28D9", 
    fg=COLOR_BLANCO, 
    font=("Segoe UI", 9, "bold"),
    relief="flat", 
    cursor="hand2",
    command=boton_modificar_stock,
    padx=8, pady=6
)
btn_modificar.pack(fill=tk.X, pady=3)

btn_baja = tk.Button(
    frame_botones_abm, 
    text="Eliminar Producto", 
    bg="#991B1B", 
    fg=COLOR_BLANCO, 
    font=("Segoe UI", 9, "bold"),
    relief="flat", 
    cursor="hand2",
    command=boton_baja,
    padx=8, pady=6
)
btn_baja.pack(fill=tk.X, pady=3)

btn_limpiar = tk.Button(
    frame_botones_abm, 
    text="Limpiar Formulario", 
    bg=COLOR_SECUNDARIO, 
    fg=COLOR_PRIMARIO, 
    font=("Segoe UI", 9),
    relief="flat", 
    cursor="hand2",
    command=limpiar_campos,
    padx=8, pady=4
)
btn_limpiar.pack(fill=tk.X, pady=(6, 3))


# ------------------------------------------------------------------------------
# PANEL DERECHO: BARRA DE HERRAMIENTAS, TABLA Y REPORTES
# ------------------------------------------------------------------------------
frame_der = tk.Frame(frame_cuerpo, bg=COLOR_FONDO)
frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Barra de Herramientas Superior (Búsqueda y Ordenamiento)
frame_tools = tk.Frame(frame_der, bg=COLOR_BLANCO, padx=10, pady=8, relief="solid", bd=1)
frame_tools.pack(fill=tk.X, pady=(0, 10))

btn_buscar = tk.Button(
    frame_tools, 
    text="🔍 Búsqueda (Sec. vs Bin.)", 
    bg=COLOR_PRIMARIO, 
    fg=COLOR_BLANCO, 
    font=("Segoe UI", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=boton_buscar,
    padx=8, pady=4
)
btn_buscar.pack(side=tk.LEFT, padx=(0, 15))

# Selector de ordenamiento
tk.Label(frame_tools, text="Ordenar por:", font=("Segoe UI", 9), bg=COLOR_BLANCO).pack(side=tk.LEFT)
combo_columna = ttk.Combobox(frame_tools, values=["Código", "Nombre", "Categoría", "Precio", "Stock"], width=9, state="readonly")
combo_columna.set("Código")
combo_columna.pack(side=tk.LEFT, padx=4)

tk.Label(frame_tools, text="Método:", font=("Segoe UI", 9), bg=COLOR_BLANCO).pack(side=tk.LEFT, padx=(8, 0))
combo_metodo = ttk.Combobox(frame_tools, values=["Selección", "Burbuja", "Inserción"], width=10, state="readonly")
combo_metodo.set("Burbuja")
combo_metodo.pack(side=tk.LEFT, padx=4)

btn_ordenar = tk.Button(
    frame_tools, 
    text="Aplicar Orden", 
    bg="#7C3AED", 
    fg=COLOR_BLANCO, 
    font=("Segoe UI", 8, "bold"),
    relief="flat",
    cursor="hand2",
    command=boton_ordenar,
    padx=6, pady=2
)
btn_ordenar.pack(side=tk.LEFT, padx=(6, 0))

# Tabla de Productos (Treeview con estilo ttk)
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview.Heading", 
    font=("Segoe UI", 9, "bold"), 
    background=COLOR_PRIMARIO, 
    foreground="#FFFFFF",
    relief="flat"
)
style.configure("Treeview", font=("Segoe UI", 9), rowheight=24, background="#FFFFFF", fieldbackground="#FFFFFF")
style.map("Treeview", background=[("selected", "#7C3AED")], foreground=[("selected", "#FFFFFF")])

frame_tabla = tk.Frame(frame_der, bg=COLOR_BLANCO, relief="solid", bd=1)
frame_tabla.pack(fill=tk.BOTH, expand=True)

columnas = ("codigo", "nombre", "categoria", "precio", "stock")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")

tabla.heading("codigo", text="Código")
tabla.heading("nombre", text="Nombre")
tabla.heading("categoria", text="Categoría")
tabla.heading("precio", text="Precio")
tabla.heading("stock", text="Stock")

tabla.column("codigo", width=75, anchor="center")
tabla.column("nombre", width=220, anchor="w")
tabla.column("categoria", width=120, anchor="w")
tabla.column("precio", width=95, anchor="e")
tabla.column("stock", width=80, anchor="center")

scroll_y = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
tabla.configure(yscrollcommand=scroll_y.set)

tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

# Barra Inferior de Reportes y Guardado
frame_reportes = tk.Frame(frame_der, bg=COLOR_FONDO, pady=8)
frame_reportes.pack(fill=tk.X)

btn_stock_bajo = tk.Button(
    frame_reportes, 
    text="Filtrar Stock Bajo", 
    bg=COLOR_SECUNDARIO, 
    fg=COLOR_PRIMARIO, 
    font=("Segoe UI", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=boton_stock_bajo,
    padx=8, pady=4
)
btn_stock_bajo.pack(side=tk.LEFT, padx=(0, 6))

btn_ver_todo = tk.Button(
    frame_reportes, 
    text="Ver Catálogo Completo", 
    bg=COLOR_SECUNDARIO, 
    fg=COLOR_TEXTO, 
    font=("Segoe UI", 9),
    relief="flat",
    cursor="hand2",
    command=boton_ver_todo,
    padx=8, pady=4
)
btn_ver_todo.pack(side=tk.LEFT, padx=(0, 15))

btn_valor_total = tk.Button(
    frame_reportes, 
    text="Valor Total", 
    bg=COLOR_SECUNDARIO, 
    fg=COLOR_PRIMARIO, 
    font=("Segoe UI", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=boton_valor_total,
    padx=8, pady=4
)
btn_valor_total.pack(side=tk.LEFT, padx=(0, 6))

btn_extremos = tk.Button(
    frame_reportes, 
    text="Más Caro / Más Barato", 
    bg=COLOR_SECUNDARIO, 
    fg=COLOR_PRIMARIO, 
    font=("Segoe UI", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=boton_extremos,
    padx=8, pady=4
)
btn_extremos.pack(side=tk.LEFT, padx=(0, 6))

btn_guardar = tk.Button(
    frame_reportes, 
    text="💾 Guardar Cambios CSV", 
    bg="#047857", 
    fg=COLOR_BLANCO, 
    font=("Segoe UI", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=boton_guardar,
    padx=10, pady=4
)
btn_guardar.pack(side=tk.RIGHT)

# Barra de Estado al pie de la ventana
lbl_estado = tk.Label(
    root, 
    text="  Estado: Listo.", 
    font=("Segoe UI", 8), 
    bg=COLOR_HEADER, 
    fg="#E9D5FF", 
    anchor="w", 
    height=2
)
lbl_estado.pack(fill=tk.X, side=tk.BOTTOM)


# ==============================================================================
# INICIO DE LA APLICACIÓN
# ==============================================================================

if __name__ == "__main__":
    cargar_datos_iniciales()
    root.mainloop()
