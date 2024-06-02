from abc import ABC, abstractmethod

from src.interpreter.interpreter_error import InterpreterError


class PushStack(ABC):
    @abstractmethod
    def push(self, element) -> None:
        pass


class PopStack(ABC):
    @abstractmethod
    def pop(self):
        pass


class FindStack(ABC):
    @abstractmethod
    def find(self, key: str):
        pass


class GlobalStack(PushStack, FindStack):
    def __init__(self) -> None:
        self._function_definitions = {}

    def push(self, element) -> None:
        key = element.key
        if key in self._function_definitions.keys():
            raise InterpreterError()
        self._function_definitions[key] = element

    def find(self, key: str):
        if key in self._function_definitions.keys():
            return self._function_definitions[key]
        return None


class ExecutionStack(PushStack, PopStack):
    def __init__(self) -> None:
        self._function_stacks = []

    def push(self, element: 'FunctionStack') -> None:
        self._function_stacks.append(element)

    def pop(self):
        return self._function_stacks.pop()


class FunctionStack(PushStack, PopStack, FindStack):
    def __init__(self) -> None:
        self._block_stacks: ['BlockStack'] = []

    def push(self, element: 'BlockStack') -> None:
        self._block_stacks.append(element)

    def pop(self) -> 'BlockStack':
        return self._block_stacks.pop()

    def find(self, key: str):
        for stack in self._block_stacks:
            if variable := stack.find(key):
                return variable
        return None


class BlockStack(PushStack, FindStack):
    def __init__(self) -> None:
        self._variables = {}

    def push(self, element) -> None:
        key = element.key
        if key in self._variables.keys():
            raise InterpreterError()
        self._variables[key] = element

    def find(self, key):
        if key in self._variables.keys():
            return self._variables[key]
        return None
