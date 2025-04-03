from .db import DatabaseConnection
import datetime
import psycopg2
import requests


def check_url_exists(url):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT 1 FROM urls WHERE name = %s;", (url,))
            result = db.fetchone()
            return result is not None
        except psycopg2.Error:
            return False


def get_url_id(url):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT id FROM urls WHERE name = %s;", (url,))
            result = db.fetchone()
            if result is not None:
                return result[0]
            else:
                return None
        except psycopg2.Error:
            return None


def add_url(url):
    with DatabaseConnection() as db:
        try:
            db.execute("""
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s);
            """, (url, datetime.datetime.now()))
            return True
        except psycopg2.IntegrityError:
            print(f"URL {url} уже существует в нашей базе")
            return False


def get_url_by_id(url_id):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT * FROM urls WHERE id = %s;", (url_id,))
            result = db.fetchone()
            if result is not None:
                return result
            else:
                return None
        except psycopg2.Error:
            return None


def get_urls():
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT * FROM urls ORDER BY created_at DESC;")
            result = db.fetchall()
            return result
        except psycopg2.Error:
            return None


def create_check(url_id, status_code):
    with DatabaseConnection() as db:
        try:
            db.execute("INSERT INTO url_checks"
                       "(url_id, created_at, status_code) VALUES (%s, %s, %s);",
                       (url_id, datetime.datetime.now(), status_code))
            return True
        except psycopg2.Error:
            print('Ошибка при создании проверки')
            return False


def get_checks_by_url_id(url_id):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT id, created_at, status_code FROM url_checks "
                       "WHERE url_id = %s ORDER BY created_at DESC", (url_id,))
            result = db.fetchall()
            return [(check[0], check[1].strftime('%Y-%m-%d %H:%M:%S')
            if check[1] else None, check[2]) for check in result]
        except psycopg2.Error:
            print('Ошибка при получении списка проверок')
            return []


def get_last_check_date(url_id):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT created_at, status_code FROM url_checks "
                       "WHERE url_id = %s ORDER BY "
                       "created_at DESC LIMIT 1", (url_id,))
            result = db.fetchone()
            return result[0].strftime('%Y-%m-%d %H:%M:%S'), result[1] \
                if result and result[0] else (None, None)
        except psycopg2.Error:
            print('Ошибка при выборе даты последней проверки')
            return None, None


def check_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException:
        print('Произошла ошибка получения ответа')
        return None

