from abc import ABC, abstractmethod

from src.scanner.position import Position

from src.parser.classes.type import Type, BaseType

from src.interpreter.visitor import Visitor
from src.interpreter.component import Component


class Expression(Component):
    def __init__(self, position: Position = Position(1, 1)):
        self._position = position

    @property
    def position(self) -> Position:
        return self._position

    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass


class BinaryExpression(Expression):
    def __init__(self, left: Expression, right: Expression, position: Position = Position(1, 1)):
        super().__init__(position)
        self._left = left
        self._right = right

    @property
    def left(self) -> Expression:
        return self._left

    @property
    def right(self) -> Expression:
        return self._right

    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass


class UnaryExpression(Expression):
    def __init__(self, expression: Expression, position: Position = Position(1, 1)):
        super().__init__(position)
        self._expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression

    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass


class CastingExpression(UnaryExpression, Component):
    def __init__(self, expression, type: BaseType, position: Position = Position(1, 1)):
        super().__init__(expression, position)
        self._type = type

    @property
    def type(self) -> BaseType:
        return self._type

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_casting_expression(self)


class IndexingExpression(UnaryExpression, Component):
    def __init__(self, expression, index: Expression, position: Position = Position(1, 1)):
        super().__init__(expression, position)
        self._index = index

    @property
    def index(self) -> Expression:
        return self._index

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_indexing_expression(self)


class LiteralExpression(Expression, Component):
    def __init__(self, type, value, position: Position = Position(1, 1)):
        super().__init__(position)
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

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_literal_expression(self)

# IdOrCallExpression
# inside can be either
# FunctionCallExpression -> if we just have one id and ({arguments}), no dot
# IdExpression -> if we have only id, no parentheses, no dot
# DotCallExpression -> if we have at least one dot
# DotCallExpression has its left and right side
# left side can be an id expression (on first left side)
# another expression can be either


class IdOrCallExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_id_or_call_expression(self)


class IdExpression(Expression, Component):
    def __init__(self, id: str, position: Position = Position(1, 1)):
        super().__init__(position)
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    def accept(self, visitor: Visitor):
        visitor.visit_id_expression(self)


class FunctionCallExpression(Expression, Component):
    def __init__(self, id: str, arguments: [Expression], position: Position = Position(1, 1)):
        super().__init__(position)
        self._id = id
        self._arguments = arguments

    @property
    def id(self) -> str:
        return self._id

    @property
    def arguments(self) -> [Expression]:
        return self._arguments

    @arguments.setter
    def arguments(self, arguments: [Expression]) -> None:
        self._arguments = arguments

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_function_call_expression(self)


class DotCallChildrenExpression(Expression):
    def __init__(self, id: str, position: Position = Position(1, 1)):
        super().__init__(position)
        self._id = id

    @property
    def id(self):
        return self._id

    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass


class FieldAccessExpression(DotCallChildrenExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_field_access_expression(self)


class MethodCallExpression(DotCallChildrenExpression, Component):
    def __init__(self, id: str, arguments: [Expression], position: Position = Position(1, 1)):
        super().__init__(id, position)
        self._arguments = arguments

    @property
    def arguments(self):
        return self._arguments

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_method_call_expression(self)


class MethodCallAndFieldAccessExpression(DotCallChildrenExpression, Component):
    def __init__(self, id: str, arguments: [Expression], index: Expression, position: Position = Position(1, 1)):
        super().__init__(id, position)
        self._arguments = arguments
        self._index = index

    @property
    def arguments(self):
        return self._arguments

    @property
    def index(self):
        return self._index

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_method_call_and_field_access_expression(self)


class IndexAccessExpression(DotCallChildrenExpression, Component):
    def __init__(self, id: str, index: Expression, position: Position = Position(1, 1)):
        super().__init__(id, position)
        self._index = index

    @property
    def index(self):
        return self._index

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_index_access_expression(self)


class FunctionCallAndIndexExpression(DotCallChildrenExpression, Component):
    def __init__(self, id: str, arguments: [Expression], index: Expression, position: Position = Position(1, 1)):
        super().__init__(id, position)
        self._arguments = arguments
        self._index = index

    @property
    def arguments(self):
        return self._arguments

    @property
    def index(self):
        return self._index

    def accept(self, visitor: Visitor):
        visitor.visit_function_call_and_index_expression(self)


class ClassInitializationExpression(Expression, Component):
    def __init__(self, type, arguments, position: Position = Position(1, 1)):
        super().__init__(position)
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

    def accept(self, visitor: Visitor):
        visitor.visit_class_initialization_expression(self)


class OrExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_or_expression(self)


class AndExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_and_expression()


class RelationExpression(BinaryExpression):
    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass


class GreaterExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_greater_expression(self)


class LessExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_less_expression(self)


class GreaterEqualExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_greater_equal_expression(self)


class LessEqualExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_less_equal_expression(self)


class EqualExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_equal_expression(self)


class NotEqualExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_not_equal_expression(self)


class MultiplicationExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_multiplication_expression(self)


class DivisionExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_division_expression(self)


class AdditionExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_addition_expression(self)


class SubtractionExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_subtraction_expression(self)


class DotCallExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_dot_call_expression(self)


class NegationExpression(UnaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_negation_expression(self)


class UnarySubtractionExpression(UnaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_unary_subtraction_expression(self)


class TermExpression(UnaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_term_expression(self)
