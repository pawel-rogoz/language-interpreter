from abc import ABC, abstractmethod
from enum import Enum, auto


class BaseType:
    def __init__(self, type):
        self._type: Type = type

    @property
    def type(self):
        return self._type


class FunctionType(BaseType):
    pass


class KeyValueType(BaseType):
    def __init__(self, type, key_type, value_type):
        super().__init__(type)
        self._key_type: Type = key_type
        self._value_type: Type = value_type

    @property
    def key_type(self):
        return self._key_type

    @property
    def value_type(self):
        return self._value_type


class ElementType(BaseType):
    def __init__(self, type, element_type):
        super().__init__(type)
        self._value_type: Type = element_type

    @property
    def value_type(self):
        return self._value_type


class Type(Enum):
    VOID = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    PAIR = auto()
    LIST = auto()
    DICT = auto()
