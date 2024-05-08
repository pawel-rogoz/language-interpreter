from abc import ABC


class Part(ABC):
    def __init__(self, block):
        self._block = block

    @property
    def block(self):
        return self._block


class ExpressionPart(Part, ABC):
    def __init__(self, block, expression):
        super().__init__(block)
        self._expression = expression

    @property
    def expression(self):
        return self._expression


class IfPart(ExpressionPart):
    pass


class ElseIfPart(ExpressionPart):
    pass


class ElsePart(Part):
    pass
