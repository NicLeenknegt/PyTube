from data.repository.RepositoryDecorator import fetch_request, insert_request, delete_request

from domain.Video import Video
from datetime import datetime

@fetch_request("select * from video order by upload_date desc limit ?")
def fetch_all_videos(cursor, amountt:int) -> [Video]:
    fetched_videos:[Video] = []
    for row in cursor:
        fetched_videos.append(Video(row[0],row[1], datetime.fromisoformat(row[2]), row[3]))
     
    return fetched_videos

@fetch_request("select * from new_videos order by upload_date desc")
def fetch_new_videos(cursor = None) -> [Video]:
    fetched_videos:[Video] = []
    for row in cursor:
        fetched_videos.append(Video(row[0],row[1], datetime.fromisoformat(row[2]), row[3]))
     
    return fetched_videos

@insert_request("video")
def insert_video(vid:Video):
    sql_title:str = vid.title.replace("'", "''")
    return '( "' + vid.id + '",\'' + sql_title + '\',"' + vid.upload_date.isoformat() + '","' + vid.subscription_name + '")'

def insert_video_and_new_video(vid:Video):
    insert_video(vid)
    insert_new_video(vid.id)

@insert_request("new_video")
def insert_new_video(vid_id:str):
    return '( "' + vid_id + '" )'

@insert_request("video")
def insert_video_list(vids:[Video]):
    query:str = ""
    for vid in vids:
        sql_title:str = vid.title.replace("'", "''")
        query = query + '( "' + vid.id + '",\'' + sql_title + '\',"' + vid.upload_date.isoformat() + '","' + vid.subscription_name + '")'
        query = query + ','
    query = query[:-1]
    return query

@fetch_request("select * from video where subscription_name = ? order by upload_date desc")
def fetch_all_videos_of_subscription(cursor, subscription_name:str):
    fetched_videos:[Video] = []
    for row in cursor:
        fetched_videos.append(Video(row[0],row[1], datetime.fromisoformat(row[2]), row[3]))
     
    return fetched_videos

def delete_video_cascade(video_id:str):
    delete_new_video(None, video_id)
    delete_video(None, video_id)

@delete_request("video", "where id = ?") 
def delete_video(cursor, video_id:str):
    for row in cursor:
        print(row)
    return cursor

@delete_request("new_video", "where video_id = ?") 
def delete_new_video(cursor, video_id:str):
    for row in cursor:
        print(row)
    return cursor

@fetch_request("select * from new_video_max_date") 
def fetch_new_video_max_date(cursor = None):
    for row in cursor:
        max_date:datetime = datetime.fromisoformat(row[0])
    return max_date
