
# 🥖 La Migaja: Sistema de Gestión para Restaurante Colombiano 🇨🇴

La Migaja Se trata de una aplicación gráfica hecha con Python que permite gestionar las operaciones internas de un restaurante colombiano, desde la toma de pedidos hasta la caja registradora.

Este sistema fue pensado para mejorar la eficiencia del restaurante **La Migaja**, automatizando los procesos manuales y permitiendo un manejo más organizado de pedidos, cocina, ventas y cobros, todo desde una interfaz visual clara y amigable.

---

## 📲 ¿Qué hace la aplicación?

🔐 **Inicio de sesión por rol:**  
Usuarios se registran como *mesero*, *cocinero* o *administrador* a través de Firebase Authentication.

🍽️ **Vista del mesero:**  
Permite seleccionar productos del menú por categorías y subcategorías, agregarlos con cantidad y observaciones, y enviar el pedido con hora y número de mesa.  
✅ El menú está organizado por:
- Gourmet (Orinoquía, Andina, Caribe, Pacífica)
- Bebidas (Frías, Calientes, Jugos, Alcohólicas)
- Entradas (Frías, Calientes)

👨‍🍳 **Vista del cocinero:**  
Muestra los pedidos pendientes y permite marcarlos como *servidos*. También se puede consultar un historial de pedidos anteriores con hora y detalles.

🧾 **Vista del administrador:**  
Módulo dividido en:
- **Caja:** Registro de pagos (efectivo y tarjeta), con cálculo de cambio y efecto de sonido.
- **Gestión del menú:** Agregar nuevos platos.
- **Ventas del día:** Contador de productos vendidos y suma total en pesos.

---

## 🧭 Guía Visual del Sistema (Diseño en Consola)

### 🔐 Pantalla de Login

```
┌─────────────────────────────────────────────┐
│                   La Migaja                 │
│             Cocina Colombiana 🇨🇴            │
│                                             │
│             🔐 Inicio de Sesión             │
│                                             │
│ Usuario:       [_______________________]    │
│ Contraseña:    [_______________________]    │
│                                             │
│  [ Ingresar ]         [ Registrar nuevo ]   │
└─────────────────────────────────────────────┘
```

---

### 🧾 Vista del Mesero

```
┌─────────────────────────────────────────────────────────────────────┐
│                  La Migaja - Bienvenido, johan jimenez             │
│────────────────────────────────────────────────────────────────────│
│ 📋 Calientes                                                        │
│ - Arepitas de queso ahumado         $22000   [ - ][0][+][Agregar]  │
│ - Empanadas con ají de la casa      $19000   [ - ][0][+][Agregar]  │
│ - Carimañolas rellenas              $20000   [ - ][0][+][Agregar]  │
│────────────────────────────────────────────────────────────────────│
│ [ Bebidas ] [ Entradas ] [ Gourmet ]    Mesa: [____]               │
│                                                             🧾      │
│                  🟩 Enviar Pedido         🟥 Cerrar Sesión         │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 👨‍🍳 Vista del Cocinero

```
┌──────────────────────────────────────────────────────────────────────┐
│        🔍 Pedidos en cocina - andres muñoz                           │
│──────────────────────────────────────────────────────────────────────│
│ 🧾 Pedido #25 | Mesa: 712 | 🕒 08:34:34  ✅ Servido                    │
│  - Carimañolas rellenas (x3)                                         │
│  - Arepitas de queso (x2)                                            │
│                                                                      │
│ 🧾 Pedido #26 | Mesa: 120 | 🕒 12:17:10 ✅ Servido                    │
│  - Chuleta Valluna, Arroz del Valle, etc.                            │
│                                                                      │
│ 🧾 Pedido #27 | Mesa: 24 | 🕒 12:42:01 ✅ Servido                     │
│  - Café filtrado (x5)                                                │
│──────────────────────────────────────────────────────────────────────│
│ 🔄 Actualizar       📜 Pedidos Anteriores       🟥 Cerrar Sesión      │
└──────────────────────────────────────────────────────────────────────┘
```

---

### 💳 Vista de Caja

```
┌─────────────────────────────────────────────┐
│               La Migaja 🧾                  │
│          Caja - Registro de Pago            │
│─────────────────────────────────────────────│
│ 📋 Pedidos Servidos                         │
│ #26 | Mesa 120 | $191000 | 2025-07-16       │
│ #24 | Mesa 615 |  $74000 | 2025-07-16       │
│ #25 | Mesa 712 | $101000 | 2025-07-16       │
│─────────────────────────────────────────────│
│ 💵 Total: $0.00   Cambio: $0.00             │
│ [ Efectivo ] [ Tarjeta ]                    │
│ ✅ [ Pagar Ahora ]                          │
│ 🔙 [ Volver al menú anterior ]              │
└─────────────────────────────────────────────┘
```

---

### 🛠️ Panel del Administrador

```
┌─────────────────────────────────────────────┐
│               La Migaja                     │
│ Bienvenido, johan andres jimenez muñoz      │
│       Continúa con la administración        │
│                                             │
│    [ Agregar menú ]                         │
│    [ Ver Ventas del Día ]                   │
│    [ Ver Caja ]                             │
└─────────────────────────────────────────────┘
```

---

## 🧠 Tecnologías y librerías

- **Python 3.12**
- **Tkinter** (interfaz gráfica)
- **Firebase Authentication** (login y registro)
- **Firebase Firestore** (almacenamiento de pedidos y productos)
- **Pillow** (para cargar imágenes del menú)
- **Winsound** (sonido de caja registradora)

---

## 💻 Instalación

```bash

# Ingresar al directorio
cd la-migaja

# Instalar dependencias
pip install -r requirements.txt

# Asegúrate de tener el archivo 'serviceAccountKey.json' en la raíz del proyecto

# Ejecutar la app
python main.py
```
