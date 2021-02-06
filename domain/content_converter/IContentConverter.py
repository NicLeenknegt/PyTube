import abc

class IContentConverter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def convert(self, json, name:str):
        raise NotImplementedError
