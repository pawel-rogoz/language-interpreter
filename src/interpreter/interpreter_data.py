from src.interpreter.stack import GlobalStack, ExecutionStack


class InterpreterData:
    def __init__(self, global_stack: GlobalStack, execution_stack: ExecutionStack):
        self._global_stack = global_stack
        self._execution_stack = execution_stack

    @property
    def global_stack(self) -> GlobalStack:
        return self._global_stack

    @property
    def execution_stack(self) -> ExecutionStack:
        return self._execution_stack
