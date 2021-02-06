import re
from domain.content_filter.IContentFilter import IContentFilter
from log.file_logger import log

class Youtube2020Filter(IContentFilter):
    
    def __init__(self):
        self.html_re = re.compile(r"\"items\":\[\{\"gridVideoRenderer\".*?\"}]}}}]}}]")
        self.locale_re = re.compile(r"locale=.*?_")
        self.video_id_re = re.compile(r"videoId\":\".*?\"")
        self.html_iterator = re.compile(r"{\"gridVideoRenderer\".*?thumbnailOverlayNowPlayingRenderer.*?}}}]}}(,|])")

    def get_content(self, html:str, last_local_id:str) -> str:
            
        #HTML ITERATOR
        last_video_id = self.get_first_item(html)
        if last_video_id == last_local_id:
            return None
        
        result:str = ""
        html_copy = html

        itererator_reg = self.html_iterator.search(html_copy)
        
        while (last_video_id != last_local_id and itererator_reg is not None):
            result:str = result + itererator_reg.group()
            last_video_id = self.get_first_item(itererator_reg.group())
            html_copy = html_copy[itererator_reg.end():]
            itererator_reg = self.html_iterator.search(html_copy)

        #HTML LOCALE FILTER
        #filters and pulls locale out of html, 7 is the length of "locale=", 9 is to cut off the "_"
        locale_str:str = self.locale_re.search(html).group()[7:9]
        #add locale to jon_str as a json object
        result = "{\"locale\":\"" + locale_str + "\"}," + result

        #add first bracket
        result = "[" + result[:-1] + "]"

        return result

    def get_first_item(self, source:str) -> str:
        return self.video_id_re.search(source).group()[10:-1]
