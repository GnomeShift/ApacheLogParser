

# ApacheLogParser
Парсер access.log'а Apache с сохранением логов в БД

## Установка и запуск
1. Клонируйте репозиторий:
```git clone https://github.com/GnomeShift/ApacheLogParser.git```

2. Перейдите в каталог проекта:
```cd ApacheLogParser```

3. Установите [необходимые зависимости](./requirements.txt):
```pip install -r requirements.txt```

4. Отредактируйте [конфиг](https://github.com/GnomeShift/ApacheLogParser#Конфигурация):

5. **Создайте новую БД**:

6. Запустите приложение:
```python3 app.py```

## Конфигурация
Пример конфигурации по умолчанию.
В комментариях указаны допустимые значения некоторых параметров:
```yaml
# Данные для подключения к БД
database:
  db_name: parser
  db_user: postgres
  db_password: pass
  db_host: localhost
  db_port: 5432
  db_engine: postgresql # postgresql/mysql

# Изменение префикса API
api:
  api_prefix: /api

logging:
  logging_level: DEBUG # Уровень логирования приложения (DEBUG, FATAL, ERROR, WARNING, INFO, OFF)

# Отладка Flask
app:
  debug: False

# Путь к файлу access.log
access_log:
    access_log_file: access.log

# Вспомогательные функции
structure:
    disable_db_creation: False # Отключение автосоздания таблицы в БД
    table_name: apache_logs # Имя создаваемой таблицы
```

## Требования
1. Python 3.9+
2. PostgreSQL/MySQL
3. Браузер для отправки HTTP-запросов к API

## Структура
Проект состоит из следующих файлов:
* `app.py`: Главный файл приложения.
* `config.py`: Импорт yaml-конфигурации в python.
* `create_db.py`: Автосоздание структуры БД.
* `db.py`: Взаимодействие с БД.
* `parser.py`: Функции для парсинга данных.

## Дополнительно
API доступен по адресу:
>localhost:5000

Логи приложения находятся в файле **logs.log**

Для удобства, файл **access.log** уже загружен в каталог проекта

## Что доступно в ApacheLogParser?
На данный момент доступен только парсер access.log
