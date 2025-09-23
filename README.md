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

cp ‪C:\Users\626\Downloads\4.png

## Задачи:
1. Создание ERD диаграммы для базы данных.
2. Разработка SQL-скриптов для создания базы данных и таблиц.
3. Реализация заданий в Jupyter Notebook с подключением к базе данных, вставкой и обновлением данных, а также визуализацией информации.

# Вариант №8

## Выполнение задания:
Для начала работы установим библиотеку psycopg2:
```python
%pip install psycopg2

```

И импортируем библиотеку psycopg2 для работы с PostgreSQL, класс Error для обработки ошибок при подключении к базе данных:
```python
import psycopg2
from psycopg2 import Error

```
## Задание 1. Создайте базу данных "medical_center" и таблицу "Staff".
Для выполнения задания перейдем в Visual Studio Code и напишем скрипт для подключения и создания новой базы данных "medical_center", а также для создания таблицы  Staff, предворительно подключившись к БД.
```python
import psycopg2

def get_connection(database_name):
    # Функция для получения подключения к базе данных
    connection = psycopg2.connect(user="postgres",
                                  password="1",
                                  host="localhost",
                                  port="5432",
                                  database="bi_student")
    return connection

def close_connection(connection):
    # Функция для закрытия подключения к базе данных
    if connection:
        connection.close()
        print("Соединение с PostgreSQL закрыто")

try:
    # Создание подключения к базе данных sql_case_bi_mgpu (база, с которой можно создавать другие базы)
    connection = psycopg2.connect(user="postgres",
                                  password="1",
                                  host="localhost",
                                  port="5432",
                                  database="bi_student")
    connection.autocommit = True  # Отключаем транзакцию для команды CREATE DATABASE
    cursor = connection.cursor()

    # ЗАДАНИЕ 1
    # Создайте базу данных "medical_center" и таблицу "Staff".
    cursor.execute("CREATE DATABASE medical_center;")
    print("База данных 'medical_center' успешно создана")

    # Закрытие текущего соединения для подключения к новой базе данных
    close_connection(connection)

    # Подключение к новой базе данных 'medical_center'
    connection = get_connection("medical_center")
    cursor = connection.cursor()


    # Создание таблицы Staff
    create_table_query = '''
    CREATE TABLE Staff (
        Staff_Id serial NOT NULL PRIMARY KEY,
        Staff_Name VARCHAR (100) NOT NULL,
        Position VARCHAR (100) NOT NULL,
        Specialization VARCHAR (100) NOT NULL,
        Departament VARCHAR (100) NOT NULL,
        Phone VARCHAR (20) NOT NULL,
        Email VARCHAR (100) NOT NULL

    );
    '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица 'Staff' успешно создана")
```
Отображение таблицы в pgAdmin:

![пр 7 фото таблиц](https://github.com/user-attachments/assets/2ef724da-2d54-435b-afa3-409a6e904895)


## Задание 2. Вставьте данные в таблицу "Staff" о 5 новых врачах.
Чтобы выполнить задание создаем новую строку и прописываем код для добавления данных о пяти новых врачах, добавляя их уже в созданную ранее таблицу.
```python
   # ЗАДАНИЕ 2 
    # Вставьте данные в таблицу "Staff" о 5 новых врачах.
    insert_query = '''
    INSERT INTO Staff (Staff_Id, Staff_Name, Position, Specialization, Departament, Phone, Email)
    VALUES
    (1, 'Иванова Анна Сергеевна', 'Врач-терапевт', 'Терапия', 'Терапевтическое отделение', '+79151234567', 'ivanova@medcenter.ru'),
    (2, 'Петров Дмитрий Игоревич', 'Хирург', 'Общая хирургия', 'Хирургическое отделение', '+79037654321', 'petrov@medcenter.ru'),
    (3, 'Сидорова Елена Владимировна', 'Медсестра', 'Сестринское дело', 'Кардиологическое отделение', '+79219876543', 'sidorova@medcenter.ru'),
    (4, 'Козлов Артем Александрович', 'Врач-невролог', 'Неврология', 'Неврологическое отделение', '+79164567890', 'kozlov@medcenter.ru'),
    (5, 'Михайлова Ольга Дмитриевна', 'Врач-педиатр', 'Педиатрия', 'Детское отделение', '+79031237890', 'mihailova@medcenter.ru');
    
    '''
    cursor.execute(insert_query)
    connection.commit()
    print("Данные успешно вставлены в таблицу 'Staff'")

except (Exception, psycopg2.Error) as error:
    print("Ошибка при подключении или работе с PostgreSQL:", error)

finally:
    # Закрытие подключения к базе данных
    if connection:
        close_connection(connection)
```

## Задание 3. Получите все записи о больнице с ID=4.
Составляем запрос для вывода всех записей о больнице с ID = 4.
```python
   # ЗАДАНИЕ 3
    # Получите все записи о больнице с ID=4

    # Для выполнения данного запроса, создадим таблицу "Hospital" и заполним ее данными

import psycopg2

def get_connection(database_name):
    # Функция для получения подключения к базе данных
    connection = psycopg2.connect(user="postgres",
                                  password="1",
                                  host="localhost",
                                  port="5432",
                                  database="bi_student")
    return connection

def close_connection(connection):
    # Функция для закрытия подключения к базе данных
    if connection:
        connection.close()
        print("Соединение с PostgreSQL закрыто")

try:
    # Создание подключения к базе данных sql_case_bi_mgpu (база, с которой можно создавать другие базы)
    connection = psycopg2.connect(user="postgres",
                                  password="1",
                                  host="localhost",
                                  port="5432",
                                  database="bi_student")
    connection.autocommit = True  # Отключаем транзакцию для команды CREATE DATABASE
    cursor = connection.cursor()


    # Подключение к новой базе данных 'medical_center'
    connection = get_connection("medical_center")
    cursor = connection.cursor()

    # Создание таблицы Hospital
    create_table_query = '''
    CREATE TABLE Hospital (
        Hospital_Id serial NOT NULL PRIMARY KEY,
        Hospital_Name VARCHAR (100) NOT NULL,
        Bed_Count serial
    );
    '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица 'Hospital' успешно создана")

    # Вставка данных в таблицу Hospital
    insert_query = '''
    INSERT INTO Hospital (Hospital_Id, Hospital_Name, Bed_Count)
    VALUES
    (1, 'Mayo Clinic', 200),
    (2, 'Cleveland Clinic', 400),
    (3, 'Johns Hopkins', 1000),
    (4, 'UCLA Medical Center', 1500);
    '''

    cursor.execute(insert_query)
    connection.commit()
    print("Данные успешно вставлены в таблицу 'Hospital'")

except (Exception, psycopg2.Error) as error:
    print("Ошибка при подключении или работе с PostgreSQL:", error)

finally:
    # Закрытие подключения к базе данных
    if connection:
        close_connection(connection)



    #  Выполним запрос для получения всех записей о больнице с ID=4

def get_connection(database_name):
    # Функция для получения подключения к базе данных
    connection = psycopg2.connect(user="postgres",
                                  password="1",
                                  host="localhost",
                                  port="5432",
                                  database="bi_student")
    return connection

def close_connection(connection):
    # Функция для закрытия подключения к базе данных
    if connection:
        connection.close()
        print("Соединение с PostgreSQL закрыто")

def get_hospital_detail(hospital_id):
    try:
        # Подключаемся к базе данных medical_center
        database_name = 'medical_center'
        connection = get_connection(database_name)
        cursor = connection.cursor()

        # Запрос для получения информации о больнице 
        select_query = """SELECT * FROM Hospital WHERE Hospital_Id = %s """
        cursor.execute(select_query, (hospital_id,))
        records = cursor.fetchall()

        # Вывод информации о больнице
        print("Печать записи о больнице:")
        for row in records:
            print("Hospital Id:", row[0])
            print("Hospital Name:", row[1])
            print("Bed Count:", row[2])

        # Закрытие подключения
        close_connection(connection)
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при получении данных:", error)

# Запросить данные о больнице с ID 4 
print("Упражнение 3. Чтение информации о больнице\n")
get_hospital_detail(4)
print("\n")
```
Получаем результат:

![пр 7 фото упр 3](https://github.com/user-attachments/assets/e521a6e0-d8c3-4979-a8c7-abc1afe810e0)


## Задание 4. Выполните запрос для получения врачей, специализирующихся на педиатрии.
```python
    # ЗАДАНИЕ 4
    # Выполните запрос для получения врачей, специализирующихся на педиатрии

import psycopg2

def get_connection(database_name):
    # Функция для получения подключения к базе данных
    connection = psycopg2.connect(user="postgres",
                                  password="1",
                                  host="localhost",
                                  port="5432",
                                  database="bi_student")
    return connection

def close_connection(connection):
    # Функция для закрытия подключения к базе данных
    if connection:
        connection.close()
        print("Соединение с PostgreSQL закрыто")

# Подключаемся к базе данных medical_center
database_name = 'medical_center'

def get_specialization_list(specialization):
    try:
        connection = get_connection(database_name)
        cursor = connection.cursor()

        # Ззапрос для получения списка врачей по специальности
        select_query = """SELECT * FROM Staff WHERE Specialization = %s """
        cursor.execute(select_query, (specialization,))
        records = cursor.fetchall()

        # Выводим информацию о врачах с указанной специальностью 
        print("Список врачей со специальностью:")
        for row in records:
            print("Staff Id:", row[0])
            print("Staff Name:", row[1])
            print("Position:", row[2])
            print("Specialization:", row[3])
            print("Departament:", row[4])
            print("Phone:", row[5])
            print("Email:", row[6])

        # Закрытие подключения
        close_connection(connection)
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при получении данных:", error)

# Получение списка врачей по заданной специальности 
print("Получить список врачей по заданной специальности\n")
get_specialization_list("Педиатрия")
print("\n")
```
Получаем результат:

![пр 7 фото упр 4](https://github.com/user-attachments/assets/0bf965d2-c928-490a-ba83-ee7785bbdaa1)


## Задание 5. Постройте график с данными о больницах, сортированных по количеству мест.
Напишем код для построения графика о больницах, сортированнных по количеству мест
```python
 # ЗАДАНИЕ 5
    # Построить график с данными о больницах, сортированных по количеству мест

import pandas as pd
import matplotlib.pyplot as plt

# Данные из таблицы Hospital
data = {
    'Hospital_Id': [1, 2, 3, 4],
    'Hospital_Name': ['Mayo Clinic', 'Cleveland Clinic', 'Johns Hopkins', 'UCLA Medical Center'],
    'Bed_Count': [200, 400, 1000, 1500]
}

# Создаем DataFrame и сортируем по Bed_Count
df = pd.DataFrame(data).sort_values('Bed_Count')

# Настройка стиля
plt.style.use('ggplot')
plt.figure(figsize=(10, 6))

# Создаем столбчатую диаграмму
bars = plt.barh(df['Hospital_Name'], df['Bed_Count'], color='skyblue')

# Добавляем значения на столбцы
for bar in bars:
    width = bar.get_width()
    plt.text(width + 20, bar.get_y() + bar.get_height()/2, 
             f'{int(width)}', 
             va='center')

# Настройки оформления
plt.title('Количество мест в больницах', pad=20, fontsize=14)
plt.xlabel('Количество мест')
plt.ylabel('Больница')
plt.tight_layout()

# Показать график
plt.show()
```
Получаем результат:

![График](https://github.com/user-attachments/assets/cdad84f3-82d1-43ff-841c-d3ace1eaf22f)


## Вывод
Научилась импортировать и экспортировать данные в базу данных SQL, обрела навыки загрузки данных из внешних источников в таблицы базы данных, а также экспорта данных из базы данных в различные форматы. Научилась работать с внешними данными, преобразовывать их в нужный формат и интегировать с существующими таблицами в базе данных.


## Структура репозитория:
- `ERD_diagram.png` — ERD диаграмма схемы базы данных.
- `create_db_and_tables.sql` — SQL скрипт для создания базы данных и таблиц.
- `Gubaidullina_Alina_Ilshatovna_pr7.ipynb` — Jupyter Notebook с выполнением всех заданий.

## Как запустить:
1. Установите PostgreSQL и настройте доступ к базе данных.
2. Выполните SQL-скрипт `create_db_and_tables.sql` для создания базы данных и таблиц.
3. Откройте и выполните Jupyter Notebook для проверки выполнения заданий.
