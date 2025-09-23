# lb_01
# Введение в распределенные системы.

## Архитектура
1. Компоненты
Сервер (Server). Это независимое приложение (server.py), которое выполняет основную "бизнес-логику" обработки биржевых данных.

Возможности:
- Предоставляет сервис. Он реализует и "выставляет наружу" сервис StockTicker, определенный в контракте (fin.proto).
- Обрабатывает запросы. Он слушает входящие сетевые соединения на определенном порту (50051) и обрабатывает вызовы от клиентов.
- Выполняет логику. Генерирует реалистичные данные об акциях (цены, изменения, объемы), имитируя реальную биржевую активность.
- Bidirectional Streaming. Поддерживает двустороннюю потоковую передачу данных в реальном времени.
- Асинхронность. Использует пул потоков (futures.ThreadPoolExecutor) для одновременной обработки нескольких клиентских подключений.

Клиент (Client). Это приложение (client.py), которое потребляет функциональность, предоставляемую сервером.

Возможности:
- Инициирует соединение. Устанавливает соединение с сервером по известному адресу (localhost:50051).
- Вызывает удаленные методы. Обращается к методам сервера (SubscribeToStockUpdates) через streaming RPC.
- Динамическая подписка. Может добавлять новые тикеры для отслеживания во время работы соединения.
- Обрабатывает потоковые ответы. Получает и отображает в реальном времени данные об акциях, возвращаемые сервером.
- Обработка ошибок. Корректно обрабатывает разрывы соединения и сетевые ошибки.

2. Взаимодействие и контракт
Ключевым элементом архитектуры является сервисный контракт (Service Contract), определенный в файле fin.proto.
- Роль контракта. Этот файл является "единым источником правды" для API. Он строго описывает:
Какие сервисы доступны (StockTicker).
Какие методы можно вызвать у каждого сервиса (SubscribeToStockUpdates).
Какие данные (сообщения) эти методы принимают (TickerRequest) и возвращают (StockUpdate).
Тип коммуникации (bidirectional streaming RPC).


<img width="659" height="568" alt="4" src="https://github.com/user-attachments/assets/ca717a6c-e40a-439c-8b1e-11d011f9e58c" />

## Технологический стек (Technology Stack)
1. Язык определения интерфейсов (IDL): Protocol Buffers (Protobuf)
2. Фреймворк RPC: gRPC
3. Транспортный протокол: HTTP/2
4. Язык программирования: Python 3
5. Тип коммуникации: Bidirectional Streaming RPC
6. Ключевые библиотеки Python: grpcio - основная библиотека gRPC для Python; grpcio-tools - инструменты для компиляции proto-файлов; concurrent.futures - для многопоточной обработки запросов; random - для генерации реалистичных данных акций; time - для работы с временными метками и задержками
7. Среда выполнения и изоляция:
   - ОС: Ubuntu/Linux
   - Виртуальное окружение (venv) - инструмент для изоляции зависимостей проекта, гарантирующий, что установленные пакеты (grpcio и др.) не будут конфликтовть с системными или другими проектами
   - Порт: 50051 (для gRPC соединений)

# Шаг 1: подготовка окружения (Ubuntu 20.04+)
Обновим пакеты и установим Python:

```python
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```
Затем создадим и активируем виртуальное окружение:

```python
mkdir grpc_weather_lab
cd grpc_weather_lab
python3 -m venv venv
source venv/bin/activate
```

Теперь в начале строки терминала увидим (venv).
Установим библиотеки gRPC:

```python
pip install grpcio grpcio-tools
```

<img width="515" height="301" alt="1" src="https://github.com/user-attachments/assets/5670da31-09c6-47ed-909f-e273f5f099e5" />


# Шаг 2: определение сервиса в .proto файле

```python
syntax = "proto3";

message TickerRequest {
    string ticker_symbol = 1;
}

message StockUpdate {
    string ticker_symbol = 1;
    double current_price = 2;
    double price_change = 3;
    double change_percent = 4;
    int64 timestamp = 5;
    int32 volume = 6;
}

service StockTicker {
    rpc SubscribeToStockUpdates(stream TickerRequest) returns (stream StockUpdate);
}
```


# Шаг 3: генерация кода
Выполним в терминале команду для генерации Python-классов из .proto файла:

```python
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. fin.proto
```

-I. указывает, где искать импорты (в текущей директории).
--python_out=. генерирует код для сообщений (fin_pb2.py).
--grpc_python_out=. генерирует код для сервиса (fin_pb2_grpc.py).

В папке появятся два новых файла: fin_pb2.py и fin_pb2_grpc.py


<img width="180" height="159" alt="2" src="https://github.com/user-attachments/assets/1db7c000-5b17-4f2d-b4b7-c64b58026268" />

# Шаг 4: реализация сервера
Создадим файл server.py и напишим код сервера:

```python
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
```

Создадим файл client.py и напишим код клиента:

```python
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
```

# Шаг 5: запуск и проверка.
Откроем первый терминал, активируем виртуальное окружение (source venv/bin/activate) и запустим сервер:

```python
python server.py
```

<img width="427" height="222" alt="Screenshot_152" src="https://github.com/user-attachments/assets/279a9d75-7a94-47b5-bf7d-1fca0541fc60" />

Откроем второй терминал, активируем то же виртуальное окружение и запустим клиент:

```python
python client.py
```

<img width="464" height="252" alt="Screenshot_153" src="https://github.com/user-attachments/assets/dc3caf75-c955-416d-a4a9-54fde20e2de7" />


# Вывод
В ходе выполнения лабораторной работы был успешно разработан и протестирован клиент-серверный сервис StockTicker с использованием технологии gRPC. В процессе работы были освоены и продемонстрированы следующие ключевые навыки:

1. Определение контракта сервиса
С помощью языка определения интерфейсов Protocol Buffers (в файле fin.proto) была создана строгая схема взаимодействия, включающая сервисы, методы и типы сообщений. Это обеспечивает строгую типизацию и независимость от языка реализации.
2. Автоматическая генерация кода
Использовались инструменты grpcio-tools для автоматической генерации Python-кода из .proto-файла, что значительно упростило и ускорило разработку, создав готовый каркас для клиента и сервера.
3. Реализация Bidirectional Streaming RPC
Был успешно реализован Bidirectional Streaming RPC для метода SubscribeToStockUpdates, который позволяет:
- Клиенту динамически подписываться на новые тикеры акций
- Серверу отправлять обновления котировок в реальном времени
- Обеим сторонам обмениваться данными асинхронно и независимо
4. Создание и запуск компонентов
Были написаны и запущены полноценные серверная и клиентская части приложения:
- Сервер настроен на асинхронную обработку запросов с использованием пула потоков
- Клиент продемонстрировал способность корректно обрабатывать потоковые данные от сервера
- Реализована генерация реалистичных биржевых данных с имитацией изменений цен

# Источники



