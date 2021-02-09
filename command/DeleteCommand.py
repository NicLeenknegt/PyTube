from data.repository.ContentPlayerRepository import delete_content_player
from data.repository.SubscriptionRepository import delete_sub
from data.repository.VideoRepository import delete_video_cascade
from data.repository.SelectionListRepository import read_selection_list, get_selection_list_type, remove_item_from_selection_list
from command.ICommand import ICommand

class DeleteCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 2:
            raise ValueError("illegal format: pytube [--delete|-d] index")
    
    def run(self, *argv):
        
        try:
            index:int = int(argv[1])
        except ValueError as err:
            raise ValueError("illegal format: index needs to be a number")

        result = read_selection_list()
        if get_selection_list_type() == "video":
            delete_video_cascade(result[index].id)
        elif get_selection_list_type() == "subscription":
            delete_sub(None, result[index].url_name)            
        elif get_selection_list_type() == "content_player":
            delete_content_player(None, result[index].name)
        remove_item_from_selection_list(index)

    def get_short_option(self) -> str:
        return "-d"

    def get_long_option(self) -> str:
        return "--delete"

