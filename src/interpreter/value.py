from src.parser.classes.type import BaseType, ElementType, KeyValueType
from src.interpreter.interpreter_error import InterpreterError
from typing import Union
from abc import ABC, abstractmethod


class Value(ABC):
    def __init__(self, type: BaseType):
        self._type = type

    @property
    def type(self):
        return self._type

    @abstractmethod
    def change_value(self, value: 'Value'):
        pass


class BaseValue(Value):
    def __init__(self, type: BaseType, value: Union[str, int, float, bool, list, dict]):
        super().__init__(type)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Value):
        if value.type != self._type:
            raise InterpreterError()
        self._value = value

    def change_value(self, value: Value):
        self.value = value


class ElementValue(Value):
    def __init__(self, type: ElementType, elements_values: [Union[str, int, float, bool, list, dict]]):
        super().__init__(type)
        self._elements_values = elements_values

    @property
    def elements_values(self):
        return self._elements_values

    @elements_values.setter
    def elements_values(self, value: 'ElementValue'):
        if self._type != value.type or len(self._elements_values) != len(value.elements_values):
            raise InterpreterError()
        self._elements_values = value.elements_values

    def swap_value(self, index: int, value: BaseValue):
        if self._type != value.type:
            raise InterpreterError()
        if len(self._elements_values) < index:
            raise InterpreterError()
        self._elements_values[index] = value.value

    def add_value(self, value: BaseValue):
        if self._type != value.type:
            raise InterpreterError()
        self._elements_values.append(value.value)

    def change_value(self, value: Value):
        self._elements_values = value


class KeyValueValue(Value):
    def __init__(self, type: KeyValueType, values: dict):
        super().__init__(type)
        self._values = values

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values: 'KeyValueValue'):
        if self._type != values.type:
            raise InterpreterError()
        self._values = values

    def change_value(self, value: Value):
        self._values = value


