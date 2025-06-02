from pydantic import BaseModel
from fake_useragent import UserAgent


class Config(BaseModel):
    HOME_URL: str = "https://autosteklo.ru/"
    CITY: str = "moscow"

    headers: dict = {
        "User-Agent": UserAgent().random
    }

    scheme: str = 'https'
    login: str = 'A6LC1A'
    password: str = 'ax2rMU'
    host: str = '194.226.60.201'
    port: int = 8000

    proxy_check_timeout: int = 60


cfg = Config()
