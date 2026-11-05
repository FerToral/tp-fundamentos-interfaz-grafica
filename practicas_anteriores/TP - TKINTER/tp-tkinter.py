# ==============================================================================
# TRABAJO PRÁCTICO INTEGRADOR: Sistema de Gestión de Inventario
# Materia: Fundamentos de Informática - UADE
# Módulo: tp-tkinter.py (Interfaz Gráfica de Usuario adaptada al TP y la matriz)
# ==============================================================================

import os
import sys

# Aseguramos que pueda importar inventario.py desde el directorio padre
directorio_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if directorio_padre not in sys.path:
    sys.path.insert(0, directorio_padre)

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import inventario

NOMBRE_ARCHIVO = os.path.join(directorio_padre, "inventario.csv")
matriz_inventario = []


def cargar_datos_iniciales():
    global matriz_inventario
    matriz_inventario = inventario.cargar_csv(NOMBRE_ARCHIVO)
    refrescar_tabla(matriz_inventario)
    actualizar_barra_estado(f"Listo. Se cargaron {len(matriz_inventario)} productos.")


def refrescar_tabla(datos):
    for item in tabla.get_children():
        tabla.delete(item)
    for prod in datos:
        precio_formateado = f"${prod[3]:.2f}"
        tabla.insert("", tk.END, values=(prod[0], prod[1], prod[2], precio_formateado, prod[4]))


def limpiar_campos():
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)


def seleccionar_fila(event):
    seleccion = tabla.selection()
    if not seleccion:
        return
    valores = tabla.item(seleccion[0], "values")
    if valores:
        limpiar_campos()
        entry_codigo.insert(0, valores[0])
        entry_nombre.insert(0, valores[1])
        entry_categoria.insert(0, valores[2])
        precio_limpio = valores[3].replace("$", "").strip()
        entry_precio.insert(0, precio_limpio)
        entry_stock.insert(0, valores[4])


def boton_alta():
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
        messagebox.showerror("Error", "Código y stock deben ser enteros; precio debe ser numérico.")
        return

    exito = inventario.alta_producto(matriz_inventario, cod, nombre_txt, cat_txt, pr, st)
    if exito:
        refrescar_tabla(matriz_inventario)
        limpiar_campos()
        actualizar_barra_estado(f"Producto '{nombre_txt}' agregado con éxito.")
        messagebox.showinfo("Éxito", f"Producto '{nombre_txt}' agregado con éxito.")
    else:
        messagebox.showerror("Error", "No se pudo agregar. Verifique que el código no exista y los valores sean válidos.")


def boton_baja():
    codigo_txt = entry_codigo.get().strip()
    if not codigo_txt:
        messagebox.showwarning("Atención", "Seleccione un producto o ingrese un código.")
        return

    try:
        cod = int(codigo_txt)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser un número entero.")
        return

    if not messagebox.askyesno("Confirmar", f"¿Eliminar producto con código {cod}?"):
        return

    exito = inventario.baja_producto(matriz_inventario, cod)
    if exito:
        refrescar_tabla(matriz_inventario)
        limpiar_campos()
        actualizar_barra_estado(f"Producto {cod} eliminado.")
        messagebox.showinfo("Baja", f"Producto {cod} eliminado correctamente.")
    else:
        messagebox.showerror("Error", f"No se encontró el producto {cod}.")


def boton_modificar_stock():
    codigo_txt = entry_codigo.get().strip()
    if not codigo_txt:
        messagebox.showwarning("Atención", "Seleccione un producto o ingrese un código.")
        return

    try:
        cod = int(codigo_txt)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser numérico.")
        return

    cantidad = simpledialog.askinteger("Modificar Stock", "Cantidad a ingresar (+) o egresar (-):", parent=root)
    if cantidad is None:
        return

    exito = inventario.modificar_stock(matriz_inventario, cod, cantidad)
    if exito:
        refrescar_tabla(matriz_inventario)
        actualizar_barra_estado(f"Stock actualizado para código {cod}.")
        messagebox.showinfo("Éxito", "Stock modificado correctamente.")
    else:
        messagebox.showerror("Error", "No se pudo modificar stock (producto no existe o stock menor a 0).")


def boton_buscar():
    codigo_txt = simpledialog.askstring("Buscar", "Ingrese código numérico:", parent=root)
    if not codigo_txt:
        return
    try:
        cod = int(codigo_txt)
    except ValueError:
        messagebox.showerror("Error", "El código debe ser numérico.")
        return

    pos_sec, pasos_sec = inventario.busqueda_secuencial(matriz_inventario, cod)
    inventario.ordenar_burbuja(matriz_inventario, 0)
    pos_bin, pasos_bin = inventario.busqueda_binaria(matriz_inventario, cod)
    refrescar_tabla(matriz_inventario)

    if pos_sec != -1:
        prod = matriz_inventario[pos_bin]
        msg = (
            f"PRODUCTO ENCONTRADO:\n\n"
            f"Código: {prod[0]} | Nombre: {prod[1]}\n"
            f"Categoría: {prod[2]} | Precio: ${prod[3]:.2f} | Stock: {prod[4]}\n\n"
            f"Comparaciones (Clase 11):\n"
            f"• Secuencial: {pasos_sec}\n"
            f"• Binaria:    {pasos_bin}"
        )
        messagebox.showinfo("Búsqueda Exitosa", msg)
    else:
        messagebox.showwarning("No encontrado", f"Código {cod} inexistente.\nSecuencial: {pasos_sec} pasos\nBinaria: {pasos_bin} pasos")


def boton_ordenar():
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
    actualizar_barra_estado(f"Ordenado por {col_str} ({met_str}).")


def boton_stock_bajo():
    umbral = simpledialog.askinteger("Stock Bajo", "Umbral mínimo de stock:", parent=root, initialvalue=10)
    if umbral is None:
        return
    bajos = inventario.stock_bajo(matriz_inventario, umbral)
    refrescar_tabla(bajos)
    actualizar_barra_estado(f"Mostrando {len(bajos)} productos con stock < {umbral}.")


def boton_ver_todo():
    refrescar_tabla(matriz_inventario)
    actualizar_barra_estado(f"Mostrando todos los productos ({len(matriz_inventario)}).")


def boton_valor_total():
    total = inventario.valor_total(matriz_inventario)
    messagebox.showinfo("Valor Total", f"Valor monetario total del inventario:\n\n${total:,.2f}")


def boton_extremos():
    caro = inventario.producto_mas_caro(matriz_inventario)
    barato = inventario.producto_mas_barato(matriz_inventario)
    if not caro or not barato:
        messagebox.showwarning("Atención", "Inventario vacío.")
        return
    msg = f"MÁS CARO: {caro[1]} (${caro[3]:.2f})\n\nMÁS BARATO: {barato[1]} (${barato[3]:.2f})"
    messagebox.showinfo("Extremos", msg)


def boton_guardar():
    inventario.guardar_csv(matriz_inventario, NOMBRE_ARCHIVO)
    actualizar_barra_estado(f"Archivo guardado.")
    messagebox.showinfo("Guardado", "Inventario guardado en CSV exitosamente.")


def actualizar_barra_estado(mensaje):
    lbl_estado.config(text=f"  Estado: {mensaje}")


# ==============================================================================
# INTERFAZ VISUAL
# ==============================================================================

COLOR_FONDO = "#F4F2F9"
COLOR_HEADER = "#2D1B4E"
COLOR_PRIMARIO = "#5B21B6"
COLOR_SECUNDARIO = "#EDE9FE"
COLOR_TEXTO = "#1F2937"
COLOR_BLANCO = "#FFFFFF"

root = tk.Tk()
root.title("Gestión de Inventario - UADE")
root.geometry("1020x680")
root.minsize(920, 600)
root.configure(bg=COLOR_FONDO)

frame_header = tk.Frame(root, bg=COLOR_HEADER, height=65)
frame_header.pack(fill=tk.X, side=tk.TOP)
frame_header.pack_propagate(False)

tk.Label(frame_header, text="SISTEMA DE GESTIÓN DE INVENTARIO", font=("Segoe UI", 14, "bold"), bg=COLOR_HEADER, fg="#FFFFFF").pack(anchor="w", padx=20, pady=(10, 0))
tk.Label(frame_header, text="UADE · Facultad de Ingeniería · Fundamentos de Informática", font=("Segoe UI", 9), bg=COLOR_HEADER, fg="#DDD6FE").pack(anchor="w", padx=20)

frame_cuerpo = tk.Frame(root, bg=COLOR_FONDO)
frame_cuerpo.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

# Formulario Izquierdo
frame_izq = tk.LabelFrame(frame_cuerpo, text=" Gestión de Producto ", font=("Segoe UI", 10, "bold"), bg=COLOR_BLANCO, fg=COLOR_PRIMARIO, padx=15, pady=15, relief="solid", bd=1)
frame_izq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

labels = ["Código:", "Nombre:", "Categoría:", "Precio ($):", "Stock:"]
entries = []
for i, texto in enumerate(labels):
    tk.Label(frame_izq, text=texto, font=("Segoe UI", 9, "bold"), bg=COLOR_BLANCO, fg=COLOR_TEXTO).grid(row=i, column=0, sticky="w", pady=(8, 2))
    ent = tk.Entry(frame_izq, font=("Segoe UI", 9), relief="solid", bd=1, width=22)
    ent.grid(row=i, column=1, sticky="w", pady=(8, 2), padx=(5, 0))
    entries.append(ent)
entry_codigo, entry_nombre, entry_categoria, entry_precio, entry_stock = entries

frame_botones_abm = tk.Frame(frame_izq, bg=COLOR_BLANCO)
frame_botones_abm.grid(row=5, column=0, columnspan=2, pady=(20, 0), sticky="ew")

tk.Button(frame_botones_abm, text="Agregar Producto", bg=COLOR_PRIMARIO, fg=COLOR_BLANCO, font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=boton_alta, pady=6).pack(fill=tk.X, pady=3)
tk.Button(frame_botones_abm, text="Modificar Stock (+ / -)", bg="#6D28D9", fg=COLOR_BLANCO, font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=boton_modificar_stock, pady=6).pack(fill=tk.X, pady=3)
tk.Button(frame_botones_abm, text="Eliminar Producto", bg="#991B1B", fg=COLOR_BLANCO, font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=boton_baja, pady=6).pack(fill=tk.X, pady=3)
tk.Button(frame_botones_abm, text="Limpiar Formulario", bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO, font=("Segoe UI", 9), relief="flat", cursor="hand2", command=limpiar_campos, pady=4).pack(fill=tk.X, pady=(6, 3))

# Panel Derecho
frame_der = tk.Frame(frame_cuerpo, bg=COLOR_FONDO)
frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

frame_tools = tk.Frame(frame_der, bg=COLOR_BLANCO, padx=10, pady=8, relief="solid", bd=1)
frame_tools.pack(fill=tk.X, pady=(0, 10))

tk.Button(frame_tools, text="🔍 Búsqueda (Sec. vs Bin.)", bg=COLOR_PRIMARIO, fg=COLOR_BLANCO, font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=boton_buscar, padx=8, pady=4).pack(side=tk.LEFT, padx=(0, 15))

tk.Label(frame_tools, text="Ordenar por:", font=("Segoe UI", 9), bg=COLOR_BLANCO).pack(side=tk.LEFT)
combo_columna = ttk.Combobox(frame_tools, values=["Código", "Nombre", "Categoría", "Precio", "Stock"], width=9, state="readonly")
combo_columna.set("Código")
combo_columna.pack(side=tk.LEFT, padx=4)

tk.Label(frame_tools, text="Método:", font=("Segoe UI", 9), bg=COLOR_BLANCO).pack(side=tk.LEFT, padx=(8, 0))
combo_metodo = ttk.Combobox(frame_tools, values=["Selección", "Burbuja", "Inserción"], width=10, state="readonly")
combo_metodo.set("Burbuja")
combo_metodo.pack(side=tk.LEFT, padx=4)

tk.Button(frame_tools, text="Aplicar Orden", bg="#7C3AED", fg=COLOR_BLANCO, font=("Segoe UI", 8, "bold"), relief="flat", cursor="hand2", command=boton_ordenar, padx=6, pady=2).pack(side=tk.LEFT, padx=(6, 0))

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background=COLOR_PRIMARIO, foreground="#FFFFFF", relief="flat")
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

frame_reportes = tk.Frame(frame_der, bg=COLOR_FONDO, pady=8)
frame_reportes.pack(fill=tk.X)

tk.Button(frame_reportes, text="Filtrar Stock Bajo", bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO, font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=boton_stock_bajo, padx=8, pady=4).pack(side=tk.LEFT, padx=(0, 6))
tk.Button(frame_reportes, text="Ver Catálogo", bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO, font=("Segoe UI", 9), relief="flat", cursor="hand2", command=boton_ver_todo, padx=8, pady=4).pack(side=tk.LEFT, padx=(0, 15))
tk.Button(frame_reportes, text="Valor Total", bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO, font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=boton_valor_total, padx=8, pady=4).pack(side=tk.LEFT, padx=(0, 6))
tk.Button(frame_reportes, text="Más Caro / Barato", bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO, font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=boton_extremos, padx=8, pady=4).pack(side=tk.LEFT, padx=(0, 6))
tk.Button(frame_reportes, text="💾 Guardar en CSV", bg="#047857", fg=COLOR_BLANCO, font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=boton_guardar, padx=10, pady=4).pack(side=tk.RIGHT)

lbl_estado = tk.Label(root, text="  Estado: Listo.", font=("Segoe UI", 8), bg=COLOR_HEADER, fg="#E9D5FF", anchor="w", height=2)
lbl_estado.pack(fill=tk.X, side=tk.BOTTOM)

if __name__ == "__main__":
    cargar_datos_iniciales()
    root.mainloop()
