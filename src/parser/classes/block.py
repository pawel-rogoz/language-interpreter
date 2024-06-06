from typing import TYPE_CHECKING

from src.interpreter.component import Component

if TYPE_CHECKING:
    from src.parser.classes.statement import Statement
    from src.interpreter.visitor import Visitor


class Block(Component):
    def __init__(self, statements: ['Statement'] = None) -> None:
        if statements is None:
            statements = list()
        self._statements = statements

    def __eq__(self, other) -> bool:
        return self._statements == other.statements

    @property
    def statements(self) -> list['Statement']:
        return self._statements

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_block(self)
