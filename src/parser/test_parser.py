from src.lexer.lexer import Lexer
from src.scanner.position import Position
from src.scanner.scanner import Scanner
from src.filter.filter import Filter
from src.parser.parser import Parser
from src.parser.classes.statement import *
from src.parser.classes.expression import *
from src.parser.classes.type import *
from src.parser.classes.block import Block

from io import StringIO, TextIOBase
import pytest


def create_parser(string) -> Parser:
    text = StringIO(string)
    scanner = Scanner(text)
    lexer = Lexer(scanner)
    filter = Filter(lexer)
    return Parser(filter)


class TestPosition:
    program = create_parser("int main() {}").parse_program()

    def test_single_function_position(self):
        assert self.program.get_functions()["main"].position == Position(1, 1)

    def test_multiple_functions_positions_with_newline(self):
        program = create_parser("int main() {}\nint abc() {}").parse_program()
        assert program.get_functions()["main"].position == Position(1, 1)
        assert program.get_functions()["abc"].position == Position(2, 1)

    def test_multiple_functions_positions_without_newline(self):
        program = create_parser("int main() {} int abc() {}").parse_program()
        assert program.get_functions()["main"].position == Position(1, 1)
        assert program.get_functions()["abc"].position == Position(1, 15)


class TestFunctionDefinition:
    program = create_parser("int main() {}").parse_program()

    def test_function_name(self):
        assert self.program.get_functions()["main"].name == "main"

    def test_function_type(self):
        assert self.program.get_functions()["main"].type == FunctionType(Type.INT)

    def test_function_parameters(self):
        assert self.program.get_functions()["main"].parameters == list()

    def test_function_block(self):
        assert self.program.get_functions()["main"].block == Block()

    def test_function_position(self):
        assert self.program.get_functions()["main"].position == Position(1, 1)


class TestStatement:
    def test_return_statement(self):
        program = create_parser("int main() { return 0; }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], ReturnStatement)

    def test_if_statement(self):
        program = create_parser("int main() { if (1 > 0) { return 0; } }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], IfStatement)

    def test_if_statement_with_else_if(self):
        program = create_parser("int main() { if (1 > 0) { return 0; } else if (1 < 2) { return 1; } }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], IfStatement)

    def test_if_statement_with_else_if_and_else(self):
        program = create_parser("int main() { if (1 > 0) { return 0; } else if (1 < 2) { return 1; } else { return -1; } }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], IfStatement)

    def test_id_or_call_statement(self):
        program = create_parser("int main() { main()[0]; }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], IdOrCallStatement)

    def test_declaration_statement(self):
        program = create_parser("int main() { int a; }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], DeclarationStatement)

    def test_initialization_statement(self):
        program = create_parser("int main() { int a = 1; }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], InitializationStatement)

    def test_while_statement(self):
        program = create_parser("int main() { while (1 > 0) { a = 1; } }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], WhileStatement)

    def test_assignment_statement(self):
        program = create_parser("int main() { a = 1; }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], AssignmentStatement)


class TestExpression:
    def test_relation_expression(self):
        program = create_parser("int main() { bool a = 1 > 0; }").parse_program()
        expression = program.get_functions()["main"].block.statements[0].expression
        assert isinstance(expression, OrExpression)

