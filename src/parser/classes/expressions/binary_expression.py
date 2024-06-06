from src.parser.classes.expressions.expression import Expression


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
