import time

import psycopg2
import requests
from bs4 import BeautifulSoup

from config import db_name, host, password, user
from weather_database import truncate_table


def cities():
    list_cities = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    url = 'http://www.statdata.ru/largestcities_world'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    table = [data.text.split() for data in soup.find('div', class_='wprt-container').find('tbody').find_all('td')]
    for data in table[7::6]:
        list_cities.append(''.join(data))
    return list_cities


def get_info():
    list_cities = []
    list_temperature = []
    API = '3c0d32271c11926b66b464516d649976'

    for city in cities()[:53]:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric'
        response = requests.get(url=url)
        res = response.json()
        key = 'name'

        if key in res:
            list_cities.append(res['name'])
            list_temperature.append(f"{round(res['main']['temp'])}")
            print('loading data...')
    print(list_cities)
    for word in list_cities:
        if "'" in word:
            list_cities.remove(word)

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
            """
            CREATE TABLE IF NOT EXISTS weather_info
            (
                weather_id SERIAL PRIMARY KEY,
                city VARCHAR(40) NOT NULL,
                celsius FLOAT NOT NULL
            );
            """
        )
        print('Data load started')

        for celcius, city in enumerate(list_cities):
            cursor.execute(
                f"""
                INSERT INTO weather_info(city, celsius)
                VALUES
                ('{city}', {list_temperature[celcius]});
                 """
            )
        print('[INFO] Data loaded successful')
        # print(f'[DATA FETCH] {cursor.fetchall()}')

    except Exception as ex:
        print(f'[ERROR] PostgreSQL got into troubles {ex}')
    finally:
        if connection:
            cursor.close()
            connection.close()


def main():
    while True:
        get_info()
        time.sleep(60)
        truncate_table()


if __name__ == '__main__':
    main()
