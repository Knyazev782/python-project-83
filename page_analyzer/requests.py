from .db import DatabaseConnection
import datetime
import psycopg2


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