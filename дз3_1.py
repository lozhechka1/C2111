import sqlite3
import http.client
import ssl
from html.parser import HTMLParser
from datetime import datetime

# ===== 1. Парсер HTML =====
class TemperatureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.record = False
        self.temperature = None

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            for attr in attrs:
                if attr == ('class', 'today-temp'):
                    self.record = True

    def handle_data(self, data):
        if self.record and not self.temperature:
            self.temperature = data.strip()
            self.record = False

# ===== 2. Отримання HTML =====
def get_weather_html():
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection("sinoptik.ua", context=context)
    conn.request("GET", "/погода-київ")
    res = conn.getresponse()
    return res.read().decode('utf-8')

# ===== 3. Отримання температури =====
html = get_weather_html()
parser = TemperatureParser()
parser.feed(html)
temperature = parser.temperature or "N/A"

# ===== 4. Створення БД та запис =====
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        datetime TEXT,
        temperature TEXT
    )
''')

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute("INSERT INTO weather (datetime, temperature) VALUES (?, ?)", (now, temperature))
conn.commit()
conn.close()

print(f"Температура збережена: {now}, температура: {temperature}")