import requests
from bs4 import BeautifulSoup

from config import cfg


class MainParser:

    def __init__(self):
        self.data = {}

    async def get_page(self, url):
        response = requests.get(url, headers=cfg.headers)

        if response.status_code != 200:
            print(f"Website is DOWN! Status code {response.status_code}")
            exit()

        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find("div", class_="marks")
        data = container.find_all('a', href=True)
        return data

    async def get_all_brand_links(self, brands) -> list:
        #   собирает список ссылок всех брендов с сайта
        links = []

        for brand_link in brands:
            link = brand_link['href'].split('/', 2)
            url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/' + link[2]
            links.append(url)

        return links

    async def get_models(self, brand_urls: list) -> list:
        #   собирает ссылки на все модели бренда, заполняет словарь брендами
        result = []

        for url in brand_urls:
            models = await self.get_page(url)
            for model in models:
                link = model['href'].split('/', 3)
                car = link[3].split('/')
                if car[0] not in self.data:
                    self.data[car[0]] = {}
                    self.data[car[0]][car[1]] = {}

                url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/steklo/' + link[3]
                result.append(url)

        return result

    async def get_gen(self, models: list) -> list:
        #   получает ссылки на все поколения модели
        result = []

        for url in models:
            response = requests.get(url, headers=cfg.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            container = soup.find("section", class_="gen-list")
            data = container.find_all('a', href= True)
            for i in data:
                link = i['href'].split('/', 3)
                url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/glass-types/' + link[3]
                result.append(url)

        return result

    async def get_glass(self, gen_list: list) -> list:
        #   получает ссылки на стёкла
        result = []

        for i in gen_list:
            response = requests.get(i, headers=cfg.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            info_glass = soup.find("section", class_="glass-type")
            glass = info_glass.find('a')
            link = glass['href'].split('/', 3)
            url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/steklo/' + link[3]
            result.append(url)

        return result


    async def get_info(self, glasses: list) -> dict:
        for i in glasses:
            response = requests.get(i, headers=cfg.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            for brand in self.data.values():
                for model in brand.values():
                    gen = soup.find("strong")
                    if 'не найден' in soup.text:
                        model[gen.text] = "Товар не найден"
                    else:
                        sizes = []
                        info_glass = soup.find_all("div", class_="dropdown-block")
                        for i in info_glass:
                            res = i.text.strip().split()
                            for size in res:
                                if size.isdigit():
                                    sizes.append(size)
                                model[gen.text] = str(sizes[:2])
        return self.data
