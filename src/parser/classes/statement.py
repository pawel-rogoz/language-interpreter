from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.interpreter.component import Component

if TYPE_CHECKING:
    from src.interpreter.visitor import Visitor
    from src.parser.classes.expression import Expression
    from src.parser.classes.type import BaseType
    from src.parser.classes.block import Block
    from src.parser.classes.if_parts import IfPart, ElseIfPart, ElsePart


class Statement(ABC):
    @abstractmethod
    def __init__(self):
        pass


class ReturnStatement(Statement, Component):
    def __init__(self, expression: 'Expression') -> None:
        self._expression = expression

    @property
    def expression(self) -> 'Expression':
        return self._expression

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_return_statement(self)


class DeclarationStatement(Statement, Component):
    def __init__(self, type: 'BaseType', id: str) -> None:
        self._type = type
        self._id = id

    @property
    def type(self) -> 'BaseType':
        return self._type

    @property
    def id(self) -> str:
        return self._id

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_declaration_statement(self)


class InitializationStatement(DeclarationStatement, Component):
    def __init__(self, type: 'BaseType', id: str, expression: 'Expression'):
        super().__init__(type, id)
        self._expression = expression

    @property
    def expression(self) -> 'Expression':
        return self._expression

    def accept(self, visitor: 'Visitor'):
        visitor.visit_initialization_statement(self)


class ExpressionStatement(Statement, Component):
    def __init__(self, expression: 'Expression'):
        self._expression = expression

    @property
    def expression(self) -> 'Expression':
        return self._expression

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_expression_statement(self)


class AssignmentStatement(ExpressionStatement, Component):
    def __init__(self, expression: 'Expression', assign_expression: 'Expression'):
        super().__init__(expression)
        self._assign_expression = assign_expression

    @property
    def assign_expression(self) -> 'Expression':
        return self._assign_expression

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_assignment_statement(self)


class IfStatement(Statement, Component):
    def __init__(self, if_part: 'IfPart', else_if_parts: ['ElseIfPart'] = None, else_part: 'ElsePart' = None) -> None:
        self._if_part = if_part
        self._else_if_parts = else_if_parts
        self._else_part = else_part

    @property
    def if_part(self) -> 'IfPart':
        return self._if_part

    @property
    def else_if_parts(self) -> ['ElseIfPart']:
        return self._else_if_parts

    @property
    def else_part(self) -> 'ElsePart':
        return self._else_part

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_if_statement(self)


class WhileStatement(Statement, Component):
    def __init__(self, expression: 'Expression', block: 'Block'):
        self._expression = expression
        self._block = block

    @property
    def expression(self) -> 'Expression':
        return self._expression

    @property
    def block(self) -> 'Block':
        return self._block

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_while_statement(self)
