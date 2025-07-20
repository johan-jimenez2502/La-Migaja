import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Clases import Restaurante, Pedido
from Conexion_fb import db

# Estilos
FONDO = "#f1ddbf"
COLOR_BOTON = "#8B2F23"
COLOR_TEXTO = "#1D5A75"
FUENTE = ("Times New Roman", 12)
TEXTO_TITULO = ("Times New Roman", 14, "bold")

CATEGORIAS_PRINCIPALES = ["Bebidas", "Entradas", "Gourmet"]
subcategorias = {
    "Bebidas": ["Calientes", "Jugos", "Frías", "Alcohólicas"],
    "Entradas": ["Calientes", "Frías"],
    "Gourmet": ["Andina", "Caribe", "Pacífica", "Orinoquía"]
}

def ventana_mesero(restaurante, nombre_usuario, return_callback):
    ventana = tk.Toplevel()
    ventana.title(f"La Migaja - Mesero ({nombre_usuario})")
    ventana.geometry("1000x720")
    ventana.configure(bg=FONDO)
    ventana.iconbitmap("Logo_migaja.ico")

    main_content_area = tk.Frame(ventana, bg=FONDO)
    main_content_area.pack(expand=True, fill="both", padx=20, pady=10)

    # --- Encabezado superior ---
    header = tk.Frame(main_content_area, bg=FONDO)
    header.pack(fill="x", pady=10)

        # --- Encabezado superior ---
    header = tk.Frame(main_content_area, bg=FONDO)
    header.pack(fill="x", pady=10)

    try:
        logo = Image.open("Logo_migaja.jpg")
        logo = logo.resize((120, 120))
        logo_tk = ImageTk.PhotoImage(logo)
        lbl_logo = tk.Label(header, image=logo_tk, bg=FONDO)
        lbl_logo.image = logo_tk  # Asegura que la imagen no se borre por el recolector de basura
        lbl_logo.pack(side="right", padx=20)
        ventana.logo_tk = logo_tk  # Extra: referencia en ventana para asegurar persistencia
    except Exception as e:
        print(f"No se pudo cargar el logo: {e}")




    info = tk.Frame(header, bg=FONDO)
    info.pack(side="left")

    tk.Label(info, text="La Migaja", font=("Georgia", 20, "bold"), bg=FONDO, fg=COLOR_TEXTO).pack(anchor="w")
    tk.Label(info, text=f"Bienvenido, {nombre_usuario}", font=("Georgia", 12), bg=FONDO).pack(anchor="w")



    center_frame = tk.Frame(main_content_area, bg=FONDO)
    center_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(center_frame, bg=FONDO, highlightthickness=0, yscrollincrement=10)
    scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=FONDO)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    ventana.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    productos = restaurante.obtener_menu()
    carrito = {}
    comandera = tk.Frame(main_content_area, bg="#fffaf0", bd=2, relief="ridge")
    comandera.pack(side="right", fill="y", padx=(10, 0), ipadx=5)

    tk.Label(comandera, text="🧾 COMANDERA", font=("Courier New", 13, "bold"), bg="#fffaf0", fg=COLOR_TEXTO).pack(pady=(10, 5))
    carrito_lista = tk.Listbox(comandera, font=("Courier New", 10), width=35, height=20, bg="#fefefe")
    carrito_lista.pack(padx=10, pady=5, fill="both", expand=True)

    descripcion_label = tk.Label(comandera, text="Notas del pedido", font=FUENTE, bg="#fffaf0")
    descripcion_label.pack(pady=(10, 2))
    descripcion_entry = tk.Text(comandera, height=3, font=("Arial", 10))
    descripcion_entry.pack(padx=5, pady=5, fill="x")
    

    def actualizar_carrito():
        carrito_lista.delete(0, tk.END)
        for prod_codigo in carrito:
            nombre = carrito[prod_codigo]["producto"].nombre
            cantidad = carrito[prod_codigo]["cantidad"]
            descripcion = carrito[prod_codigo].get("descripcion", "")
            texto = f"{nombre} x{cantidad}"
            if descripcion:
                texto += f"\n  • {descripcion}"
            carrito_lista.insert(tk.END, texto)

    def mostrar_categoria(categoria):
        for widget in center_frame.winfo_children():
            widget.destroy()

        productos_por_subcategoria = {}
        for prod in productos:
            if prod.categoria.strip().lower() == categoria.strip().lower():
                sub = prod.subcategoria.strip().capitalize() if prod.subcategoria else "Otros"
                if sub == "Frio": sub = "Frías"
                if sub == "Alcoholica": sub = "Alcohólicas"
                productos_por_subcategoria.setdefault(sub, []).append(prod)

        orden_subs = subcategorias.get(categoria, [])

        # Canvas horizontal con scroll extendido
        canvas_horizontal = tk.Canvas(center_frame, bg=FONDO, highlightthickness=0)
        scrollbar_horizontal = tk.Scrollbar(center_frame, orient="horizontal", command=canvas_horizontal.xview)
        canvas_horizontal.configure(xscrollcommand=scrollbar_horizontal.set)
        canvas_horizontal.pack(side="top", fill="both", expand=True)
        scrollbar_horizontal.pack(side="bottom", fill="x")

        frame_horizontal = tk.Frame(canvas_horizontal, bg=FONDO)
        canvas_horizontal.create_window((0, 0), window=frame_horizontal, anchor="nw")

        # Expandir scroll según contenido
        frame_horizontal.bind(
            "<Configure>",
            lambda e: canvas_horizontal.configure(scrollregion=canvas_horizontal.bbox("all"))
        )

        for idx, sub in enumerate(orden_subs):
            if sub not in productos_por_subcategoria:
                continue

            columna = tk.Frame(frame_horizontal, bg=FONDO)
            columna.grid(row=0, column=idx, padx=10, sticky="n")

            tk.Label(columna, text=sub, font=TEXTO_TITULO, bg=FONDO, fg=COLOR_TEXTO).pack(pady=(0, 5))

            # Canvas y scrollbar para scroll vertical por subcategoría
            canvas_columna = tk.Canvas(columna, bg=FONDO, height=500, highlightthickness=0)
            scrollbar_columna = ttk.Scrollbar(columna, orient="vertical", command=canvas_columna.yview)
            canvas_columna.configure(yscrollcommand=scrollbar_columna.set)

            scrollable_frame = tk.Frame(canvas_columna, bg=FONDO)
            canvas_columna.create_window((0, 0), window=scrollable_frame, anchor="nw")

            # Expande el scroll dinámicamente
            scrollable_frame.bind(
                "<Configure>",
                lambda e, c=canvas_columna: c.configure(scrollregion=c.bbox("all"))
            )

            canvas_columna.pack(side="left", fill="both", expand=True)
            scrollbar_columna.pack(side="right", fill="y")

            # Scroll con mouse en cada columna
            canvas_columna.bind_all("<MouseWheel>", lambda e: canvas_columna.yview_scroll(int(-1*(e.delta/120)), "units"))

            for prod in productos_por_subcategoria[sub]:
                fila = tk.Frame(columna, bg=FONDO)
                fila.pack(fill="x", pady=2)
                tk.Label(fila, text=prod.nombre, font=("Arial", 10), bg=FONDO).pack(side="left", padx=3)
                tk.Label(fila, text=f"${prod.precio}", font=("Arial", 10), bg=FONDO, fg=COLOR_TEXTO).pack(side="left", padx=3)

                cantidad = tk.IntVar(value=0)
                bloque_cantidad = tk.Frame(fila, bg=FONDO)
                bloque_cantidad.pack(side="right", padx=5)

                def aumentar(var=cantidad):
                    var.set(var.get() + 1)

                def disminuir(var=cantidad):
                    var.set(max(0, var.get() - 1))

                ttk.Button(bloque_cantidad, text="-", width=2, command=disminuir).pack(side="left")
                cantidad_entry = tk.Entry(
                    bloque_cantidad,
                    textvariable=cantidad,
                    font=("Arial", 10),
                    width=3,
                    justify="center",
                    state="readonly"
                )
                cantidad_entry.pack(side="left", padx=2)
                ttk.Button(bloque_cantidad, text="+", width=2, command=aumentar).pack(side="left")

                def agregar(prod=prod, var=cantidad):
                    cant = var.get()
                    if cant <= 0:
                        return
                    desc = descripcion_entry.get("1.0", tk.END).strip()
                    if prod.codigo in carrito:
                        carrito[prod.codigo]["cantidad"] += cant
                        if desc:
                            carrito[prod.codigo]["descripcion"] = desc
                    else:
                        carrito[prod.codigo] = {"producto": prod, "cantidad": cant, "descripcion": desc}
                    var.set(0)
                    descripcion_entry.delete("1.0", tk.END)
                    actualizar_carrito()

                ttk.Button(bloque_cantidad, text="Agregar", command=agregar).pack(side="left", padx=5)


    # Botones de categoría — centrados y del mismo ancho
    bottom_buttons = tk.Frame(main_content_area, bg=FONDO)
    bottom_buttons.pack(pady=10)
    botones_categoria = tk.Frame(bottom_buttons, bg=FONDO)
    botones_categoria.pack()
    for cat in CATEGORIAS_PRINCIPALES:
        tk.Button(botones_categoria, text=cat, command=lambda c=cat: mostrar_categoria(c),
                  font=FUENTE, bg=COLOR_BOTON, fg="white", width=20, height=2).pack(side="left", padx=15)

    envio_frame = tk.Frame(main_content_area, bg=FONDO)
    envio_frame.pack(pady=10)
    tk.Label(envio_frame, text="Mesa:", bg=FONDO, font=FUENTE).pack()
    entrada_mesa = tk.Entry(envio_frame, font=FUENTE)
    entrada_mesa.pack()

    def enviar():
        mesa = entrada_mesa.get().strip()
        if not mesa:
            messagebox.showwarning("⚠️", "Ingrese el número de mesa")
            return
        pedido = Pedido(mesa=mesa)
        for data in carrito.values():
            for _ in range(data["cantidad"]):
                pedido.agregar_producto(data["producto"])


        if not pedido.items:
            messagebox.showwarning("⚠️", "Seleccione al menos un producto")
            return
        try:
            restaurante.enviar_pedido(pedido)
            messagebox.showinfo("✅", "Pedido enviado")
            entrada_mesa.delete(0, tk.END)
            descripcion_entry.delete("1.0", tk.END)
            carrito.clear()
            carrito_lista.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("❌", f"Error: {e}")

    tk.Button(envio_frame, text="Enviar Pedido", command=enviar,
              bg=COLOR_BOTON, fg="white", font=TEXTO_TITULO).pack(pady=5)

    tk.Button(envio_frame, text="Cerrar Sesión", command=lambda: (ventana.destroy(), return_callback()),
              bg="#333333", fg="white").pack()

    mostrar_categoria("Bebidas")
    ventana.mainloop()  