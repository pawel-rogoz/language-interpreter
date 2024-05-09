from src.parser.classes.function_definition import FunctionDefinition

class Program:
    def __init__(self, functions: dict):
        self._functions = functions

    def get_functions(self) -> dict[str, FunctionDefinition]:
        return self._functions
