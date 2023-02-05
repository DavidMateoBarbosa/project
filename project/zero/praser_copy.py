from typing import *
from logic import *
from io import TextIOWrapper


class _Parser:
    file: TextIOWrapper | list
    def __init__(self, file: TextIOWrapper) -> None:
        self.logic = LogicAndGraphic()
        self.file = file
        self.clean_file()
        self.check_headers()

    def clean_file(self) -> None:
        """check the file and ignore unnecessary identations"""
        self.file = list(line.replace("\n", "") for line in self.file)
        while "" in self.file:
            self.file.remove("")
        self.file
    
    def check_headers(self) -> None:
        """check the file and raise if it doesn't starts with ROBOT_R and VARS ..."""
        if self.file[0] != 'ROBOT_R' or not self.file[1].startswith("VARS "):
            raise TypeError(r"script must be start with ROBOT_R\nVARS ..., not", self.file[0], self.file[1])

def parser(file: str) -> bool:
    try:
        print(file)
        with open(file, mode='r', encoding='utf-8') as file:
            _Parser(file)
        return "script and execution good request"
    except InvalidCommand:
        return "script good request, execution bad request"
    except TypeError:
        return "script bad request"