from view.ListView import show_list
from controller.SubscriptionController import get_new_videos
from data.repository.VideoRepository import fetch_new_videos
from data.repository.SelectionListRepository import save_videos_to_selection_list
from command.ICommand import ICommand
from sqlite3 import OperationalError

class ShowNewVideosCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 1:
            raise ValueError("illegal format: pytube [--new|-n]")


    def run(self, *argv):
        try:
            get_new_videos()
            vids:[Video] = fetch_new_videos()
        except ValueError:
            raise
        except OperationalError:
            raise ValueError("database failure: something went wrong while fetching the new videos")
        save_videos_to_selection_list(vids)
        show_list(vids, "new videos")

    def get_short_option(self) -> str:
        return "-n"

    def get_long_option(self) -> str:
        return "--new"
