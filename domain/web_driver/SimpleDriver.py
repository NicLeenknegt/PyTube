from requests import Response, get, ConnectionError, Timeout, HTTPError, RequestException

from domain.web_driver.IWebDriver import IWebDriver
from time import perf_counter

class SimpleDriver(IWebDriver):

    def get_html(self, url:str) -> str:
        try:
            r:Response = get(url)
            r.raise_for_status()
        except ConnectionError as err:
            raise ValueError("connection error: a network problem has occurred, possibly a DNS failure or refused connection")
        except HTTPError as err:
            raise ValueError("htttp error: something went wrong while trying to fetch {}".format(url))
        except Timeout as err:
            raise ValueError("connection error: connection timeout")
        except RequestException as err:
            raise ValueError("connection error: something went wrong while trying to fetch {}".format(url))
            
        return r.text
