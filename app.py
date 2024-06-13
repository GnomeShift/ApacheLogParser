from dateutil.parser import parse
import subprocess
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from db import get_db
from create_db import LogEntry
import logging
from parsing import parse_apache_log
from sqlalchemy import func
from werkzeug.serving import WSGIRequestHandler

from config import DEBUG, API_PREFIX, LOGGING_LEVEL, ACCESS_LOG_FILE, DISABLE_DB_CREATION

app = Flask(__name__)
CORS(app)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

class UTF8RequestHandler(WSGIRequestHandler):
    def send_header(self, keyword, value):
        super().send_header(keyword, 'utf-8')

# Настройка лога приложения
logging.basicConfig(
    level=LOGGING_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="logs.log"
)

# Автосоздание базы данных
if not DISABLE_DB_CREATION:
    subprocess.call(["python", "create_db.py"])

# API
@app.route('/')
def index():
    data = {'message': 'API started successfully'}
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route(f'{API_PREFIX}/logs', methods=['GET'])
def get_logs():
    """Показ логов"""
    logging.info('Показ логов')
    db = get_db()
    logs = db.query(LogEntry).all()
    log_dicts = [log.__dict__ for log in logs]
    for log_dict in log_dicts:
        log_dict.pop('_sa_instance_state', None)
    response = jsonify(log_dicts)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 201

@app.route(f'{API_PREFIX}/logs/by_ip', methods=['GET'])
def get_logs_by_ip():
    """Фильтрация логов по IP."""
    logging.info('Фильтрация логов по IP')
    db = get_db()
    ip = request.args.get('ip')
    logs = db.query(LogEntry).filter(LogEntry.ip == ip).all()
    log_dicts = [log.__dict__ for log in logs]
    for log_dict in log_dicts:
        log_dict.pop('_sa_instance_state', None)
    response = jsonify(log_dicts)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 201

@app.route(f'{API_PREFIX}/logs/by_date', methods=['GET'])
def get_logs_by_date():
    """Фильтрация логов по дате"""
    logging.info('Фильтрация логов по дате')
    db = get_db()
    date_str = request.args.get('date')
    date = parse(date_str)
    logs = db.query(LogEntry).filter(func.date(LogEntry.datetime) == date.date()).all()
    log_dicts = [log.__dict__ for log in logs]
    for log_dict in log_dicts:
        log_dict.pop('_sa_instance_state', None)
    response = jsonify(log_dicts)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 201

@app.route(f'{API_PREFIX}/logs/by_range', methods=['GET'])
def get_logs_by_range():
    """Фильтрация логов по диапазону дат"""
    logging.info('Фильтрация логов по диапазону дат')
    db = get_db()
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    start_date = parse(start_date_str)
    end_date = parse(end_date_str)
    logs = db.query(LogEntry).filter(LogEntry.datetime >= start_date, LogEntry.datetime <= end_date).all()
    log_dicts = [log.__dict__ for log in logs]
    for log_dict in log_dicts:
        log_dict.pop('_sa_instance_state', None)
    response = jsonify(log_dicts)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 201

def read_access_log(filename):
    """Читает access.log и возвращает строки"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            logs = f.readlines()
        return logs
    except FileNotFoundError:
        logging.error(f"Файл access.log не найден: {filename}")
        return []

def save_logs_to_db(filename):
    """Сохранение логов в базу данных"""
    logs = read_access_log(filename)
    db = get_db()
    for log in logs:
        parsed_log = parse_apache_log(log)
        if parsed_log:
            log_entry = LogEntry(**parsed_log)
            db.add(log_entry)
    db.commit()
    db.close()

if __name__ == "__main__":
    app.run(debug=DEBUG)

    save_logs_to_db(ACCESS_LOG_FILE)