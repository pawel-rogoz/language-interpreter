from src.parser.classes.expression import Expression


class LINQExpression(Expression):
    def __init__(self,from_expression,where_expression,orderby_expression,orderby_sorting,select_expression):
        self._from_expression = from_expression
        self._where_expression = where_expression
        self._orderby_expression = orderby_expression
        self._orderby_sorting = orderby_sorting
        self._select_expression = select_expression

    @property
    def from_expression(self):
        return self._from_expression

    @property
    def where_expression(self):
        return self._where_expression

    @property
    def orderby_expression(self):
        return self._orderby_expression

    @property
    def orderby_sorting(self):
        return self._orderby_sorting

    @property
    def select_expression(self):
        return self._select_expression
