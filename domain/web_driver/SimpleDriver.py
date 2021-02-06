import requests

from domain.web_driver.IWebDriver import IWebDriver
from time import perf_counter

class SimpleDriver(IWebDriver):

    def get_html(self, url:str) -> str:
        r:requests.Response = requests.get(url)
        return r.text
