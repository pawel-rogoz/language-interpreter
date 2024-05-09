from src.parser.classes.statement import *


class Block:
    def __init__(self, statements=None):
        if statements is None:
            statements = list()
        self._statements: list[Statement] = statements

    def __eq__(self, other):
        return self.statements == other.statements

    @property
    def statements(self) -> list[Statement]:
        return self._statements
