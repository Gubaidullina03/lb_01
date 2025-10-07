import grpc
import time
import fin_pb2
import fin_pb2_grpc

def run():
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = fin_pb2_grpc.StockTickerStub(channel)
            
            print("Connecting to Stock Ticker Server...")
            
            # Создаем генератор запросов
            def request_generator():
                tickers = ["AAPL", "GOOGL", "TSLA", "MSFT"]
                for ticker in tickers:
                    yield fin_pb2.TickerRequest(ticker_symbol=ticker)
                    time.sleep(3)
            
            # Отправляем запросы и получаем ответы
            responses = stub.SubscribeToStockUpdates(request_generator())
            
            for response in responses:
                print(f"\n📈 {response.ticker_symbol}:")
                print(f"   Price: ${response.current_price:.2f}")
                print(f"   Change: {response.price_change:+.2f} ({response.change_percent:+.2f}%)")
                print(f"   Volume: {response.volume:,}")
                print(f"   Time: {time.strftime('%H:%M:%S', time.localtime(response.timestamp))}")
                
    except grpc.RpcError as e:
        print(f"RPC error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()