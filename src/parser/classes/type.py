from enum import Enum, auto
from typing import Union


class BaseType:
    def __init__(self, type):
        self._type: Type = type

    def __eq__(self, other):
        return self.type == other.type

    def __str__(self):
        return f"{self.type}"

    def __hash__(self):
        return hash(self._type)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type: 'Type'):
        if self._type == Type.UNKNOWN:
            self._type = type


class FunctionType(BaseType):
    pass


class KeyValueType(BaseType):
    def __init__(self, type: 'Type', key_type : 'Type', value_type: Union['Type','BaseType']):
        super().__init__(type)
        self._key_type: Type = key_type
        self._value_type: Type = value_type

    def __eq__(self, other):
        return self.type == other.type and self.key_type == other.key_type and self.value_type == other.value_type

    def __str__(self):
        return f"{self._type} [ {self._key_type} : {self._value_type} ]"

    def __hash__(self):
        return hash((self._type, self._key_type, self._value_type))

    @property
    def key_type(self) -> 'Type':
        return self._key_type

    @key_type.setter
    def key_type(self, type: 'Type'):
        if self._key_type == Type.UNKNOWN:
            self._key_type = type

    @property
    def value_type(self):
        return self._value_type

    @value_type.setter
    def value_type(self, type: 'Type'):
        if self._value_type == Type.UNKNOWN:
            self._value_type = type


class ElementType(BaseType):
    def __init__(self, type, element_type):
        super().__init__(type)
        self._element_type: Type = element_type

    def __eq__(self, other):
        return self.type == other.type and self.element_type == other.element_type

    def __str__(self):
        return f"{self._type} [{self._element_type}]"

    def __hash__(self):
        return hash((self._type, self._element_type))

    @property
    def element_type(self):
        return self._element_type

    @element_type.setter
    def element_type(self, type: Union['Type', 'BaseType']):
        if self._element_type == Type.UNKNOWN:
            self._element_type = type


class Type(Enum):
    VOID = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    PAIR = auto()
    LIST = auto()
    DICT = auto()
    UNKNOWN = auto()


