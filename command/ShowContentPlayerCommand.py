from view.ListView import show_list
from data.repository.ContentPlayerRepository import fetch_content_players
from data.repository.SelectionListRepository import save_content_player_to_selection_list
from command.ICommand import ICommand
from sqlite3 import OperationalError

class ShowContentPlayerCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) != 1:
            raise ValueError("illegal format: pytube [--players|-p]")
    
    def run(self, *argv):
        try:
            players:[ContentPlayer] = fetch_content_players()
        except OperationalError:
            raise ValueError("database failure: an error ocurred while retreiving the players")
        save_content_player_to_selection_list(players)
        show_list(players, "players")

    def get_short_option(self) -> str:
        return "-p"

    def get_long_option(self) -> str:
        return "--players"

