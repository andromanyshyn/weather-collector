import requests
from bs4 import BeautifulSoup


def cities():
    list_cities = []
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    url = "http://www.statdata.ru/largestcities_world"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    columns = soup.find("table").find_all("tr")[2:]

    for idx, row in enumerate(columns):
        if idx >= 50:
            break
        data = row.find_all("td")
        city_name = data[1].text
        list_cities.append(city_name)
    return list_cities
