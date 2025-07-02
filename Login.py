import tkinter as tk
from tkinter import messagebox
from Mesero import ventana_mesero
from Cocinero import ventana_cocinero
from Conexion_fb import db
from Clases import Restaurante

restaurante = Restaurante(db)

# --- FUNCIÓN PRINCIPAL ---
def iniciar_app():
    def login():
        usuario = entrada_usuario.get().strip()
        contraseña = entrada_contrasena.get().strip()
        rol = rol_seleccionado.get()

        if not usuario or not contraseña or not rol:
            messagebox.showwarning("⚠️", "Debes completar todos los campos.")
            return

        ref = db.collection("usuarios").document(usuario).get()
        if ref.exists:
            datos = ref.to_dict()
            if datos["contraseña"] == contraseña and datos["rol"] == rol:
                ventana.destroy()
                if rol == "Mesero":
                    ventana_mesero(restaurante)
                elif rol == "Cocinero":
                    ventana_cocinero(restaurante)
            else:
                messagebox.showerror("❌", "Contraseña o rol incorrecto.")
        else:
            messagebox.showerror("❌", "Usuario no encontrado.")

    def registrar():
        usuario = entrada_usuario.get().strip()
        contraseña = entrada_contrasena.get().strip()
        rol = rol_seleccionado.get()

        if not usuario or not contraseña or not rol:
            messagebox.showwarning("⚠️", "Completa todos los campos para registrarte.")
            return

        ref = db.collection("usuarios").document(usuario)
        if ref.get().exists:
            messagebox.showerror("❌", "El usuario ya existe.")
        else:
            ref.set({
                "contraseña": contraseña,
                "rol": rol
            })
            messagebox.showinfo("✅", "Usuario registrado exitosamente.")

    # --- VENTANA ---
    ventana = tk.Tk()
    ventana.title("🔐 Login - La Migaja")
    ventana.geometry("350x300")

    tk.Label(ventana, text="Usuario:").pack(pady=5)
    entrada_usuario = tk.Entry(ventana)
    entrada_usuario.pack()

    tk.Label(ventana, text="Contraseña:").pack(pady=5)
    entrada_contrasena = tk.Entry(ventana, show="*")
    entrada_contrasena.pack()

    tk.Label(ventana, text="Rol:").pack(pady=5)
    rol_seleccionado = tk.StringVar()
    opciones = tk.OptionMenu(ventana, rol_seleccionado, "Mesero", "Cocinero")
    opciones.pack()

    tk.Button(ventana, text="Ingresar", command=login, bg="#40754C", fg="white").pack(pady=10)
    tk.Button(ventana, text="Registrarse", command=registrar, bg="#8B2F23", fg="white").pack()

    ventana.mainloop()


if __name__ == "__main__":
    iniciar_app()
