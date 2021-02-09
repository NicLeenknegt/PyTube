#!/usr/bin/env python3
import sys
from command.ShowNewVideosCommand import ShowNewVideosCommand
from command.SelectCommand import SelectCommand
from command.ShowOldVideosCommand import ShowOldVideosCommand
from command.DeleteCommand import DeleteCommand
from command.AddSubscriptionCommand import AddSubscriptionCommand
from command.ShowSubscriptionsCommand import ShowSubscriptionsCommand
from command.ShowContentPlayerCommand import ShowContentPlayerCommand
from command.AddContentPlayerCommand import AddContentPlayerCommand
from command.ICommand import ICommand

def main(argv):
    
    command_array = [
            SelectCommand(),
            ShowNewVideosCommand(),
            ShowOldVideosCommand(),
            DeleteCommand(),
            AddSubscriptionCommand(),
            ShowSubscriptionsCommand(),
            ShowContentPlayerCommand(),
            AddContentPlayerCommand()
            ]

    for command in command_array:
        if argv[0] in command.get_options():
            try:
                command.execute(*argv)
            except ValueError as err:
                print("pytube: " + err.args[0])

if __name__ == '__main__':
    main(sys.argv[1:])
