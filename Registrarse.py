import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Conexion_fb import db

# Colores personalizados
COLOR_FONDO = "#f1ddbf"
COLOR_PRIMARIO = "#8B2F23"
COLOR_SECUNDARIO = "#40754C"

def ventana_registro(ventana_login, return_to_login_callback):

    ventana = tk.Toplevel()
    ventana.title("📝 Registrar Nuevo Usuario")
    ventana.geometry("600x800")
    ventana.configure(bg=COLOR_FONDO)
    ventana.iconbitmap("Logo_migaja.ico")
    ventana.resizable(False, False)

    # Logo
    try:
        imagen_logo = Image.open("Logo_migaja.jpg")
        imagen_logo = imagen_logo.resize((150, 150), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(imagen_logo)
        tk.Label(ventana, image=logo, bg=COLOR_FONDO).pack(pady=(20, 10))
        ventana.logo = logo  # Guardar referencia
    except Exception as e:
        print("No se pudo cargar el logo:", e)

    # Título
    tk.Label(ventana, text="Registro de Usuario", font=("Times New Roman", 18, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRIMARIO).pack(pady=(0, 20))

    # Campos de entrada
    def crear_campo(texto, show=None):
        tk.Label(ventana, text=texto, font=("Times New Roman", 11, "bold"),
                 bg=COLOR_FONDO, anchor="w").pack(pady=(5, 0), padx=30, fill="x")
        entrada = tk.Entry(ventana, font=("Times New Roman", 12), show=show)
        entrada.pack(padx=30, pady=5, fill="x")
        return entrada

    entrada_nombre = crear_campo("Nombre completo:")
    entrada_usuario = crear_campo("Usuario:")
    entrada_contraseña = crear_campo("Contraseña:", show="*")
    entrada_confirmar = crear_campo("Confirmar contraseña:", show="*")

    # Selección de rol
    tk.Label(ventana, text="Rol:", font=("Times New Roman", 11, "bold"),
             bg=COLOR_FONDO, anchor="w").pack(pady=(10, 0), padx=30, fill="x")
    rol_var = tk.StringVar(value="Mesero")
    opciones_rol = ["Mesero", "Cocinero", "Administrador"]
    opcion_menu = tk.OptionMenu(ventana, rol_var, *opciones_rol)
    opcion_menu.config(font=("Times New Roman", 11), bg="white", relief="flat")
    opcion_menu.pack(padx=30, pady=5, fill="x")

    # Función de registro
    def registrar():
        nombre = entrada_nombre.get().strip()
        usuario = entrada_usuario.get().strip()
        contraseña = entrada_contraseña.get().strip()
        confirmar = entrada_confirmar.get().strip()
        rol = rol_var.get()

        if not all([nombre, usuario, contraseña, confirmar]):
            messagebox.showwarning("⚠️", "Todos los campos son obligatorios.")
            return
        if contraseña != confirmar:
            messagebox.showwarning("⚠️", "Las contraseñas no coinciden.")
            return

        try:
            if db.collection("usuarios").document(usuario).get().exists:
                messagebox.showerror("❌", "El usuario ya está registrado.")
                return

            db.collection("usuarios").document(usuario).set({
                "nombre": nombre,
                "contraseña": contraseña,
                "rol": rol
            })

            messagebox.showinfo("✅", "Usuario registrado exitosamente.")
            ventana.destroy()
            ventana_login.deiconify()

        except Exception as e:
            messagebox.showerror("❌ Error de conexión", str(e))

    # Botón registrar
    tk.Button(ventana, text="Registrar", command=registrar,
              bg=COLOR_SECUNDARIO, fg="white", font=("Times New Roman", 12, "bold"),
              height=2).pack(pady=(25, 10), padx=50, fill="x")

    # Botón cancelar
    tk.Button(ventana, text="Cancelar", command=lambda: [ventana.destroy(), ventana_login.deiconify()],
              bg=COLOR_PRIMARIO, fg="white", font=("Times New Roman", 12, "bold"),
              height=2).pack(pady=(0, 20), padx=50, fill="x")

    # Cerrar ventana con la X
    ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), ventana_login.deiconify()])