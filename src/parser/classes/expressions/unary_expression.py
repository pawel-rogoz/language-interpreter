from src.parser.classes.expressions.expression import Expression


class UnaryExpression(Expression):
    def __init__(self, expression: Expression):
        self._expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression
