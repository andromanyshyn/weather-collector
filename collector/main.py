import asyncio

import aiohttp

from collector.cities import cities
from config.config import API_KEY
from database.weather_database import database_connect, truncate_table


class CityWeather:
    def __init__(self, list_cities):
        self.list_cities = list_cities
        self.api_key = API_KEY

    async def fetch_weather_data(self, session, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        async with session.get(url=url) as response:
            if response.status == 200:
                data = await response.json()
                return data

    async def get_city_names(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for city in self.list_cities:
                task = self.fetch_weather_data(session, city)
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            cities_eng = [data["name"] for data in results if data is not None]
            return cities_eng

    async def get_city_temperatures(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for city in self.list_cities:
                task = self.fetch_weather_data(session, city)
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            list_temperature = [
                data["main"]["temp"] for data in results if data is not None
            ]
            return list_temperature


async def insert_data(cities, temperatures):
    connection = database_connect()
    try:
        connection.autocommit = True
        with connection.cursor() as cursor:
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

            for indx, city in enumerate(cities):
                print("Data load started")
                cursor.execute(
                    """
                    INSERT INTO weather_info(city, celsius)
                    VALUES (%s, %s);
                    """,
                    (city, temperatures[indx]),
                )
            print("[INFO] Data loaded successful")
    except Exception as ex:
        print(f"[ERROR] PostgreSQL got into troubles {ex}")


async def main():
    weather = CityWeather(cities())
    get_cities = await weather.get_city_names()
    get_city_temperature = await weather.get_city_temperatures()
    while True:
        await insert_data(get_cities, get_city_temperature)
        await asyncio.sleep(10)
        truncate_table()
        await asyncio.sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
