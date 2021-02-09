from view.ListView import show_list
from controller.SubscriptionController import get_new_videos
from data.repository.VideoRepository import fetch_new_videos
from data.repository.SelectionListRepository import save_videos_to_selection_list
from command.ICommand import ICommand

class ShowNewVideosCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 1:
            raise ValueError("illegal format: pytube [--new|-n]")
    
    def run(self, *argv):
        get_new_videos()
        vids:[Video] = fetch_new_videos()
        save_videos_to_selection_list(vids)
        show_list(vids)

    def get_short_option(self) -> str:
        return "-n"

    def get_long_option(self) -> str:
        return "--new"

