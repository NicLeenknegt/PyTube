from command.ICommand import ICommand
from data.repository.ContentPlayerRepository import update_content_player, fetch_content_players
from data.repository.SelectionListRepository import save_content_player_to_selection_list
from domain.ContentPlayer import ContentPlayer

class ContentPlayerSelectCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 2:
            raise ValueError("internal error: ContentPlayerSelectCommand receives wrong arguments from SelectCommand")     

    def run(self, *argv):
        index:int = argv[0]
        result:[ContentPlayer] = argv[1]

        update_content_player(None, result[index].name)
        save_content_player_to_selection_list(fetch_content_players())

    def get_short_option(self) -> str:
        return None

    def get_long_option(self) -> str:
        return "content_player"

