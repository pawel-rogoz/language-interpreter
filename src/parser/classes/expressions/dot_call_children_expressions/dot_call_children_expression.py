from src.parser.classes.expressions.expression import Expression
from abc import ABC


class DotCallChildrenExpression(Expression, ABC):
    def __init__(self, id: str):
        self._id = id

    @property
    def id(self):
        return self._id
