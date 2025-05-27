from pydantic import BaseModel
from fake_useragent import UserAgent


class Config(BaseModel):
    HOME_URL: str = "https://autosteklo.ru/"
    CITY: str = "moscow"

    headers: dict = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
    }


cfg = Config()
