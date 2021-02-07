import os
from subprocess import call, PIPE

class ContentPlayer:

    def __init__(self, name:str, command:str, is_active:bool = False):
        self.name = name
        self.command = command
        self.is_active = is_active

    def play(self, url:str):
        run_command = self.command + ' ' + url
        result = call(run_command, stdout=PIPE, shell=True)
        if result > 0:
            raise ValueError("content player command failed")

    def __str__(self):
        return "{0:30}{1:100}{2}".format(self.name, self.command, "ACTIVE" if self.is_active else "")
