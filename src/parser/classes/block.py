from src.parser.classes.statement import Statement

from src.interpreter.visitor import Visitor
from src.interpreter.component import Component


class Block(Component):
    def __init__(self, statements=None):
        if statements is None:
            statements = list()
        self._statements: list[Statement] = statements

    def __eq__(self, other):
        return self.statements == other.statements

    @property
    def statements(self) -> list[Statement]:
        return self._statements

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_block(self)
