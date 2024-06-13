import re
from dateutil.parser import parse

def parse_apache_log(log_line):
    """
    Args:
        log_line (str): Строка лога

    Returns:
        dict: Словарь с данными из лога
    """

    pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
    match = re.match(pattern, log_line)
    if match:
        ip, date_time_str, request, status, size, referrer, user_agent = match.groups()
        date_time_str = date_time_str.replace(':', ' ', 1)
        date_time = parse(date_time_str, dayfirst=True)
        return {
            "ip": ip,
            "datetime": date_time,
            "request": request,
            "status": status,
            "size": size,
            "referrer": referrer,
            "user_agent": user_agent
        }
    else:
        return None