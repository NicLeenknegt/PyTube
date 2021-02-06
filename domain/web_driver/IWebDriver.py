import abc

class IWebDriver(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_html(self, url:str) -> str:
        raise NotImplementedError
