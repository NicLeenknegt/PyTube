from domain.Subscription import Subscription
from domain.web_driver.SimpleDriver import SimpleDriver
from domain.content_filter.Youtube2020Filter import Youtube2020Filter
from domain.content_converter.YTVideoConverter import YTVideoConverter
from data.repository.VideoRepository import insert_video, fetch_new_video_max_date, insert_video_and_new_video
from datetime import datetime, timedelta
from multiprocessing import Pool
from data.repository.SubscriptionRepository import fetch_all_subs_w_last_id

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

def get_new_videos():
    driver = SimpleDriver()
    content_filter = Youtube2020Filter()
    content_converter = YTVideoConverter()

    subs = fetch_all_subs_w_last_id()
    for sub in subs:
        sub.set_filter(content_filter)
        sub.set_driver(driver)
        sub.set_converter(content_converter)

    with Pool(len(subs)) as p:
        p.map(load_new_videos, subs)

