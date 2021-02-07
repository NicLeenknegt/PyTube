from data.repository.RepositoryDecorator import fetch_request, insert_request, delete_request
from domain.ContentPlayer import ContentPlayer

@insert_request("content_player")
def insert_content_player(content_player:ContentPlayer):
    is_active =  '1' if content_player.is_active else '0'
    return '( "' + content_player.name + '","' + content_player.command + '",' + is_active + ')'

@fetch_request("select * from active_content_player")
def fetch_active_content_player(cursor = None) -> ContentPlayer:
    fetched_content_players:[ContentPlayer] = []
    for row in cursor:
        is_active =  True if row[2] == 1 else False
        fetched_content_players.append(ContentPlayer(row[0], row[1], is_active))
    
    return fetched_content_players[0]

@fetch_request("select * from content_player")
def fetch_content_players(cursor = None) -> [ContentPlayer]:
    fetched_content_players:[ContentPlayer] = []
    for row in cursor:
        is_active =  True if row[2] == 1 else False
        fetched_content_players.append(ContentPlayer(row[0], row[1], is_active))
    
    return fetched_content_players
