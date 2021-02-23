from domain.Subscription import Subscription
from domain.web_driver.SimpleDriver import SimpleDriver
from domain.content_filter.Youtube2020Filter import Youtube2020Filter
from domain.content_converter.YTVideoConverter import YTVideoConverter
from data.repository.VideoRepository import insert_video, fetch_new_video_max_date, insert_video_and_new_video
from datetime import datetime, timedelta
from multiprocessing import Pool
from data.repository.SubscriptionRepository import fetch_all_subs_w_last_id
from sqlite3 import OperationalError, IntegrityError
from threading import Thread

def load_all_videos_test(sub:Subscription):
    html:str = SimpleDriver().get_html(sub.url_format.format(sub.url_name))
    json:str = Youtube2020Filter().get_content(html, None)
    if json is not None:
        converted_vids:[Video] = YTVideoConverter().convert(json, sub.url_name)
        for vid in converted_vids:
            try:
                print(vid)
                #insert_video(vid)
            except OperationalError:
                raise ValueError("database failure: an error occured while saving videos of \"{}\"".format(sub.url_name))
            except IntegrityError as err:
                raise ValueError("database failure: an error ocurred while inserting the video \"{}\"".format(vid.title))

def load_new_videos_test(sub:Subscription):
    html:str = SimpleDriver().get_html(sub.url_format.format(sub.url_name))
    json:str = Youtube2020Filter().get_content(html, sub.last_video_id)
    if json is not None:
        converted_vids:[Video] = YTVideoConverter().convert(json, sub.url_name)
        # [::-1] reverses the list, so the new videos will be inserted in the end
        for vid in converted_vids[::-1]:
            try:
                insert_video_and_new_video(vid)
            except OperationalError:
                raise ValueError("database failure: an error occured while saving videos of \"{}\"".format(sub.url_name))
            except IntegrityError as err:
                raise ValueError("database failure: an error ocurred while inserting the video \"{}\"".format(vid.title))

def load_all_videos(sub:Subscription):
    html:str = sub.web_driver.get_html(sub.url_format.format(sub.url_name))
    json:str = sub.content_filter.get_content(html, None)
    if json is not None:
        converted_vids:[Video] = sub.content_converter.convert(json, sub.url_name)
        for vid in converted_vids:
            try:
                insert_video(vid)
            except OperationalError:
                raise ValueError("database failure: an error occured while saving videos of \"{}\"".format(sub.url_name))
            except IntegrityError as err:
                raise ValueError("database failure: an error ocurred while inserting the video \"{}\"".format(vid.title))

def load_new_videos(sub:Subscription):
    html:str = sub.web_driver.get_html(
            sub.url_format.format(sub.url_name)
            )
    json:str = sub.content_filter.get_content( html, sub.last_video_id)
    if json is not None:
        new_video_max_date:datetime = fetch_new_video_max_date()
        new_video_max_date = new_video_max_date - timedelta(days=1)
        converted_vids:[Video] = sub.content_converter.convert(json, sub.url_name)
        # [::-1] reverses the list, so the new videos will be inserted in the end
        for vid in converted_vids[::-1]:
            # to prevent new subs from overloading the new tab
            # Only videos newer than the highest date can be inserted
            if new_video_max_date < vid.upload_date:
                try:
                    insert_video_and_new_video(vid)
                except OperationalError:
                    raise ValueError("database failure: an error occured while saving videos of \"{}\"".format(sub.url_name))
                except IntegrityError as err:
                    raise ValueError("database failure: an error ocurred while inserting the video \"{}\"".format(vid.title))

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
    threads = []

    for index, sub in enumerate(subs):
        sub.set_filter(content_filter)
        sub.set_driver(driver)
        sub.set_converter(content_converter)
        sub_thread = Thread(target=load_new_videos_test, args=(sub, ))
        threads.append(sub_thread)
        sub_thread.start()

    for thread in threads:
        thread.join()
#
#    with Pool(len(subs)) as p:
#        p.map(load_new_videos, subs)
#
