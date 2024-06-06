from src.parser.classes.expressions.expression import Expression
from src.parser.classes.type import Type


class LiteralExpression(Expression):
    def __init__(self, type, value):
        self._type: Type = type
        self._value = value

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value