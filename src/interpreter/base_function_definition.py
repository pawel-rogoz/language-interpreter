from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from src.interpreter.component import Component

if TYPE_CHECKING:
    from src.parser.classes.parameter import Parameter
    from src.interpreter.visitor import Visitor


class BaseFunctonDefinition(Component):
    def __init__(self, parameters: ['Parameter']):
        self.parameters = parameters

    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass
