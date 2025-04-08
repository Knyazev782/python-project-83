import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')


class DatabaseConnection:
    def __init__(self):
        self.database_url = DATABASE_URL
        try:
            self.conn = psycopg2.connect(self.database_url)
        except psycopg2.Error:
            raise Exception('Ошибка подключения к базе данных!')

    def __enter__(self):
        try:
            self.cursor = self.conn.cursor()
            return self.cursor
        except psycopg2.Error:
            raise Exception('Не удалось создать курсор!')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()
