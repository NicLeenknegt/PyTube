import abc

class IContentFilter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_content(self, html:str, last_local_id:str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_item(self, source:str) -> str:
        raise NotImplementedError
