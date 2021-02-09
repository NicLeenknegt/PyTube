from view.MessageView import print_insert_success_message
from command.ICommand import ICommand
from domain.ContentPlayer import ContentPlayer
from data.repository.ContentPlayerRepository import insert_content_player
from shutil import which
from sqlite3 import OperationalError, IntegrityError

class AddContentPlayerCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) < 3 or len(argv) > 5:
            raise ValueError("illegal format: pytube --add-player [name] [command] [active]")
        if len(argv) == 5 and argv[4] != "active":
            raise ValueError("illegal argument: third optional argument has to be 'active'")
        if which(argv[2].replace("\\","")) is None:
            raise ValueError("illegal argument: command does not exist")
        
    def run(self, *argv):
        
        if len(argv) == 5 and argv[4] == "active":
            content_player = ContentPlayer(argv[1], argv[2], argv[3], True)
        elif len(argv) == 4 and argv[3] == "active":
            content_player = ContentPlayer(argv[1], argv[2], None, True)
        elif len(argv) == 4:
            content_player = ContentPlayer(argv[1], argv[2], argv[3])
        elif len(argv) == 3:
            content_player = ContentPlayer(argv[1], argv[2])
        try:
            insert_content_player(content_player)
        except OperationalError as err:
            raise ValueError("database failure: something went wrong while inserting a new player")
        except IntegrityError as err:
            raise ValueError("database failure: there already exists a player with name \"{}\"".format(content_player.name))
        
        print_insert_success_message("\"{0}\" player".format(content_player.name))

    def get_short_option(self) -> str:
        return None

    def get_long_option(self) -> str:
        return "--add-player"

