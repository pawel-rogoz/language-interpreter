from typing import TYPE_CHECKING

from src.parser.classes.expression import Expression

from src.interpreter.component import Component

if TYPE_CHECKING:
    from src.interpreter.visitor import Visitor


class LINQExpression(Expression, Component):
    def __init__(self, from_expression: Expression, where_expression: Expression, orderby_expression: Expression,
                 orderby_sorting: Expression, select_expression: Expression) -> None:
        self._from_expression = from_expression
        self._where_expression = where_expression
        self._orderby_expression = orderby_expression
        self._orderby_sorting = orderby_sorting
        self._select_expression = select_expression

    @property
    def from_expression(self) -> Expression:
        return self._from_expression

    @property
    def where_expression(self) -> Expression:
        return self._where_expression

    @property
    def orderby_expression(self) -> Expression:
        return self._orderby_expression

    @property
    def orderby_sorting(self) -> Expression:
        return self._orderby_sorting

    @property
    def select_expression(self) -> Expression:
        return self._select_expression

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_linq_expression(self)
