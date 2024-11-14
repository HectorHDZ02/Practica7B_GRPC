import grpc
from concurrent import futures
import shop_pb2
import shop_pb2_grpc

class ShopServicer(shop_pb2_grpc.ShopServiceServicer):
    def PurchaseItem(self, request, context):
        # Lógica para procesar la compra de un artículo
        # Esta es solo una implementación de ejemplo
        total_price = 10 * request.quantity  # Precio unitario de ejemplo
        return shop_pb2.PurchaseResponse(message="Artículo comprado exitosamente", total_price=total_price)

    def MakePayment(self, request, context):
        # Lógica para procesar el pago
        # Esta es solo una implementación de ejemplo
        success = True  # Simulando un pago exitoso
        return shop_pb2.PaymentResponse(message="Pago exitoso", success=success)

    def PlaceOrder(self, request, context):
        # Lógica para realizar un pedido
        # Esta es solo una implementación de ejemplo
        order_id = "123456"  # ID del pedido generado
        purchases = []
        total_price = 0
        for item in request.items:
            total_price += 10 * item.quantity  # Precio unitario de ejemplo
            purchases.append(shop_pb2.PurchaseResponse(message="Artículo comprado exitosamente", total_price=total_price))
        return shop_pb2.OrderResponse(order_id=order_id, purchases=purchases)

    def GetProductInfo(self, request, context):
        # Lógica para obtener información del producto
        # Aquí deberías tener una lógica para buscar el producto en tu base de datos o en algún otro lugar
        # Esta es solo una implementación de ejemplo
        product_info = {
            "123": {"name": "Producto 'Jabon ZOTE' ", "description": "producto de limpieza utilizado para la higiene personal y la limpieza doméstica.", "price": 140.0},
            "456": {"name": "Producto 'Auriculares SONY' ", "description": " Proporcionan una experiencia de escucha de alta calidad, conocidos por su innovación tecnológica y su excelente rendimiento de audio", "price": 1299.0},
            "789": {"name": "Producto 'Consola de Videojuegos XBOX S'", "description": "Xbox ha experimentado varias actualizaciones y mejoras, incluyendo la Xbox 360, Xbox One y la Xbox Series X|S. Las consolas Xbox ofrecen una experiencia de juego de alta calidad, con gráficos impresionantes, rendimiento rápido y una amplia gama de funciones y servicios. ", "price": 5999.0}
        }
        if request.product_id in product_info:
            product = product_info[request.product_id]
            return shop_pb2.ProductInfoResponse(name=product["name"], description=product["description"], price=product["price"])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Producto no encontrado")
            return shop_pb2.ProductInfoResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shop_pb2_grpc.add_ShopServiceServicer_to_server(ShopServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado. Escuchando en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
