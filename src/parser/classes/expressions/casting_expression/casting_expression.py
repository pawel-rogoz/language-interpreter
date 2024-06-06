from src.parser.classes.expressions.unary_expression import UnaryExpression


class CastingExpression(UnaryExpression):
    def __init__(self, expression, type=None):
        super().__init__(expression)
        self._type = type

    @property
    def type(self):
        return self._type
