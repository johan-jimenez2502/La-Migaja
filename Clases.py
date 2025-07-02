from Conexion_fb import db

class Producto:
    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} - ${self.precio}"

class Pedido:
    def __init__(self, mesa=""):
        self.items = []
        self.total = 0
        self.estado = "pendiente"
        self.mesa = mesa

    def agregar_producto(self, producto):
        self.items.append(producto)
        self.total += producto.precio

    def a_dict(self):
        return {
            "items": [vars(p) for p in self.items],
            "total": self.total,
            "estado": self.estado,
            "mesa": self.mesa
        }

class Restaurante:
    def __init__(self, db):
        self.db = db

    def obtener_menu(self):
        productos = []
        docs = self.db.collection("menu").stream()
        for doc in docs:
            data = doc.to_dict()
            producto = Producto(data["codigo"], data["nombre"], data["precio"])
            productos.append(producto)
        return productos

    def enviar_pedido(self, pedido):
        self.db.collection("pedidos").add(pedido.a_dict())

    def obtener_pedidos_pendientes(self):
        pedidos = []
        docs = self.db.collection("pedidos").where("estado", "==", "pendiente").stream()
        for doc in docs:
            pedido = doc.to_dict()
            pedido["id"] = doc.id
            pedidos.append(pedido)
        return pedidos

    def marcar_pedido_servido(self, pedido_id):
        self.db.collection("pedidos").document(pedido_id).update({
            "estado": "servido"
        })

    def obtener_pedido_por_id(self, pedido_id):
        doc = self.db.collection("pedidos").document(pedido_id).get()
        if doc.exists:
            pedido = doc.to_dict()
            pedido["id"] = pedido_id
            return pedido
        return None

    def obtener_inventario(self):
        inventario = {}
        docs = self.db.collection("inventario").stream()
        for doc in docs:
            data = doc.to_dict()
            inventario[data["codigo"]] = data.get("stock", 0)
        return inventario

    def descontar_inventario(self, pedido):
        inventario_ref = self.db.collection("inventario")
        for item in pedido["items"]:
            codigo = item.get("codigo")
            if codigo:
                doc_ref = inventario_ref.document(codigo)
                doc = doc_ref.get()
                if doc.exists:
                    stock_actual = doc.to_dict().get("stock", 0)
                    if stock_actual > 0:
                        doc_ref.update({"stock": stock_actual - 1})
