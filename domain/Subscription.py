import abc
from domain.web_driver.IWebDriver import IWebDriver
from domain.content_filter.IContentFilter import IContentFilter
from domain.content_converter.IContentConverter import IContentConverter

class Subscription:

    def __init__(self,
            url_name:str,
            url_format:str,
            url_type:str,
            last_video_id:str = None
            ):
        self.url_name = url_name
        self.url_format = url_format
        self.videos = []
        self.web_driver = None
        self.content_filter = None
        self.content_converter = None
        self.type:str = url_type    
        self.last_video_id = last_video_id

    def set_driver(self,driver:IWebDriver):
        self.web_driver = driver

    def set_converter(self, converter:IContentConverter):
        self.content_converter = converter

    def set_filter(self, content_filter:IContentFilter):
        self.content_filter = content_filter

    def __str__(self):
        return "{0:<40}{1:60}{2:10}".format(self.url_name, self.url_format, self.type)

    def to_dict(self) -> dict:
        return {
                "url_name":self.url_name,
                "url_format":self.url_format,
                "url_type":self.type,
                "last_video_id":self.last_video_id
                }
