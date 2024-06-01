from src.parser.classes.parameter import Parameter
from src.parser.classes.block import Block
from src.parser.classes.type import BaseType
from src.scanner.position import Position

from src.interpreter.visitor import Visitor
from src.interpreter.component import Component


class FunctionDefinition(Component):
    def __init__(self, name, type, parameters, block, position):
        self.name: str = name
        self.type: BaseType = type
        self.parameters: list[Parameter] = parameters
        self.block: Block = block
        self.position: Position = position

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_function_definition(self)

    # def visit(self, scope: Scope):
    #     result = self.block.visit(scope)
    #     if result.type != self.type:
    #         raise InterpreterError()
    #     return result
