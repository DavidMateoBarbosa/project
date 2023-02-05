from typing import *
from logic import *

def _f(): ...

CommandName: TypeAlias = str
Command: TypeAlias = _f.__class__
Commands: TypeAlias = dict[CommandName, Command]

class _Parser:
    "load commands in console raise if execute the commands is imposible"
    logic: LogicAndGraphic
    commands: Commands
    static_commands: Commands
    graphic: bool
    def __init__(self, commands: str, with_exceptions: ExceptionState = True) -> None:
        "if with_exceptions is False the goal can't be reached"
        self.logic = LogicAndGraphic(with_exceptions)
        self._build_commands()

    def _load_commands(self): ...

    def _build_commands(self) -> None:
        self.static_commands = {
            "M": self.logic.move_forward,
            "R": self.logic.rotate_right,
            "C": self.logic.put_chip,
            "B": self.logic.put_balloon,
            "c": self.logic.pick_chip,
            "b": self.logic.pick_balloon,
            "P": self.logic.pop_balloon,
            "J": self.logic.jump_to,
            "G": self.logic.go_to
        }


    def block_checker(line: str) -> bool:
        if line.startswith("[") and line.endswith("]"):
            return True
        return False

    def first_last_state(self) -> str:
        return self.logic.first_last_state()


def parser(file: str, with_exceptions: ExceptionState = True, with_graphic: bool = False) -> Literal[0, 1]:
    try:
        with open(file) as file:
            _parser = _Parser(file, with_exceptions)
            if with_graphic:
                print(_parser.first_last_state())
            return 1
    except InvalidCommand:
        return 0


print(parser("1,2,3,4,5,6,7",with_graphic=True), )

str = ""

str = str.split("]")[0]