import tkinter as tk
from tkinter import ttk, messagebox
from Conexion_fb import db  # Conexión con Firebase
from Clases import Restaurante
from PIL import Image, ImageTk

# Diccionario de subcategorías por categoría
subcategorias_dict = {
    "Gourmet": ["Andina", "Caribe", "Pacífica", "Orinoquía"],
    "Bebidas": ["Alcohólicas", "Calientes", "Frías", "Jugos"],
    "Entradas": ["Frías", "Calientes", "Delicias Regionales"]
}

def ventana_agregar_producto(restaurante, nombre_usuario, return_callback):


    ventana = tk.Toplevel()
    ventana.title("Agregar Nuevo Producto al Menú")
    ventana.geometry("500x500")
    ventana.configure(bg="#f1ddbf")

    logo_img = Image.open("Logo_migaja.jpg")
    logo_img = logo_img.resize((130, 130))
    logo_img = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(ventana, image=logo_img, bg="#f1ddbf")
    logo_label.image = logo_img
    logo_label.pack(pady=(10, 0))

    # Título
    tk.Label(ventana, text="Agregar Producto", font=("Arial", 16, "bold"), bg="#f1ddbf", fg="#1D5A75").pack(pady=10)

    def campo(label_text):
        tk.Label(ventana, text=label_text, bg="#f1ddbf").pack(pady=3)
        entrada = tk.Entry(ventana, width=40)
        entrada.pack()
        return entrada

    # Campos de entrada
    entrada_nombre = campo("Nombre del producto")
    entrada_codigo = campo("Código")
    entrada_precio = campo("Precio")
    entrada_unidades = campo("Unidades")

    # Categoría
    tk.Label(ventana, text="Categoría", bg="#f1ddbf").pack(pady=3)
    categoria_var = tk.StringVar()
    categoria_combo = ttk.Combobox(ventana, textvariable=categoria_var, state="readonly",
                                    values=list(subcategorias_dict.keys()))
    categoria_combo.pack()

    # Subcategoría
    tk.Label(ventana, text="Subcategoría", bg="#f1ddbf").pack(pady=3)
    subcategoria_var = tk.StringVar()
    subcategoria_combo = ttk.Combobox(ventana, textvariable=subcategoria_var, state="readonly")
    subcategoria_combo.pack()

    # Función para actualizar subcategorías al cambiar categoría
    def actualizar_subcategorias(event=None):
        categoria = categoria_var.get()
        subcategorias = subcategorias_dict.get(categoria, [])
        subcategoria_combo["values"] = subcategorias
        if subcategorias:
            subcategoria_var.set(subcategorias[0])
        else:
            subcategoria_var.set("")

    categoria_combo.bind("<<ComboboxSelected>>", actualizar_subcategorias)

    # ✅ Cargar por defecto la primera categoría y sus subcategorías
    categoria_combo.current(0)
    actualizar_subcategorias()

    # Función para guardar el producto en Firestore
    def guardar():
        nombre = entrada_nombre.get().strip()
        codigo = entrada_codigo.get().strip()
        precio = entrada_precio.get().strip()
        unidades = entrada_unidades.get().strip()
        categoria = categoria_var.get().strip().lower()
        subcategoria = subcategoria_var.get().strip().lower()

        if not all([nombre, codigo, precio, unidades, categoria, subcategoria]):
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
            return

        try:
            precio = float(precio)
            unidades = int(unidades)
        except:
            messagebox.showerror("Error", "Precio debe ser un número y unidades un entero.")
            return

        try:
            doc_ref = db.collection("menu").document(codigo)
            doc_ref.set({
                "nombre": nombre,
                "codigo": codigo,
                "precio": precio,
                "unidades": unidades,
                "categoria": categoria,
                "subcategoria": subcategoria,
                "imagen": ""  # Por si después agregas imágenes
            })
            messagebox.showinfo("✅ Producto agregado", f"'{nombre}' se agregó exitosamente al menú.")
            entrada_nombre.delete(0, tk.END)
            entrada_codigo.delete(0, tk.END)
            entrada_precio.delete(0, tk.END)
            entrada_unidades.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar: {e}")

    # Botón para guardar
    tk.Button(ventana, text="Guardar Producto", command=guardar, bg="#8B2F23", fg="white",
              font=("Arial", 12, "bold")).pack(pady=15)

    
    # Botón para volver a la ventana anterior (admin)
    tk.Button(
        ventana,
        text="🔙 Volver al Menú Principal",
        command=lambda: [ventana.destroy(), return_callback()],
        bg="#333333",
        fg="white",
        font=("Arial", 11, "bold"),
        width=25,
        height=2,
        relief="flat",
        activebackground="#15445a",
        activeforeground="white",
        cursor="hand2"
    ).pack(pady=(10, 20))

    ventana.transient()
    ventana.grab_set()
    ventana.focus_set()

