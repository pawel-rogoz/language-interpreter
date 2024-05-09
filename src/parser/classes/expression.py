from abc import ABC, abstractmethod
from src.parser.classes.type import Type


class Expression(ABC):
    @abstractmethod
    def __init__(self):
        pass


class BinaryExpression(Expression):
    def __init__(self, left: Expression, right: Expression = None):
        self._left = left
        self._right = right

    @property
    def left(self) -> Expression:
        return self._left

    @property
    def right(self) -> Expression:
        return self._right


class UnaryExpression(Expression):
    def __init__(self, expression: Expression):
        self._expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression


class CastingExpression(UnaryExpression):
    def __init__(self, expression, type=None):
        super().__init__(expression)
        self._type = type

    @property
    def type(self):
        return self._type


class IndexingExpression(UnaryExpression):
    def __init__(self, expression, index=None):
        super().__init__(expression)
        self._index = index

    @property
    def index(self):
        return self._index


class LiteralExpression(Expression):
    def __init__(self, type, value):
        self._type: Type = type
        self._value = value

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value


class IdOrCallExpression(Expression):
    def __init__(self, id, arguments, index, nested_id_or_call):
        self._id: str = id
        self._arguments: list[Expression] = arguments
        self._index: Expression = index
        self._nested_id_or_call: IdOrCallExpression = nested_id_or_call


class ClassInitializationExpression(Expression):
    def __init__(self, type, arguments):
        self._type: Type = type
        self._arguments: list[Expression] = arguments

    @property
    def type(self):
        return self._type

    @property
    def arguments(self):
        return self._arguments


class OrExpression(BinaryExpression):
    pass


class AndExpression(BinaryExpression):
    pass


class RelationExpression(BinaryExpression):
    pass


class GreaterExpression(RelationExpression):
    pass


class LessExpression(RelationExpression):
    pass


class GreaterEqualExpression(RelationExpression):
    pass


class LessEqualExpression(RelationExpression):
    pass


class EqualExpression(RelationExpression):
    pass


class NotEqualExpression(RelationExpression):
    pass


class MultiplicationExpression(BinaryExpression):
    pass


class DivisionExpression(BinaryExpression):
    pass


class AdditionExpression(BinaryExpression):
    pass


class SubtractionExpression(BinaryExpression):
    pass


class NegationExpression(UnaryExpression):
    pass


class UnarySubtractionExpression(UnaryExpression):
    pass


class TermExpression(UnaryExpression):
    pass
