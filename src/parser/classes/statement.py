from abc import ABC, abstractmethod
from src.parser.classes.expression import Expression


class Statement(ABC):
    @abstractmethod
    def __init__(self):
        pass


class ReturnStatement(Statement):
    def __init__(self, expression):
        self._expression = expression

    @property
    def expression(self):
        return self._expression


class DeclarationStatement(Statement):
    def __init__(self, type, id):
        self._type = type
        self._id = id

    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id


class InitializationStatement(DeclarationStatement):
    def __init__(self, type, id, expression):
        super().__init__(type, id)
        self._expression = expression

    @property
    def expression(self):
        return self._expression


class ExpressionStatement(Statement):
    def __init__(self, expression):
        self._expression: Expression = expression

    @property
    def expression(self):
        return self._expression


class AssignmentStatement(ExpressionStatement):
    def __init__(self, expression, assign_expression):
        super().__init__(expression)
        self._assign_expression = assign_expression

    @property
    def assign_expression(self):
        return self._assign_expression


class IfStatement(Statement):
    def __init__(self, if_part, else_if_parts=None, else_part=None):
        self._if_part = if_part
        self._else_if_parts = else_if_parts
        self._else_part = else_part


class WhileStatement(Statement):
    def __init__(self, expression, block):
        self._expression = expression
        self._block = block

    @property
    def expression(self):
        return self._expression

    @property
    def block(self):
        return self._block
