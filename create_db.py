import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text
from config import DISABLE_DB_CREATION, TABLE_NAME

# Загрузка config.yaml
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Получение параметров из конфиг-файла
db_name = config["database"]["db_name"]
db_user = config["database"]["db_user"]
db_password = config["database"]["db_password"]
db_host = config["database"]["db_host"]
db_port = config["database"]["db_port"]
db_engine = config["database"]["db_engine"]

# Создание строки подключения к базе данных
DATABASE_URL = f"{db_engine}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Базовая модель SQLAlchemy
Base = declarative_base()

# Модель таблицы с логами
class LogEntry(Base):
    __tablename__ = f"{TABLE_NAME}"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(2048))
    datetime = Column(DateTime)
    request = Column(String(2048))
    status = Column(Integer)
    size = Column(Integer)
    referrer = Column(Text)
    user_agent = Column(Text)

def create_db():
    """Создание таблицы через SQLAlchemy"""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    if not DISABLE_DB_CREATION:
        create_db()