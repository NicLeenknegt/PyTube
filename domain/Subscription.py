import abc
from domain.web_driver.IWebDriver import IWebDriver
from domain.content_filter.IContentFilter import IContentFilter
from domain.content_converter.IContentConverter import IContentConverter
from data.repository.VideoRepository import insert_video, fetch_new_video_max_date, insert_video_and_new_video
from datetime import datetime, timedelta

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

def load_all_videos(self:Subscription):
    html:str = self.web_driver.get_html(
            self.url_format.format(self.url_name)
            )
    json:str = self.content_filter.get_content( html, self.last_video_id)
    if json is not None:
        converted_vids:[Video] = self.content_converter.convert(json, self.url_name)
        for vid in converted_vids:
            insert_video(vid)        

def load_new_videos(self:Subscription):
    html:str = self.web_driver.get_html(
            self.url_format.format(self.url_name)
            )
    json:str = self.content_filter.get_content( html, self.last_video_id)
    if json is not None:
        new_video_max_date:datetime = fetch_new_video_max_date()
        new_video_max_date = new_video_max_date - timedelta(days=1)
        converted_vids:[Video] = self.content_converter.convert(json, self.url_name)
        # [::-1] reverses the list, so the new videos will be inserted in the end
        for vid in converted_vids[::-1]:
            # to prevent new subs from overloading the new tab
            # Only videos newer than the highest date can be inserted
            if new_video_max_date < vid.upload_date:            
                insert_video_and_new_video(vid)        

def subscription_from_dict(json:dict):
    return Subscription(
            json['url_name'],                
            json['url_format'],
            json['url_type'],
            json['last_video_id']
            )
