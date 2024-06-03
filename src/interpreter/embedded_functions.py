from typing import TYPE_CHECKING

from src.parser.classes.parameter import Parameter
from src.parser.classes.type import BaseType, Type

from src.interpreter.base_function_definition import BaseFunctonDefinition
from src.interpreter.component import Component

if TYPE_CHECKING:
    from src.interpreter.visitor import Visitor


class PrintFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[Parameter(BaseType(Type.STRING), '_'),]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_print_function(self)
