import psycopg2
from config import db_name, host, password, user


def truncate_table():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
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

