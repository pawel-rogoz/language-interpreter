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

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value


class CallExpression(Expression):
    def __init__(self, arguments):
        self._arguments = arguments

    @property
    def arguments(self):
        return self._arguments


# IdOrCallExpression
# inside can be either
# FunctionCallExpression -> if we just have one id and ({arguments}), no dot
# IdExpression -> if we have only id, no parentheses, no dot
# DotCallExpression -> if we have at least one dot
# DotCallExpression has its left and right side
# left side can be an id expression (on first left side)
# another expression can be either
class IdOrCallExpression(BinaryExpression):
    pass


class IdExpression(Expression):
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id


class FunctionCallExpression(Expression):
    def __init__(self, id: str, call: CallExpression):
        self._id = id
        self._call = call


class DotCallChildrenExpression(Expression, ABC):
    def __init__(self, id: str):
        self._id = id

    @property
    def id(self):
        return self._id


class FieldAccessExpression(DotCallChildrenExpression):
    pass


class MethodCallExpression(DotCallChildrenExpression):
    def __init__(self, id: str, call: CallExpression):
        super().__init__(id)
        self._call = call

    @property
    def call(self):
        return self._call


class MethodCallAndFieldAccessExpression(DotCallChildrenExpression):
    def __init__(self, id: str, call: CallExpression, index: Expression):
        super().__init__(id)
        self._call = call
        self._index = index

    @property
    def call(self):
        return self._call

    @property
    def index(self):
        return self._index


class IndexAccessExpression(DotCallChildrenExpression):
    def __init__(self, id: str, index: Expression):
        super().__init__(id)
        self._index = index

    @property
    def index(self):
        return self._index


class FunctionCallAndIndexExpression(DotCallChildrenExpression):
    def __init__(self, id: str, call: CallExpression, index: Expression):
        super().__init__(id)
        self._call = call
        self._index = index

    @property
    def call(self):
        return self._call

    @property
    def index(self):
        return self._index


class ClassInitializationExpression(Expression):
    def __init__(self, type, arguments):
        self._type: Type = type
        self._arguments: list[Expression] = arguments

    def __eq__(self, other):
        return self.type == other.type and self.arguments == other.arguments

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


class DotCallExpression(BinaryExpression):
    pass


class NegationExpression(UnaryExpression):
    pass


class UnarySubtractionExpression(UnaryExpression):
    pass


class TermExpression(UnaryExpression):
    pass
