from domain.ContentPlayer import ContentPlayer, content_player_from_dict
from domain.Video import Video, vid_from_dict
from domain.Subscription import Subscription,subscription_from_dict
import json
import os

def save_content_player_to_selection_list(content_players:[ContentPlayer]):
    content_player_array:dict = [content_player.to_dict() for content_player in content_players]
    save_selection_list({"type":"content_player", "content":content_player_array})

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
    elif selection_list["type"] == "subscription":
        return [subscription_from_dict(selection) for selection in selection_list['content']]
    elif selection_list["type"] == "content_player":
        return [content_player_from_dict(selection) for selection in selection_list['content']]

def remove_item_from_selection_list(index:int):
    selection_list = read_selection_list_file()
    del selection_list["content"][index]
    save_selection_list(selection_list)

def get_selection_list_type() -> str:
    selection_list:dict = read_selection_list_file()
    return selection_list["type"]

