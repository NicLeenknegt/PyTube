from re import compile, Match
from domain.content_filter.IContentFilter import IContentFilter
from log.file_logger import log

class Youtube2020Filter(IContentFilter):
    
    def __init__(self):
        self.html_re = compile(r"\"items\":\[\{\"gridVideoRenderer\".*?\"}]}}}]}}]")
        self.locale_re = compile(r"locale=.*?_")
        self.video_id_re = compile(r"videoId\":\".*?\"")
        self.html_iterator = compile(r"{\"gridVideoRenderer\".*?thumbnailOverlayNowPlayingRenderer.*?}}}]}}(,|])")

    def get_content(self, html:str, last_local_id:str) -> str:

        #HTML LOCALE FILTER
        locale_str_match = self.locale_re.search(html)
        if locale_str_match is None:
            raise ValueError("filter error: filtering locale failed")
        #filters and pulls locale out of html, 7 is the length of "locale=", 9 is to cut off the "_"
        locale_str:str = locale_str_match.group()[7:9]
        #add locale to jon_str as a json object
        result:str = "{\"locale\":\"" + locale_str + "\"},"

        #HTML ITERATOR
        last_video_id = self.get_first_item(html)
        if last_video_id == last_local_id:
            return None
        
        itererator_reg = self.html_iterator.search(html)
        
        while (last_video_id != last_local_id and itererator_reg is not None):
            result:str = result + itererator_reg.group()
            last_video_id = self.get_first_item(itererator_reg.group())
            html = html[itererator_reg.end():]
            itererator_reg = self.html_iterator.search(html)

        #add first bracket
        result = "[" + result[:-1] + "]"

        return result

    def get_first_item(self, source:str) -> str:
        id_match = self.video_id_re.search(source)
        if id_match is None:
            raise ValueError("filter error: filtering first video id failed")
        return id_match.group()[10:-1]
