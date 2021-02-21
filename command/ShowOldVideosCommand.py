from view.ListView import show_list
from data.repository.VideoRepository import fetch_all_videos
from data.repository.SelectionListRepository import save_videos_to_selection_list
from command.ICommand import ICommand
from sqlite3 import OperationalError

class ShowOldVideosCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) > 2:
            raise ValueError("illegal format: pytube [--old|-o]")

    def run(self, *argv):
        amount:int = 25
        if len(argv) > 1:
            try:
                amount = int(argv[1])
            except ValueError as err:
                raise ValueError("argument must be number")
        try:
            vids:[Video] = fetch_all_videos(None, amount)
        except OperationalError:
            raise ValueError("database failure: something went wrong while fetching the old videos")
        save_videos_to_selection_list(vids)
        show_list(vids, "new videos")

    def get_short_option(self) -> str:
        return "-o"

    def get_long_option(self) -> str:
        return "--old"

