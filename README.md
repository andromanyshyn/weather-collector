# Asynchronous City Weather Collector

This repository contains an asynchronous Python script that collects weather data for a list of cities from the OpenWeatherMap API. The collected data is then stored in a PostgreSQL database, and the script periodically updates the weather information. The project utilizes the `aiohttp` library for asynchronous HTTP requests and leverages `asyncio` for managing concurrent tasks.

## Prerequisites

- Python 3.7+
- PostgreSQL database with valid credentials
- OpenWeatherMap API key (Sign up at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up))

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/andromanyshyn/weather-collector.git
    cd weather-collector
    ```

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Your API Key**:

    - Rename `config/config.py.example` to `config/config.py`.
    - Replace `YOUR_API_KEY` with your actual OpenWeatherMap API key.

4. **Define Cities to Collect Data For**:

    - Edit `collector/cities.py` to specify the list of cities for weather data collection.

5. **Set Up Database Connection**:

    - Ensure you have a PostgreSQL database available.
    - Update the database connection details in `database/weather_database.py` if required.

6. **Run the Script**:

    ```bash
    python main.py
    ```

    The script will initiate the weather data collection for the specified cities, store it in the database, and regularly update the data.

## Customization

- You can adjust the **update frequency** by modifying the sleep intervals in the `main` coroutine within `main.py`.

- The script is currently designed to insert weather data into a table named `weather_info`. If needed, you can modify the **database schema and insertion logic** within the `insert_data` coroutine in `main.py`.
