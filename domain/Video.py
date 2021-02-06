from datetime import datetime

class Video:

    def __init__(self, vid_id:str, title:str, date:datetime, subscription_name:str):
        self.id = vid_id
        self.title = title
        self.upload_date:datetime = date
        self.subscription_name = subscription_name

    def __str__(self) -> str:
        return "{0:30}{1:120}{2}".format(self.subscription_name, self.title, self.upload_date.isoformat())

    def to_dict(self) -> dict:
        return { 
                "id":self.id,
                "title":self.title,
                "upload_date":self.upload_date.isoformat(),
                "subscription_name": self.subscription_name
                }

def vid_from_dict(json:dict):
    return Video(
            json['id'],
            json['title'],
            datetime.fromisoformat(json['upload_date']),
            json['subscription_name']
            )
