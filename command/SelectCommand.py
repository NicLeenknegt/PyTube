from data.repository.SelectionListRepository import read_selection_list, get_selection_list_type
from command.ICommand import ICommand
from command.select_command.VideoSelectCommand import VideoSelectCommand
from command.select_command.SubscriptionSelectCommand import SubscriptionSelectCommand
from command.select_command.ContentPlayerSelectCommand import ContentPlayerSelectCommand

class SelectCommand(ICommand):

    def validate_input(self, *argv):
        if len(argv) == 1:
            raise ValueError("missing argument: [--select|-s] needs index argument")
        if len(argv) != 2:
            raise ValueError("illegal format: pytube [--select|-s] index")
    
    def run(self, *argv):
        
        command_array:[ICommand] = [ 
                VideoSelectCommand(), 
                SubscriptionSelectCommand(),
                ContentPlayerSelectCommand()
                ]

        try:
            index:int = int(argv[1])
        except ValueError as err:
            raise ValueError("illegal format: index needs to be number")

        result = read_selection_list()

        if (index < 0 or index >= len(result)):
            raise ValueError("index out of range: needs to be between {0} and {1}".format(0, len(result) - 1))

        for command in command_array:
            if get_selection_list_type() == command.get_long_option():
                command.execute(index, result)

    def get_short_option(self) -> str:
        return "-s"

    def get_long_option(self) -> str:
        return "--select"

