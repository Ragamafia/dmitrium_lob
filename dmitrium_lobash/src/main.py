import time
import asyncio

from parser import MainParser
from utils import save_dict_to_json
from config import cfg

parser = MainParser()

async def main():
    home_page = await parser.get_page(cfg.HOME_URL)
    all_brands = await parser.get_all_brand_links(home_page)
    models = await parser.get_models(all_brands)
    gens = await parser.get_gen(models)
    glasses = await parser.get_glass(gens)
    data = await parser.get_info(glasses)

    for i in data:
        print(i)

    save_dict_to_json(data)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())

    end_time = time.time()
    print(f'Times: {end_time - start_time} seconds')
