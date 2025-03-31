import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print("Версия PostgreSQL:", cur.fetchone())
    cur.close()
    conn.close()
except psycopg2.Error as e:
    print(f"Ошибка подключения: {e}")
