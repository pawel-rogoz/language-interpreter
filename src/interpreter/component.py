from abc import ABC, abstractmethod

from src.interpreter.visitor import Visitor


class Component(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass
