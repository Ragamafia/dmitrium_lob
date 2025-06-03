import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from fake_useragent import UserAgent


current_file = Path(__file__)
root = current_file.parent.parent
env_path = root / 'env' / '.env'

load_dotenv(dotenv_path=env_path)


class Config(BaseModel):
    HOME_URL: str = "https://autosteklo.ru/"
    CITY: str = "moscow"

    headers: dict = {
        "User-Agent": UserAgent().random
    }

    scheme: str = 'https'
    proxy_user: str = os.getenv('PROXY_USERNAME')
    proxy_pass: str = os.getenv('PROXY_PASSWORD')
    proxy_host: str = os.getenv('PROXY_HOST')
    proxy_port: int = os.getenv('PROXY_PORT')

    proxy_check_timeout: int = 60
    request_attempts: int = 5


cfg = Config()