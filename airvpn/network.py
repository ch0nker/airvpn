from requests import Session
from os import path
from enum import StrEnum

class Status(StrEnum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"

class AirSession(Session):
    BASE_URL = "https://airvpn.org/api/"

    def __init__(self, api_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers.setdefault("API-KEY", api_key)
    
    def get(self, endpoint: str, *args, **kwargs):
        return super().get(f"{AirSession.BASE_URL}{endpoint}/", *args, **kwargs)

    def post(self, endpoint: str, *args, **kwargs):
        return super().post(f"{AirSession.BASE_URL}{endpoint}/", *args, **kwargs)