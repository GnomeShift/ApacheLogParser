import yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Данные для подключения
DB_NAME = config["database"]["db_name"]
DB_USER = config["database"]["db_user"]
DB_PASSWORD = config["database"]["db_password"]
DB_HOST = config["database"]["db_host"]
DB_PORT = config["database"]["db_port"]
DB_ENGINE = config["database"]["db_engine"]

if DB_ENGINE == "postgresql":
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_ENGINE == "mysql":
    DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Настройки API
API_PREFIX = config["api"]["api_prefix"]

# Уровень логирования
LOGGING_LEVEL = config["logging"]["logging_level"]

# Отладка Flask
DEBUG = config["app"]["debug"]

# Путь к access.log
ACCESS_LOG_FILE = config["access_log"]["access_log_file"]

# Автоматическое создание базы данных
DISABLE_DB_CREATION = config["structure"]["disable_db_creation"]

# Имя таблицы с логами
TABLE_NAME = config["structure"]["table_name"]