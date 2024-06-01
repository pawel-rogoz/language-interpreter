from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.interpreter.visitor import Visitor


class Component(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass
