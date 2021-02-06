#!/usr/bin/env python3
import cmd
import sys
import os
import re
from traceback import format_exc
from getopt import getopt, GetoptError
from domain.web_driver.SimpleDriver import SimpleDriver
from domain.content_filter.Youtube2020Filter import Youtube2020Filter
from domain.content_converter.YTVideoConverter import YTVideoConverter
from domain.Video import Video, vid_from_dict
from domain.Subscription import Subscription,load_new_videos, load_all_videos, subscription_from_dict
from log.file_logger import log
from domain.DateMatchesDict import date_matches_dict, py_tube_date_matches
from data.repository.SubscriptionRepository import fetch_all_subscriptions, insert_subscription, fetch_all_subs_w_last_id, delete_sub
from data.repository.VideoRepository import  fetch_new_videos, delete_new_video, fetch_all_videos, fetch_all_videos_of_subscription, delete_video_cascade
from multiprocessing import Pool
import os
from time import perf_counter
import json

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

def show_list(content_list):    
    [print("{0:<5}{1}".format(str(i) + ".", content)) for i, content in enumerate(content_list)]

def insert_subscription_from_url(url:str):
    if "youtube" in url:
        driver = SimpleDriver()
        content_filter = Youtube2020Filter()
        content_converter = YTVideoConverter()
        url_name:str
        if "/c/" in url:
            url_name = url[len("https://www.youtube.com/c/"):-len("/videos")]
            sub:Subscription = Subscription(url_name, "https://www.youtube.com/c/{0}/videos", "CHANNEL")
        elif "/user/" in url:
            url_name = url[len("https://www.youtube.com/user/"):-len("/videos")]
            sub:Subscription = Subscription(url_name, "https://www.youtube.com/user/{0}/videos", "USER")
        sub.set_filter(content_filter)
        sub.set_driver(driver)
        sub.set_converter(content_converter)
        insert_subscription(sub)
        load_all_videos(sub)

def save_videos_to_selection_list(vids:[Video]):
    vid_array:dict = [vid.to_dict() for vid in vids]
    save_selection_list({"type":"video", "content":vid_array})

def save_sub_to_selection_list(subs:[Subscription]):
    sub_array:dict = [sub.to_dict() for sub in subs]
    save_selection_list({"type":"subscription", "content":sub_array})

def save_selection_list(selection_list:dict):
    abs_path = os.getcwd() + "/data/selection_list.json"
    selection_list_file = open(abs_path, 'w')
    selection_list_file.write(json.dumps(selection_list))
    selection_list_file.close()

def read_selection_list_file():
    abs_path = os.getcwd() + "/data/selection_list.json"
    selection_list_file = open(abs_path, 'r')
    result = json.loads(selection_list_file.read())
    selection_list_file.close()
    return result

def read_selection_list():
    selection_list:dict = read_selection_list_file()
    if selection_list["type"] == "video":
        return [vid_from_dict(selection) for selection in selection_list['content']]
    if selection_list["type"] == "subscription":
        return [subscription_from_dict(selection) for selection in selection_list['content']]

def remove_item_from_selection_list(index:int):
    selection_list = read_selection_list_file()
    del selection_list["content"][index]
    save_selection_list(selection_list)

def get_selection_list_type() -> str:
    selection_list:dict = read_selection_list_file()
    return selection_list["type"]

def main(argv):

    try:
        opts, args = getopt(argv,"d:a:ns:ou", 
                [
                    "delete",
                    "new",
                    "select=",
                    "old=",
                    "add-subs=",
                    "subs",
                ])
    except GetoptError:
        print(format_exc())
        return 0

    for opt, arg in opts:
        if opt in ("-n","--new"):
            get_new_videos()
            vids:[Video] = fetch_new_videos()
            save_videos_to_selection_list(vids)
            show_list(vids)
        elif opt in ("-o", "--old"):
            amount:int = 25
            if len(argv) > 1:
                amount = int(argv[1])
            vids:[Video] = fetch_all_videos(None, amount)
            save_videos_to_selection_list(vids)
            show_list(vids)
        elif opt in ("-s", "--select"):
            index:int
            index = int(arg)
            result = read_selection_list()
            if (index < 0 or index >= len(result)):
                return 0
            if get_selection_list_type() == "video":
                os.system(
                        "open /Applications/Google\ Chrome.app https://www.youtube.com/watch?v=" + result[index].id 
                        )
                '''
                This removes the selected item from the locally saves selection list
                I still wonder whether it wouldn't be better to allow the user to reselect the previously selected video.
                Perhaps I should make a seperate command for that.
                '''
                remove_item_from_selection_list(index)
                delete_new_video(None, result[index].id)
            elif get_selection_list_type() == "subscription":
                vids:[Video] = fetch_all_videos_of_subscription(None, result[index].url_name)
                save_videos_to_selection_list(vids)                
                show_list(vids)
        elif opt in ("-d", "--delete="):
            index:int
            index = int(arg)
            result = read_selection_list()
            if get_selection_list_type() == "video":
                print("check")
                delete_video_cascade(result[index].id)
            elif get_selection_list_type() == "subscription":
                delete_sub(None, result[index].name)            
            remove_item_from_selection_list(index)
        elif opt in ("-a", "--add-subs="):
            insert_subscription_from_url(argv[1])
        elif opt in ("-u", "--subs="):
            subs:[Subscription] = fetch_all_subscriptions()
            save_sub_to_selection_list(subs)
            show_list(subs)

if __name__ == '__main__':
    main(sys.argv[1:])
