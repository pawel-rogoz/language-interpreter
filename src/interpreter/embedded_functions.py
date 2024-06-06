from typing import TYPE_CHECKING

from src.parser.classes.parameter import Parameter, ThisParameter, FunctionParameter
from src.parser.classes.type import BaseType, Type, KeyValueType, ElementType

from src.interpreter.base_function_definition import BaseFunctonDefinition
from src.interpreter.component import Component

if TYPE_CHECKING:
    from src.interpreter.visitor import Visitor


class PrintFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[Parameter(BaseType(Type.STRING), '_print'),]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_print_function(self)


class ValueFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_value_function(self)


class KeyFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_key_function(self)


class KeysFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_keys_function(self)


class ValuesFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_values_function(self)


class AddFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[Parameter(KeyValueType(Type.PAIR, Type.UNKNOWN, Type.UNKNOWN), '_add'),
                                   ThisParameter(KeyValueType(Type.DICT, Type.UNKNOWN, Type.UNKNOWN), '_add_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_add_function(self)


class IsKeyFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[Parameter(BaseType(Type.UNKNOWN), '_is_key'),
                                   ThisParameter(KeyValueType(Type.DICT, Type.UNKNOWN, Type.UNKNOWN), '_is_key_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_is_key_function(self)


class LengthFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[ThisParameter(ElementType(Type.LIST, Type.UNKNOWN), '_length_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_length_function(self)


class PushFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[Parameter(Type.UNKNOWN, '_push'), ThisParameter(ElementType(Type.LIST, Type.UNKNOWN), '_push_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_push_function(self)


class PopFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[ThisParameter(ElementType(Type.LIST, Type.UNKNOWN), '_pop_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_pop_function(self)


class RemoveFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[Parameter(Type.UNKNOWN, '_remove'), ThisParameter(KeyValueType(Type.DICT, Type.UNKNOWN, Type.UNKNOWN), '_remove_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_remove_function(self)


class ForEachFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[FunctionParameter(Type.UNKNOWN, '_for_each'), ThisParameter(KeyValueType(Type.DICT, Type.UNKNOWN, Type.UNKNOWN), '_for_each_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_for_each_function(self)


class WhereFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[FunctionParameter(Type.UNKNOWN, '_where'), ThisParameter(KeyValueType(Type.DICT, Type.UNKNOWN, Type.UNKNOWN), '_where_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_where_function(self)


class SelectFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[FunctionParameter(Type.UNKNOWN, '_select'), ThisParameter(KeyValueType(Type.DICT, Type.UNKNOWN, Type.UNKNOWN), '_select_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_select_function(self)


class OrderByFunctionDefinition(BaseFunctonDefinition, Component):
    def __init__(self, parameters=[FunctionParameter(Type.UNKNOWN, '_orderby'), ThisParameter(KeyValueType(Type.DICT, Type.UNKNOWN, Type.UNKNOWN), '_orderby_this')]):
        super().__init__(parameters)

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_orderby_function(self)
