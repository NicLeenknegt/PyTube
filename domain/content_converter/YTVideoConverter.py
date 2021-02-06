import json
import re
from domain.Video import Video
from domain.content_converter.IContentConverter import IContentConverter
from domain.content_converter.DateConverter import DateConverter
from log.file_logger import log
from datetime import datetime
from domain.DateMatchesDict import py_tube_date_matches, date_matches_dict

class YTVideoConverter(IContentConverter):

    def __init__(self):
        self.date_converter:IContentConverter = DateConverter()

    def convert(self, json_str:str,name:str) -> [Video]:
        json_array = json.loads(json_str)
        vid_array:[Video] = []
        
        #Set locale for date conversion
        py_tube_date_matches = date_matches_dict[json_array[0]['locale']]

        #Cut away locale from json array
        json_array = json_array[1:]

        for json_item in json_array:
            vid_id:str = json_item['gridVideoRenderer']['videoId']

            vid_title:str = json_item['gridVideoRenderer']['title']['runs'][0]['text']
            vid_title_len:int = len(vid_title)
            
            date_str:str = json_item['gridVideoRenderer']['title']['accessibility']['accessibilityData']['label'][vid_title_len:]
                
            date:datetime = self.date_converter.convert(date_str, None)

            vid_array.append(Video(vid_id, vid_title,date,name))
            
        return vid_array 
