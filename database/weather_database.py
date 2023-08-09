import psycopg2

from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


def database_connect():
    with psycopg2.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    ) as connection:
        connection.autocommit = True
        return connection


def truncate_table():
    connection = database_connect()
    try:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("""TRUNCATE TABLE weather_info RESTART IDENTITY""")
            print("[INFO] Truncated successful")
    except Exception as ex:
        print(f"[ERROR] PostgreSQL gone wrong {ex}")
