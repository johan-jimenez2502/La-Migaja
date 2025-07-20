import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import winsound  # Solo funciona en Windows

def abrir_ventana_pago_efectivo(total_a_pagar):
    # Ventana de pago
    ventana = tk.Toplevel()
    ventana.title("Pago en Efectivo")
    ventana.geometry("400x300")
    ventana.configure(bg="#F5E9CC")

    # 🧾 Título
    tk.Label(ventana, text="💵 Pago en Efectivo", font=("Helvetica", 16, "bold"),
             bg="#f0e6d2", fg="#6a3d2c").pack(pady=10)

    # Total a pagar
    tk.Label(ventana, text=f"Total a pagar: ${total_a_pagar:.2f}",
             font=("Helvetica", 13), bg="#f0e6d2").pack(pady=5)

    # Entrada de efectivo recibido
    tk.Label(ventana, text="Efectivo recibido:", bg="#f0e6d2").pack()
    entrada_efectivo = tk.Entry(ventana, font=("Helvetica", 12))
    entrada_efectivo.pack(pady=5)

    # Cambio
    label_cambio = tk.Label(ventana, text="Cambio: $0.00", font=("Helvetica", 13, "bold"), bg="#f0e6d2")
    label_cambio.pack(pady=10)

    # Bombillo apagado
    canvas_bombillo = tk.Canvas(ventana, width=40, height=40, bg="#f0e6d2", highlightthickness=0)
    bombillo = canvas_bombillo.create_oval(5, 5, 35, 35, fill="gray")
    canvas_bombillo.pack(pady=10)

    def calcular_cambio():
        try:
            efectivo = float(entrada_efectivo.get())
            cambio = efectivo - total_a_pagar

            if cambio < 0:
                messagebox.showwarning("Pago insuficiente", "El monto recibido no cubre el total.")
                return

            # Mostrar cambio
            label_cambio.config(text=f"Cambio: ${cambio:.2f}")

            # Encender bombillo
            canvas_bombillo.itemconfig(bombillo, fill="yellow")

            # Sonido de caja
            try:
                winsound.Beep(800, 200)  # Beep simple (frecuencia, duración)
                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            except:
                print("Sonido no disponible.")

            # Mensaje
            messagebox.showinfo("Pago procesado", "¡Caja abierta y pago completado!")
            ventana.destroy()

        except ValueError:
            messagebox.showerror("Entrada inválida", "Por favor, ingresa un número válido.")

    # Botón pagar
    tk.Button(ventana, text="💰 Cobrar", font=("Helvetica", 12), bg="#4caf50", fg="white",
              command=calcular_cambio).pack(pady=10)

    # Cerrar
    tk.Button(ventana, text="Cancelar", command=ventana.destroy,
              bg="#6c757d", fg="white").pack(pady=5)

    ventana.transient()
    ventana.grab_set()
    ventana.focus_set()
