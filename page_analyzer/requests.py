from .db import DatabaseConnection
import datetime
import psycopg2


def check_url_unique(url):
    with DatabaseConnection() as db:
        try:
            db.execute("SELECT 1 FROM urls WHERE name = %s;", (url,))
            result = db.fetchone()
            if result is not None:
                return True
            else:
                return False
        except psycopg2.IntegrityError:
            return



def add_url(url):
    with DatabaseConnection() as db:
        try:
            db.execute("""
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id;
            """, (url, datetime.datetime.now()))
            result = db.fetchone()
            url_id = result[0]
            return url_id
        except psycopg2.IntegrityError:
            print(f"URL {url} уже существует в нашей базе")
            return