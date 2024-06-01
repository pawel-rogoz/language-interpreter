from src.parser.parser import Parser

from src.interpreter.visitor import Visitor


class Interpreter:
    def __init__(self, parser: Parser, visitor: Visitor):
        self._program = parser.parse_program()
        self._visitor = visitor

    def interpret(self):
        program = self._program
        visitor = self._visitor
        return visitor.visit_program(program)
