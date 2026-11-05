import tkinter as tk
# Función para cerrar la ventana
def cerrar():
    root.destroy()
root = tk.Tk()
root.title("Crud de artículos")
root.geometry("800x600")
# Crear un botón y colocarlo en la ventana
btn_cerrar = tk.Button(root, text="Cerrar", command=cerrar)
btn_cerrar.grid(row=10, column=8, pady=5)
# Iniciar el bucle principal de la aplicación
root.mainloop()
