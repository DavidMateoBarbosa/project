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
        self.script = list(file)[1:]
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
            if line.startswith(" "):
                raise TypeError()
            if line.replace(" ", "").replace("\n", "") == "[" or line.startswith("["):
                _is_in_commands = True
            elif line.startswith("[ "):
                raise TypeError()
            if _is_in_commands:
                self._commands(line)
    
    def _commands(self, line: str) -> None:
        if line.replace(" ", "").replace("\n", "") == "[" or line.replace(" ", "").replace("\n", "") == "]": return
        line = line.replace(" ", "").replace("\n", "")
        if not line.endswith(";"): raise TypeError()
        line = line[:-1]
        function, params = line.split(":")
        params = params.split(",")
        if function == 'put' or function == 'pick': eval(f"self.{function}({params[0]}, '{params[1]}')")
        else: eval(f"self.{function}({params[0]}, {params[1]})")
        


    def assingTo(self, n) -> ...: ...
    def goto(self, x, y) -> ...:
        self.logic.go_to((x, y))
    def move(self, n) -> ...:
        for _ in range(n):self.logic.move_forward()
    def turn(self, D) -> ...: ...
    def face(self, O) -> ...: ...
    def put(self, n, item) -> ...: 
        for _ in range(n):
            if item == "Balloon":self.logic.put_balloon()
            elif item == "Chip":self.logic.put_chip()
    def pick(self, n, item) -> ...:
        for _ in range(n):
            if item == "Balloon":self.logic.pick_balloon()
            elif item == "Chip":self.logic.pick_chip()
    def moveToThe(self, n, D) -> ...: ...
    def moveInDir(self, n, O) -> ...: ...
    def jumpToThe(self, n, D) -> ...: ...
    def jumpInDir(self, n, O) -> ...: ...



def parser(file: str) -> Literal["script and execution good request", "script good request, execution bad request", "script bad request"]:
    try:
        with open(file, mode='r', encoding='utf-8') as file:
            parse = _Parser(file)
        return "script and execution good request"
    except InvalidCommand:
        return "script good request, execution bad request"
    except TypeError:
        return "script bad request"
    
print(parser(r"C:\Users\LoganTaurus\Desktop\project\bot.txt"))