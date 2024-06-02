from abc import ABC, abstractmethod

from src.interpreter.visitor import Visitor
from src.interpreter.component import Component

from src.parser.classes.type import Type


class Expression(Component):
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

    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass


class UnaryExpression(Expression):
    def __init__(self, expression: Expression):
        self._expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression

    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass


class CastingExpression(UnaryExpression, Component):
    def __init__(self, expression, type=None):
        super().__init__(expression)
        self._type = type

    @property
    def type(self):
        return self._type

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_casting_expression(self)


class IndexingExpression(UnaryExpression, Component):
    def __init__(self, expression, index=None):
        super().__init__(expression)
        self._index = index

    @property
    def index(self):
        return self._index

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_indexing_expression(self)


class LiteralExpression(Expression, Component):
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

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_literal_expression(self)


class CallExpression(Expression, Component):
    def __init__(self, arguments):
        self._arguments = arguments

    @property
    def arguments(self):
        return self._arguments

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_call_expression(self)


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
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    def accept(self, visitor: Visitor):
        visitor.visit_id_expression(self)


class FunctionCallExpression(Expression, Component):
    def __init__(self, id: str, call: CallExpression):
        self._id = id
        self._call = call

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_function_call_expression(self)

    # def visit(self, scope: Scope):
    #     if self._id in scope.global_scope.functions.keys():
    #         self._call.visit(scope)
    #     raise InterpreterError()


class DotCallChildrenExpression(Expression):
    def __init__(self, id: str):
        self._id = id

    @property
    def id(self):
        return self._id


class FieldAccessExpression(DotCallChildrenExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_field_access_expression(self)


class MethodCallExpression(DotCallChildrenExpression, Component):
    def __init__(self, id: str, call: CallExpression):
        super().__init__(id)
        self._call = call

    @property
    def call(self):
        return self._call

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_method_call_expression(self)


class MethodCallAndFieldAccessExpression(DotCallChildrenExpression, Component):
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

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_method_call_and_field_access_expression(self)


class IndexAccessExpression(DotCallChildrenExpression, Component):
    def __init__(self, id: str, index: Expression):
        super().__init__(id)
        self._index = index

    @property
    def index(self):
        return self._index

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_index_access_expression(self)


class FunctionCallAndIndexExpression(DotCallChildrenExpression, Component):
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

    def accept(self, visitor: Visitor):
        visitor.visit_function_call_and_index_expression(self)


class ClassInitializationExpression(Expression, Component):
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

    def accept(self, visitor: Visitor):
        visitor.visit_class_initialization_expression(self)


class OrExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_or_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     if not isinstance(left, bool):
    #         raise InterpreterError()
    #     if left:
    #         return BaseValue(BaseType(Type.BOOL), True)
    #     right = self.right.visit(scope)
    #     if not isinstance(right, bool):
    #         raise InterpreterError()
    #     return BaseValue(BaseType(Type.BOOL), right)


class AndExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_and_expression()

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     if not isinstance(left, bool):
    #         raise InterpreterError()
    #     if not left:
    #         return BaseValue(BaseType(Type.BOOL), False)
    #     right = self.right.visit(scope)
    #     if not isinstance(right, bool):
    #         raise InterpreterError()
    #     return BaseValue(BaseType(Type.BOOL), right)


class RelationExpression(BinaryExpression):
    pass


class GreaterExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_greater_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if not isinstance(left, type(right)):
    #         raise InterpreterError()
    #     if not isinstance(left, Union[int, float]):
    #         raise InterpreterError()
    #     return BaseValue(BaseType(Type.BOOL), left > right)


class LessExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_less_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if not isinstance(left, type(right)):
    #         raise InterpreterError()
    #     if not isinstance(left, Union[int, float]):
    #         raise InterpreterError()
    #     return BaseValue(BaseType(Type.BOOL), left < right)


class GreaterEqualExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_greater_equal_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if not isinstance(left, type(right)):
    #         raise InterpreterError()
    #     if not isinstance(left, Union[int, float]):
    #         raise InterpreterError()
    #     return BaseValue(BaseType(Type.BOOL), left >= right)


class LessEqualExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_less_equal_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if not isinstance(left, type(right)):
    #         raise InterpreterError()
    #     if not isinstance(left, Union[int, float]):
    #         raise InterpreterError()
    #     return BaseValue(BaseType(Type.BOOL), left <= right)


class EqualExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_equal_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if not isinstance(left, type(right)):
    #         raise InterpreterError()
    #     return BaseValue(BaseType(Type.BOOL), left == right)


class NotEqualExpression(RelationExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_not_equal_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if not isinstance(left, type(right)):
    #         raise InterpreterError()
    #     return BaseValue(BaseType(Type.BOOL), left != right)


class MultiplicationExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_multiplication_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if isinstance(left or right, str):
    #         if not isinstance(left or right, int):
    #             raise InterpreterError()
    #         return BaseValue(BaseType(Type.STRING), left * right)
    #     if isinstance(left or right, int):
    #         if isinstance(left or right, float):
    #             return BaseValue(BaseType(Type.FLOAT), left * right)
    #         if not isinstance(left and right, int):
    #             raise InterpreterError()
    #     return BaseValue(BaseType(Type.INT), left * right)


class DivisionExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_division_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if isinstance(left or right, int):
    #         if isinstance(left or right, float):
    #             return BaseValue(BaseType(Type.FLOAT), left / right)
    #         elif isinstance(left and right, int):
    #             return BaseValue(BaseType(Type.INT), left / right)
    #     raise InterpreterError()


class AdditionExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_addition_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if isinstance(left or right, int):
    #         if isinstance(left or right, float):
    #             return BaseValue(BaseType(Type.FLOAT), left + right)
    #         elif isinstance(left and right, int):
    #             return BaseValue(BaseType(Type.INT), left + right)
    #     if isinstance(left and right, str):
    #         return BaseValue(BaseType(Type.STRING), left + right)
    #     raise InterpreterError()


class SubtractionExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_subtraction_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     left = self.left.visit(scope)
    #     right = self.right.visit(scope)
    #     if isinstance(left or right, int):
    #         if isinstance(left or right, float):
    #             return BaseValue(BaseType(Type.FLOAT), left - right)
    #         elif isinstance(left and right, int):
    #             return BaseValue(BaseType(Type.INT), left - right)
    #     raise InterpreterError()


class DotCallExpression(BinaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_dot_call_expression(self)


class NegationExpression(UnaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_negation_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     expression = self.expression.visit(scope)
    #     if isinstance(expression, int):
    #         return BaseValue(BaseType(Type.INT), not expression)
    #     elif isinstance(expression, float):
    #         return BaseValue(BaseType(Type.FLOAT), not expression)
    #     elif isinstance(expression, bool):
    #         return BaseValue(BaseType(Type.BOOL), not bool)
    #     raise InterpreterError()


class UnarySubtractionExpression(UnaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_unary_subtraction_expression(self)

    # def visit(self, scope: Scope) -> BaseValue:
    #     expression = self.expression.visit(scope)
    #     if isinstance(expression, int):
    #         return BaseValue(BaseType(Type.INT), -expression)
    #     elif isinstance(expression, float):
    #         return BaseValue(BaseType(Type.FLOAT), -expression)
    #     raise InterpreterError()


class TermExpression(UnaryExpression, Component):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_term_expression(self)
