from typing import Optional

from src.interpreter.interpreter_error import InterpreterError

from src.interpreter.variable import Variable


class BlockVariables:
    def __init__(self) -> None:
        self._variables = {}

    def add_variable(self, element: Variable) -> None:
        key = element.id
        if key in self._variables.keys():
            raise InterpreterError("There is already declared variable with this id")
        self._variables[key] = element

    def find_variable(self, key: str) -> Optional[Variable]:
        if key in self._variables.keys():
            return self._variables[key]
        return None


class FunctionContext:
    def __init__(self) -> None:
        self._block_variables: [BlockVariables] = []
        self._current_block_variable: Optional[BlockVariables] = None

    def add_variable(self, variable: Variable):
        if not self._current_block_variable:
            raise InterpreterError("Can't push an item to an empty stack")
        for block in self._block_variables:
            if block.find_variable(variable):
                raise InterpreterError(message=f"There is already a variable {variable.id} declared")
        self._current_block_variable.add_variable(variable)

    def push_block_variables(self, block_variables: BlockVariables) -> None:
        self._block_variables.append(block_variables)
        self._current_block_variable = block_variables

    def pop_block_variables(self) -> BlockVariables:
        result = self._block_variables.pop()
        self._current_block_variable = self._block_variables[-1] if len(self._block_variables) > 0 else None
        return result

    def find_variable(self, key: str) -> Optional[Variable]:
        for block_variable in self._block_variables:
            if variable := block_variable.find_variable(key):
                return variable
        return None


class ExecutionStack:
    def __init__(self) -> None:
        self._function_contexts: [FunctionContext] = []
        self._current_context: Optional[FunctionContext] = None

    @property
    def function_stacks(self) -> [FunctionContext]:
        return self._function_contexts

    @property
    def current_context(self) -> FunctionContext:
        return self._current_context

    def add_variable(self, variable: Variable) -> None:
        if self._current_context:
            self._current_context.add_variable(variable)
        else:
            raise InterpreterError("Can't push item to empty stack")

    def push_block_variables(self, block_variables: BlockVariables) -> None:
        if self._current_context:
            self._current_context.push_block_variables(block_variables)
        else:
            raise InterpreterError("Can't push block variables to empty stack")

    def pop_block_variables(self) -> None:
        if self._current_context:
            self._current_context.pop_block_variables()
        else:
            raise InterpreterError("Can't push an item to an empty stack")

    def push_function_context(self, element: FunctionContext) -> None:
        self._function_contexts.append(element)
        self._current_context = element

    def pop_function_context(self) -> FunctionContext:
        result = self._function_contexts.pop()
        self._current_context = self._function_contexts[-1] if len(self._function_contexts) > 0 else None
        return result

    def find_variable(self, key: str) -> Optional[Variable]:
        return self._current_context.find_variable(key)
