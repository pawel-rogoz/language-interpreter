from src.parser.classes.expressions.dot_call_children_expressions.dot_call_children_expression \
    import DotCallChildrenExpression
from src.parser.classes.expressions.call_expression.call_expression import CallExpression


class MethodCallExpression(DotCallChildrenExpression):
    def __init__(self, id: str, call: CallExpression):
        super().__init__(id)
        self._call = call

    @property
    def call(self):
        return self._call
