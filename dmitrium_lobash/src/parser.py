import asyncio
from typing import List

import ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

from aiohttp import ClientSession, ClientTimeout
from aiohttp_proxy import ProxyType, ProxyConnector
from bs4 import BeautifulSoup

from config import cfg


TIMEOUT = ClientTimeout(total=cfg.proxy_check_timeout)


class MainParser:

    def __init__(self):
        self.data = {}

    async def run(self):
        proxy_type = ProxyType.HTTP if cfg.scheme == "http" else ProxyType.HTTPS
        kwargs = {
            "timeout": TIMEOUT,
            "connector": ProxyConnector(
                proxy_type=proxy_type,
                username=cfg.login,
                password=cfg.password,
                host=cfg.host,
                port=cfg.port,
                ssl_context=ssl_context
            )
        }

        async with ClientSession(**kwargs) as self.session:
            await self.get_pages()


    async def get_pages(self):
        home_page = await self.get_page(cfg.HOME_URL)
        home = await self.get_home_page(home_page)

        tasks_brand = [self.get_all_brand_links(brand) for brand in home]
        brands = await asyncio.gather(*tasks_brand)

        tasks_model = [self.get_models(model) for model in brands]
        models = await  asyncio.gather(*tasks_model)

        task_gens = [await self.get_gen(m) for m in models]
        gens = await asyncio.gather(*task_gens)

        task_glass = [await self.get_glass(g) for g in gens]
        glasses = await asyncio.gather(*task_glass)

        task_info = [await self.get_info(size) for size in glasses]
        info = await asyncio.gather(*task_info)

        print(self.data)

    async def get_page(self, url):
        async with self.session.get(url, headers=cfg.headers) as response:

            if response.status != 200:
                print(f"Website is DOWN! Status code {response.status}")
                exit()

            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            return soup

    async def get_home_page(self, page):
        container = page.find("div", class_="marks")
        data = container.find_all('a', href=True)
        return data

    async def get_all_brand_links(self, brand_link):
        link = brand_link['href'].split('/', 2)
        url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/' + link[2]
        return url

    async def get_models(self, brand):
        models_list = []
        models = await self.get_page(brand)
        container = models.find("div", class_="marks")
        data = container.find_all('a', href=True)
        for i in data:
            link = i['href'].split('/', 3)
            car = link[3].split('/')
            if car[0] not in self.data:
                self.data[car[0]] = {}
                self.data[car[0]][car[1]] = {}
            url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/steklo/' + link[3]
            models_list.append(url)
        return models_list

    async def get_gen(self, model):
        result = []
        for i in model:
            gens = await self.get_page(i)
            container = gens.find("section", class_="gen-list")
            data = container.find_all('a', href= True)
            for i in data:
                link = i['href'].split('/', 3)
                url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/glass-types/' + link[3]
                result.append(url)
        print(result)
        return result

    async def get_glass(self, gen):
        print('get_glass')
        result = []
        for i in gen:
            glasses = await self.get_page(i)
            container = glasses.find("section", class_="glass-type")
            glass = container.find('a')
            link = glass['href'].split('/', 3)
            url = cfg.HOME_URL.rstrip('/') + '/' + cfg.CITY + '/steklo/' + link[3]
            result.append(url)
        print(result)
        return result


    async def get_info(self, glasses):
        for i in glasses:
            glass = await self.get_page(i)

            for brand in self.data.values():
                for model in brand.values():
                    gen = glass.find("strong")
                    if 'не найден' in gen.text:
                        model[gen.text] = "Товар не найден"
                    else:
                        sizes = []
                        info_glass = glass.find_all("div", class_="dropdown-block")
                        for i in info_glass:
                            res = i.text.strip().split()
                            for size in res:
                                if size.isdigit():
                                    sizes.append(size)
                                model[gen.text] = str(sizes[:2])

