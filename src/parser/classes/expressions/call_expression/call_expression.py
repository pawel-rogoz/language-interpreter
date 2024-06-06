from src.parser.classes.expressions.expression import Expression


class CallExpression(Expression):
    def __init__(self, arguments):
        self._arguments = arguments

    @property
    def arguments(self):
        return self._arguments
