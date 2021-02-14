from command.ICommand import ICommand
from data.repository.ContentPlayerRepository import update_content_player, fetch_content_players
from data.repository.SelectionListRepository import save_content_player_to_selection_list
from domain.ContentPlayer import ContentPlayer
from sqlite3 import OperationalError
from view.MessageView import print_select_success_message

class ContentPlayerSelectCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 2:
            raise ValueError("internal error: ContentPlayerSelectCommand receives wrong arguments from SelectCommand")     

    def run(self, *argv):
        index:int = argv[0]
        result:[ContentPlayer] = argv[1]

        try:
            update_content_player(None, result[index].name)
        except OperationalError:
            raise ValueError("database failure: failed to set the active player")

        # updates the list of content players if the user decides to select multiple times,
        save_content_player_to_selection_list(fetch_content_players())
        print_select_success_message("player", result[index].name)

    def get_short_option(self) -> str:
        return None

    def get_long_option(self) -> str:
        return "content_player"

