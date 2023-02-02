r"""
>>> (lym) Machines And Languages 
>>> Projects
Authors Info
+---------------------------------------------------------------------------------+
|        >>> Author <<<        | Author ID |         Author mail        | seccion |
|------------------------------|-----------|----------------------------|---------|
| David Mateo Barbosa Monsalve | 202110756 | d.barbosam@uniandes.edu.co |    3    |
| ...                          | ...       | ...                        | ...     |
+---------------------------------------------------------------------------------+
Module info:
+---------------------------------------------------------------------------------+
|packages:                                                                        |
|   .zero                                                                         |
|   ...                                                                           |
|to use:                                                                          |
|   import project.zero                                                           |
|   ...                                                                           |
|Required Modules: # NOTE: missing module raise _utils.MissingModule              |
|    typing -> (builtin module)                                                   |
|    tkinter -> (pip install tk)                                                  |
|    pandas -> (pip install pandas)                                               |
+---------------------------------------------------------------------------------+
"""

from ._utils import modules_cheker as _modules_cheker

_modules_cheker()

from . import zero


__all__ = "zero", 