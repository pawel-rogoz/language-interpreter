from src.parser.classes.expressions.unary_expression import UnaryExpression


class IndexingExpression(UnaryExpression):
    def __init__(self, expression, index=None):
        super().__init__(expression)
        self._index = index

    @property
    def index(self):
        return self._index
