import tkinter as tk
from tkinter import messagebox
from Registrarse import ventana_registro
from Conexion_fb import db
from Clases import Restaurante

restaurante = Restaurante(db)

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("🔐 Login - La Migaja")
    ventana.geometry("350x250")
    ventana.configure(bg="#F5E9CC")
    ventana.iconbitmap("Logo_migaja.ico")
    ventana.resizable(False, False)

    def abrir_registro():
        ventana.withdraw()
        ventana_registro(ventana)

    def login():
        usuario = entrada_usuario.get().strip()
        contraseña = entrada_contrasena.get().strip()

        if not usuario or not contraseña:
            messagebox.showwarning("⚠️", "Debes completar todos los campos.")
            return

        try:
            user_ref = db.collection("usuarios").document(usuario).get()
            
            if user_ref.exists:
                user_data = user_ref.to_dict()
                if user_data["contraseña"] == contraseña:
                    ventana.destroy()
                    if user_data["rol"] == "Mesero":
                        from Mesero import ventana_mesero
                        ventana_mesero(restaurante, user_data["nombre"])
                    else:
                        from Cocinero import ventana_cocinero
                        ventana_cocinero(restaurante, user_data["nombre"])
                else:
                    messagebox.showerror("❌ Error", "Contraseña incorrecta")
            else:
                messagebox.showerror("❌ Error", "Usuario no registrado")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error de conexión: {str(e)}")

    # Widgets
    tk.Label(ventana, text="Usuario:", bg="#F5E9CC").pack(pady=5)
    entrada_usuario = tk.Entry(ventana)
    entrada_usuario.pack()

    tk.Label(ventana, text="Contraseña:", bg="#F5E9CC").pack(pady=5)
    entrada_contrasena = tk.Entry(ventana, show="*")
    entrada_contrasena.pack()

    # Botones
    tk.Button(ventana, text="Ingresar", command=login, bg="#8B2F23", fg="white", width=15).pack(pady=10)
    tk.Button(ventana, text="Registrar nuevo usuario", command=abrir_registro, bg="#40754C", fg="white").pack()

    ventana.mainloop()

if __name__ == "__main__":
    iniciar_app()