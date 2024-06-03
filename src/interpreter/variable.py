from src.interpreter.interpreter_error import InterpreterError
from src.interpreter.value import BaseValue, Value
from src.parser.classes.type import BaseType


class Variable:
    def __init__(self, type: BaseType, id: str, value: Value | None):
        self._type = type
        self._id = id
        if value.type != self._type:
            raise InterpreterError(message=f"Can't assign value type: {value.type} to variable type: {self._type}")
        self._value = value

    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Value):
        if self._type != value.type:
            raise InterpreterError()
        if self._value is None:
            self._value = value
        self._value.change_value(value)
