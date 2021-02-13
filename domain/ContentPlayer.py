import os
from subprocess import call, PIPE

class ContentPlayer:

    def __init__(self, name:str, command:str, args:str = None, is_active:bool = False):
        self.name = name
        self.command = command + " " + ("" if args is None else args)
        self.is_active = is_active

    def play(self, url:str):
        run_command = self.command + ' ' + url 
        result = call(run_command, stdout=PIPE, shell=True, stderr=PIPE)
        if result > 0:
            raise ValueError("player failure: executing the command \"{}\" failed".format(run_command))

    def __str__(self):
        return "{0:30}{1:100}{2}".format(self.name, self.command, "ACTIVE" if self.is_active else "")

    def to_dict(self) -> dict:
        return {
                "name":self.name,
                "command":self.command,
                "is_active":self.is_active
                }

def content_player_from_dict(json:dict):
    return ContentPlayer(
            json['name'],
            json['command'],
            None,
            json['is_active']
            )
