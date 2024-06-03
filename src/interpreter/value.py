from src.parser.classes.type import BaseType, ElementType, KeyValueType, Type
from src.interpreter.interpreter_error import InterpreterError
from typing import Union
from abc import ABC, abstractmethod


class Value(ABC):
    def __init__(self, type: Union[BaseType, KeyValueType, ElementType], value):
        self._type = type
        self._value = value

    def __eq__(self, other):
        return self._value == other.value and self._type == other.type

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    def change_value(self, value: 'Value'):
        if value.type == self.type:
            self._value = value.value
        else:
            raise InterpreterError(message=f"Can't assign value: {value.value} to object type {self._type}")


class BaseValue(Value):
    pass


class ElementValue(Value):
    def __init__(self, type, value: list):
        super().__init__(type, value)

    def change_value(self, index: int, value: Value):
        if self._type != value.type:
            raise InterpreterError()
        if len(self._value) < index:
            raise InterpreterError()
        self._value[index] = value.value

    def add_value(self, value: Value):
        if self._type != value.type:
            raise InterpreterError()
        self._value.append(value.value)

    def get_value(self, index: int) -> Value:
        if index > len(self._value):
            raise InterpreterError(f"Cannot get a value from index {index} - object size is: {len(self._value)}")
        return self._value[index]


class KeyValueValue(Value):
    def __init__(self, type: KeyValueType, value: dict):
        super().__init__(type, value)

    def change_value(self, key: Value, value: Value):
        if self._type != value.type:
            raise InterpreterError()
        if key.value in self._value.keys():
            self._value[key.value] = value.value
        raise InterpreterError()

    def add_value(self, key: Value, value: Value):
        if self._type.key_type != key.type or self._type.value_type != value.type:
            raise InterpreterError()
        if key.value in self._value.keys():
            raise InterpreterError()
        self._value[key.value] = value.value

    def get_value(self, key) -> Value:
        if key not in self._value.keys():
            raise InterpreterError(f"There is no element with key: {key}")
        return self._value[key]