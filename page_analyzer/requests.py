from .db import DatabaseConnection
import datetime
import psycopg2
import requests
from bs4 import BeautifulSoup


def check_url_exists(url):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT 1 FROM urls WHERE name = %s;", (url,))
            result = db.fetchone()
            return result is not None
        except psycopg2.Error as e:
            print(f'Ошибка при проверке существования URL: {e}')
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
        except psycopg2.Error as e:
            print(f'Ошибка при получении ID URL: {e}')
            return None


def add_url(url):
    with DatabaseConnection() as db:
        try:

            now = datetime.datetime.now().replace(microsecond=0)
            db.execute("""
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s);
            """, (url, now))
            return True
        except psycopg2.IntegrityError:
            print(f"URL {url} уже существует в нашей базе")
            return False
        except psycopg2.Error as e:
            print(f'Ошибка при добавлении URL: {e}')
            return False


def get_url_by_id(url_id):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT * FROM urls WHERE id = %s;", (url_id,))
            result = db.fetchone()
            if result is not None:

                return result[0], result[1], result[2].strftime('%Y-%m-%d %H:%M:%S')
            else:
                return None
        except psycopg2.Error as e:
            print(f'Ошибка при получении URL по ID: {e}')
            return None


def get_urls():
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT * FROM urls ORDER BY created_at DESC;")
            result = db.fetchall()

            return [(row[0], row[1], row[2].strftime('%Y-%m-%d %H:%M:%S')) for row in result]
        except psycopg2.Error as e:
            print(f'Ошибка при получении списка URL: {e}')
            return None


def create_check(url_id, status_code, h1, title, description):
    with DatabaseConnection() as db:
        try:
            h1 = h1[:255] if h1 else None
            title = title[:255] if title else None
            description = description[:255] if description else None

            now = datetime.datetime.now().replace(microsecond=0)
            db.execute("INSERT INTO url_checks"
                       "(url_id, created_at, status_code, "
                       "h1, title, description) VALUES (%s, %s, %s, %s, %s, %s);",
                       (url_id, now, status_code, h1, title, description))
            return True
        except psycopg2.Error as e:
            print(f'Ошибка при создании проверки: {e}')
            return False


def get_checks_by_url_id(url_id):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT id, created_at, status_code, "
                       "h1, title, description FROM url_checks "
                       "WHERE url_id = %s ORDER BY created_at DESC", (url_id,))
            result = db.fetchall()
            return [(check[0], check[1].strftime('%Y-%m-%d %H:%M:%S')
            if check[1] else None, check[2], check[3],
                     check[4], check[5]) for check in result]
        except psycopg2.Error as e:
            print(f'Ошибка при получении списка проверок: {e}')
            return []


def get_last_check_date(url_id):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT created_at, status_code FROM url_checks "
                       "WHERE url_id = %s ORDER BY "
                       "created_at DESC LIMIT 1", (url_id,))
            result = db.fetchone()
            if result is None:
                return None, None
            else:
                return result[0].strftime('%Y-%m-%d %H:%M:%S'), result[1]
        except psycopg2.Error as e:
            print(f'Ошибка при выборе даты последней проверки: {e}')
            return None, None


def check_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        h1_tag = None
        title_tag = None
        meta_tag = None
        if soup.find('h1'):
            h1_tag = soup.find('h1').get_text(strip=True)
        if soup.find('title'):
            title_tag = soup.find('title').get_text(strip=True)
        if soup.find('meta', attrs={'name': 'description'}):
            meta_tag = soup.find('meta',
                                 attrs={'name': 'description'}).get('content')
        return response.status_code, h1_tag, title_tag, meta_tag
    except requests.exceptions.RequestException as e:
        print(f'Произошла ошибка получения ответа для {url}: {e}')
        return None, None, None, None
