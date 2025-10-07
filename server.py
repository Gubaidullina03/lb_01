import grpc
from concurrent import futures
import time
import random
import fin_pb2
import fin_pb2_grpc

class StockTickerServicer(fin_pb2_grpc.StockTickerServicer):
    def SubscribeToStockUpdates(self, request_iterator, context):
        """Bidirectional streaming RPC"""
        print("Client connected to stock updates stream")
        
        try:
            for ticker_request in request_iterator:
                # Проверяем, что поле существует
                if hasattr(ticker_request, 'ticker_symbol'):
                    symbol = ticker_request.ticker_symbol
                    print(f"Received subscription for: {symbol}")
                    
                    # Отправляем обновления для этого тикера
                    for i in range(5):  # 5 обновлений на тикер
                        if not context.is_active():
                            print("Client disconnected")
                            return
                        
                        # Генерируем данные акции
                        base_price = random.uniform(100, 500)
                        current_price = round(base_price + random.uniform(-5, 5), 2)
                        price_change = round(current_price - base_price, 2)
                        change_percent = round((price_change / base_price) * 100, 2)
                        
                        # Создаем ответ
                        update = fin_pb2.StockUpdate(
                            ticker_symbol=symbol,
                            current_price=current_price,
                            price_change=price_change,
                            change_percent=change_percent,
                            timestamp=int(time.time()),
                            volume=random.randint(1000, 100000)
                        )
                        
                        print(f"Sending update for {symbol}: ${current_price}")
                        yield update
                        time.sleep(2)  # Пауза между обновлениями
                else:
                    print("Invalid request: missing ticker_symbol")
                    
        except Exception as e:
            print(f"Error in stream: {e}")
            raise

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    fin_pb2_grpc.add_StockTickerServicer_to_server(
        StockTickerServicer(), server
    )
    
    port = 50051
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started on port {port}")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()