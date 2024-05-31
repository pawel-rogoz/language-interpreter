from src.parser.parser import Parser
from src.interpreter.interpreter_error import InterpreterError
from src.interpreter.scope import *


class Interpreter:
    def __init__(self, parser: Parser):
        self._program = parser.parse_program()

    def interpret(self):
        program = self._program
        functions = program.get_functions()
        if "main" not in functions.keys():
            raise InterpreterError(message="There is no function in given input")
        scope = Scope(global_scope=GlobalScope(functions), local_scope=None)
        return program.visit(scope)
