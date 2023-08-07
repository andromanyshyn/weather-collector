import time

import psycopg2
import requests
from bs4 import BeautifulSoup

from config.config import DB_NAME, DB_HOST, DB_PASSWORD, DB_USER, API_KEY
from database.weather_database import truncate_table
from collector.cities import cities


class CityWeather():
    def __init__(self, list_cities):
        self.list_cities = list_cities
        self.api_key = API_KEY

    def get_city_names(self):
        cities_eng = []
        for city in self.list_cities:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'
            response = requests.get(url=url)
            data = response.json()
            key = 'name'
            if key in data:
                cities_eng.append(data['name'])
        return cities_eng

    def get_city_temperatures(self):
        list_temperature = []
        for city in cities():
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url=url)
            data = response.json()
            if 'main' in data and 'temp' in data['main']:
                list_temperature.append(f"{round(data['main']['temp'])}")
        return list_temperature


eng_cities = CityWeather(cities())
print(eng_cities.get_city_names())
print(eng_cities.get_city_temperatures())

# def get_weather_city():
#     list_cities = []
#     list_temperature = []
#
#     for city in cities():
#         url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
#         response = requests.get(url=url)
#         res = response.json()
#         key = 'name'
#
#         if key in res:
#             list_cities.append(res['name'])
#             list_temperature.append(f"{round(res['main']['temp'])}")
#     print(list_cities)
#
#
# get_weather_city()
#
# try:
#     connection = psycopg2.connect(
#         host=DB_HOST,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         database=DB_NAME
#     )
#     connection.autocommit = True
#     cursor = connection.cursor()
#
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS weather_info
#         (
#             weather_id SERIAL PRIMARY KEY,
#             city VARCHAR(40) NOT NULL,
#             celsius FLOAT NOT NULL
#         );
#         """
#     )
#     print('Data load started')
#
#         for celcius, city in enumerate(list_cities):
#             cursor.execute(
#                 f"""
#                 INSERT INTO weather_info(city, celsius)
#                 VALUES
#                 ('{city}', {list_temperature[celcius]});
#                  """
#             )
#         print('[INFO] Data loaded successful')
#         # print(f'[DATA FETCH] {cursor.fetchall()}')
#
#     except Exception as ex:
#         print(f'[ERROR] PostgreSQL got into troubles {ex}')
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#
#
# def main():
#     while True:
#         get_weather_city()
#         time.sleep(60)
#         truncate_table()
#
#
# if __name__ == '__main__':
#     main()
