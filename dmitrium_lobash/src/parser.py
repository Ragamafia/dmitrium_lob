import requests
from bs4 import BeautifulSoup

from config import cfg


class MainParser:

    def __init__(self):
        # home_page = self.get_page(cfg.HOME_URL)
        # brands = self.get_brand_links(home_page)
        # models = self.get_models(brands)
        cars = self.get_car_gen()
        glasses = self.get_glass_type(cars)
        self.get_glass(glasses)

    def get_page(self, url):
        response = requests.get(url, headers=cfg.headers)

        if response.status_code != 200:
            print(f"Website is DOWN! Status code {response.status_code}")
            exit()

        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find("div", class_="marks")
        data = container.find_all('a', href=True)
        return data

    def get_brand_links(self, page) -> list:
        links = []

        for brand_link in page:
            link = brand_link['href'].split('/', 2)
            url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/' + link[2]
            links.append(url)
        return links

    def get_models(self, brands: list) -> dict:
        auto = {}

        for i in brands:
            models = self.get_page(i)
            for model in models:
                link = model['href'].split('/', 3)
                url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/steklo/' + link[3]
                print(url)
                auto[link[3]] = url

        return auto

    def get_car_gen(self):
        result = []

        #for i in models.values():
        i = "https://autosteklo.ru/moscow/steklo/toyota/corona"
        car = requests.get(i, headers=cfg.headers)
        soup = BeautifulSoup(car.text, "html.parser")
        container = soup.find("section", class_="gen-list")
        data = container.find_all('a', href=True)
        for i in data:
            link = i['href'].split('/', 3)
            url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/glass-types/' + link[3]
            result.append(url)

        return result

    def get_glass_type(self, cars):
        result = {}

        for i in cars:
            response = requests.get(i, headers=cfg.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            info_glass = soup.find("section", class_="glass-type")
            info_car = soup.find("div", class_="car-info")
            res = info_glass.find('a')
            link = res['href'].split('/', 3)
            url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/glass-types/' + link[3]
            result[info_car.text] = url
        return result

    def get_glass(self, glasses: dict):
        for i in glasses.values():
            response = requests.get(i, cfg.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            print(soup.text)
            info_glass = soup.find("section", class_="glass-type")
            print(info_glass)
            res = info_glass.find('a')
            link = res['href'].split('/', 3)
            print(link)
            url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/glass-types/' + link[3]
            print(url)
