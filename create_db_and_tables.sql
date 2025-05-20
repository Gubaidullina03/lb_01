 # Создание базы данных medical_center  
     
     CREATE DATABASE medical_center;

# Создание таблицы Staff
    
    CREATE TABLE Staff (
        Staff_Id serial NOT NULL PRIMARY KEY,
        Staff_Name VARCHAR (100) NOT NULL,
        Position VARCHAR (100) NOT NULL,
        Specialization VARCHAR (100) NOT NULL,
        Departament VARCHAR (100) NOT NULL,
        Phone VARCHAR (20) NOT NULL,
        Email VARCHAR (100) NOT NULL

    );

# Заполнение таблицы Staff

    INSERT INTO Staff (Staff_Id, Staff_Name, Position, Specialization, Departament, Phone, Email)
    VALUES
    (1, 'Иванова Анна Сергеевна', 'Врач-терапевт', 'Терапия', 'Терапевтическое отделение', '+79151234567', 'ivanova@medcenter.ru'),
    (2, 'Петров Дмитрий Игоревич', 'Хирург', 'Общая хирургия', 'Хирургическое отделение', '+79037654321', 'petrov@medcenter.ru'),
    (3, 'Сидорова Елена Владимировна', 'Медсестра', 'Сестринское дело', 'Кардиологическое отделение', '+79219876543', 'sidorova@medcenter.ru'),
    (4, 'Козлов Артем Александрович', 'Врач-невролог', 'Неврология', 'Неврологическое отделение', '+79164567890', 'kozlov@medcenter.ru'),
    (5, 'Михайлова Ольга Дмитриевна', 'Врач-педиатр', 'Педиатрия', 'Детское отделение', '+79031237890', 'mihailova@medcenter.ru');

# Создание таблицы Hospital

    CREATE TABLE Hospital (
        Hospital_Id serial NOT NULL PRIMARY KEY,
        Hospital_Name VARCHAR (100) NOT NULL,
        Bed_Count serial
    );
# Заполнение таблицы Hospital

    INSERT INTO Hospital (Hospital_Id, Hospital_Name, Bed_Count)
    VALUES
    (1, 'Mayo Clinic', 200),
    (2, 'Cleveland Clinic', 400),
    (3, 'Johns Hopkins', 1000),
    (4, 'UCLA Medical Center', 1500);