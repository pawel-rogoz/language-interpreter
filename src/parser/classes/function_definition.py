from typing import TYPE_CHECKING

from src.interpreter.base_function_definition import BaseFunctonDefinition

if TYPE_CHECKING:
    from src.scanner.position import Position

    from src.parser.classes.parameter import Parameter
    from src.parser.classes.block import Block
    from src.parser.classes.type import BaseType

    from src.interpreter.visitor import Visitor


class FunctionDefinition(BaseFunctonDefinition):
    def __init__(self, name: str, type: 'BaseType', parameters: ['Parameter'], block: 'Block', position: 'Position') -> None:
        super().__init__(parameters)
        self.name = name
        self.type = type
        self.block = block
        self.position = position

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_function_definition(self)
