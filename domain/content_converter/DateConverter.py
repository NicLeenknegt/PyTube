import re
from domain.content_converter.IContentConverter import IContentConverter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from domain.DateMatchesDict import py_tube_date_matches

class DateConverter(IContentConverter):

    def __init__(self):
        self.word_re = re.compile(r"\d+\s\S*?\s")
        self.space_re = re.compile(r"\s")

    def convert(self, json_str:str, name:str) -> datetime:
        time_relative:relativedelta = None

        now:datetime = datetime.now()
        years:int = 0
        months:int = 0
        weeks:int = 0
        days:int = 0
        hours:int = 0
        minutes:int = 0
        seconds:int = 0
        
        date_matches:dict = py_tube_date_matches

        for re_find in self.word_re.findall(json_str):
            pair:[str] = self.space_re.split(re_find)
            if pair[1].startswith(date_matches['year']):
                years = int(pair[0])
            elif pair[1].startswith(date_matches['months']):
                months = int(pair[0])
            elif pair[1].startswith(date_matches['weeks']):
                weeks = int(pair[0])
            elif pair[1].startswith(date_matches['days']):
                days = int(pair[0])
            elif pair[1].startswith(date_matches['hours']):
                hours = int(pair[0])
            elif pair[1].startswith(date_matches['minutes']):
                minutes = int(pair[0])
            elif pair[1].startswith(date_matches['seconds']):
                seconds = int(pair[0])

        time_relative = relativedelta(
                years=- years,
                months =- months,
                weeks =- weeks,
                days=-days,
                hours =- hours,
                minutes =- minutes,
                seconds =- seconds
                )

        return now + time_relative
        
