from typing import *
from praser import *

@overload
def start_project(): ...

def start_project(with_exceptions: ExceptionState = True, with_graphic: bool = False):
    commands = input("enter the commands separate with ';'")
    parser_state = bool(parser(commands, with_exceptions, with_graphic))
    print("Yes" if parser_state else "No")


__all__ = "start_project",