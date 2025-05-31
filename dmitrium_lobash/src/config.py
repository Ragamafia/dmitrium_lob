from pydantic import BaseModel
from fake_useragent import UserAgent


class Config(BaseModel):
    HOME_URL: str = "https://autosteklo.ru/"
    CITY: str = "moscow"

    headers: dict = {
        "User-Agent": UserAgent().random
    }


cfg = Config()
