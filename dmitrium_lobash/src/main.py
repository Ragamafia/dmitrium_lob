import time
import asyncio

from parser import MainParser
from utils import save_dict_to_json


parser = MainParser()


if __name__ == '__main__':
    start_time = time.time()

    asyncio.run(parser.run())

    end_time = time.time()
    print(f'Times: {end_time - start_time} seconds')
