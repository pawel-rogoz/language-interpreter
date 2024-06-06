from typing import TYPE_CHECKING

from src.scanner.position import Position

from src.interpreter.component import Component

if TYPE_CHECKING:
    from src.interpreter.visitor import Visitor
    from src.parser.classes.function_definition import FunctionDefinition


class Program(Component):
    def __init__(self, functions: dict[str, 'FunctionDefinition']):
        self._functions = functions
        self._position = Position(1, 0)

    @property
    def functions(self) -> dict[str, 'FunctionDefinition']:
        return self._functions

    @property
    def position(self) -> Position:
        return self._position

    def get_functions(self) -> dict[str, 'FunctionDefinition']:
        return self._functions

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_program(self)
