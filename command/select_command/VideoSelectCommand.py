from data.repository.ContentPlayerRepository import fetch_active_content_player
from command.ICommand import ICommand
from domain.ContentPlayer import ContentPlayer
from data.repository.SelectionListRepository import remove_item_from_selection_list
from data.repository.VideoRepository import delete_new_video

class VideoSelectCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 2:
            raise ValueError("internal error: VideoSelectCommand receives wrong arguments from SelectCommand")     

    def run(self, *argv):
        index:int = argv[0]
        result:[Video] = argv[1]
        content_player:ContentPlayer = fetch_active_content_player()
         
        content_player.play('https://www.youtube.com/watch?v=' + result[index].id)
        '''
        This removes the selected item from the locally saves selection list
        I still wonder whether it wouldn't be better to allow the user to reselect the previously selected video.
        Perhaps I should make a seperate command for that.
        '''
        remove_item_from_selection_list(index)
        delete_new_video(None, result[index].id)

    def get_short_option(self) -> str:
        return None

    def get_long_option(self) -> str:
        return "video"

