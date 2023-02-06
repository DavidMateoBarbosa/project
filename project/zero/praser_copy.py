from typing import *
from logic import *
from io import TextIOWrapper


class _Parser:
    logic: LogicAndGraphic
    script: TextIOWrapper | list
    vars: dict[str, Any]
    available_commands: dict[str, Callable[[Self, Any], Any]]
    def __init__(self, file: TextIOWrapper) -> None:
        self.logic = LogicAndGraphic()
        self.script = list(file)
        self.vars = {}
        self.available_commands = {
            'assingTo': self.assingTo,
            'goto': self.goto,
            'move': self.move,
            'turn': self.turn,
            'face': self.face,
            'put': self.put,
            'pick': self.pick,
            'moveToThe': self.moveToThe,
            'moveInDir': self.moveInDir,
            'jumpToThe': self.jumpToThe,
            'jumpInDir': self.jumpInDir
        }
        self._parser()

    def _parser(self) -> None:
        _is_in_commands = False
        for line in self.script:
            print(line)
            if line == "[" or line.startswith("["):
                if line.startswith("[ ") or line.startswith(" "):
                    raise TypeError()
                _is_in_commands = True
            if _is_in_commands:
                print(line)
                self._commands(line)
            else:
                pass

    def _commands(self, line: str) -> None:
        line = line.replace(" ","")
        if line.startswith("["):
            line = line[1:]
        if line.endswith("]"):
            line = line[:-1]
        sentinel_1 = line.endswith(";\n")
        sentinel_2 = line.endswith("\n;")
        print(sentinel_1, sentinel_2)
        if (not sentinel_1) and (not sentinel_2):
            raise TypeError()
        


        print(line)

    def assingTo(self, n) -> ...: ...
    def goto(self, x, y) -> ...: ...
    def move(self, n) -> ...: ...
    def turn(self, D) -> ...: ...
    def face(self, O) -> ...: ...
    def put(self, n, item) -> ...: ...
    def pick(self, n, item) -> ...: ...
    def moveToThe(self, n, D) -> ...: ...
    def moveInDir(self, n, O) -> ...: ...
    def jumpToThe(self, n, D) -> ...: ...
    def jumpInDir(self, n, O) -> ...: ...



def parser(file: str) -> Literal["script and execution good request", "script good request, execution bad request", "script bad request"]:
    with open(file, mode='r', encoding='utf-8') as file:
            parse = _Parser(file)
            print(parse.logic.first_last_state())
    try:
        print(file)
        with open(file, mode='r', encoding='utf-8') as file:
            parse = _Parser(file)
            print(parse.logic.first_last_state())
        return "script and execution good request"
    except InvalidCommand:
        return "script good request, execution bad request"
    except TypeError:
        return "script bad request"
    
print(parser(r"C:\Users\LoganTaurus\Desktop\project\bot.txt"))