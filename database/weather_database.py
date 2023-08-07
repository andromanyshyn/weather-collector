import psycopg2
from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


def truncate_table():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(
            """TRUNCATE TABLE weather_info RESTART IDENTITY"""
        )
        print('[INFO] Truncated successful')
    except Exception as ex:
        print(f'[ERROR] PostgreSQL gone wrong {ex}')
    finally:
        if connection:
            cursor.close()
            connection.close()

