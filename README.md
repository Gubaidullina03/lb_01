# pr_07
# Работа с внешними приложениями.

## Цель:
Научиться импортировать и экспортировать данные в базу данных SQL. Работа включает в себя загрузку данных из внешних источников в таблицы базы данных, а также экспорт данных из базы данных в различные форматы. Работа с внешними данными, преобразование их в нужный формат и интеграция с существующими таблицами в базе данных.

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
Отображение таблицы в pgAdmin
(/пр 7 фото таблиц.png)
(C:\Users\626\Downloads\пр 7 фото таблиц.png)


## Структура репозитория:
- `ERD_diagram.png` — ERD диаграмма схемы базы данных.
- `create_db_and_tables.sql` — SQL скрипт для создания базы данных и таблиц.
- `Gubaidullina_Alina_Ilshatovna.ipynb` — Jupyter Notebook с выполнением всех заданий.

## Как запустить:
1. Установите PostgreSQL и настройте доступ к базе данных.
2. Выполните SQL-скрипт `create_db_and_tables.sql` для создания базы данных и таблиц.
3. Откройте и выполните Jupyter Notebook для проверки выполнения заданий.
