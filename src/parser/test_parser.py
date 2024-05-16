from src.lexer.lexer import Lexer
from src.scanner.position import Position
from src.scanner.scanner import Scanner
from src.filter.filter import Filter
from src.parser.parser import Parser
from src.parser.classes.statement import *
from src.parser.classes.expression import *
from src.parser.classes.type import *
from src.parser.classes.block import Block
from src.parser.parser_error import *


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

    def test_expression_statement(self):
        program = create_parser("int main() { main()[0]; }").parse_program()
        assert isinstance(program.get_functions()["main"].block.statements[0], ExpressionStatement)

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
        assert isinstance(expression, GreaterExpression)

    def test_literal_expression(self):
        parser = create_parser("190")
        assert parser.parse_literal() == LiteralExpression(Type.INT, 190)

    def test_class_initialization_expression(self):
        parser = create_parser("new Dict<int,int>()")
        assert parser.parse_class_initialization() == ClassInitializationExpression(
            KeyValueType(Type.DICT, Type.INT, Type.INT),
            list()
        )


class TestBaseAndFunctionType:
    def test_int(self):
        parser = create_parser("int")
        assert parser.parse_type() == BaseType(Type.INT)

    def test_string(self):
        parser = create_parser("string")
        assert parser.parse_type() == BaseType(Type.STRING)

    def test_bool(self):
        parser = create_parser("bool")
        assert parser.parse_type() == BaseType(Type.BOOL)

    def test_float(self):
        parser = create_parser("float")
        assert parser.parse_type() == BaseType(Type.FLOAT)


class TestClassType:
    def test_dict_type(self):
        parser = create_parser("Dict<string,int>")
        assert parser.parse_type() == KeyValueType(Type.DICT, Type.STRING, Type.INT)

    def test_dict_not_enough_types_error(self):
        parser = create_parser("Dict<string>")
        with pytest.raises(ClassDeclarationError):
            parser.parse_type()

    def test_pair_type(self):
        parser = create_parser("Pair<string,int>")
        assert parser.parse_type() == KeyValueType(Type.PAIR, Type.STRING, Type.INT)

    def test_pair_not_enough_types_error(self):
        parser = create_parser("Pair<string>")
        with pytest.raises(ClassDeclarationError):
            parser.parse_type()

    def test_list_type(self):
        parser = create_parser("List<string>")
        assert parser.parse_type() == ElementType(Type.LIST, Type.STRING)

    def test_list_too_many_arguments_error(self):
        parser = create_parser("List<string,int>")
        with pytest.raises(ClassDeclarationError):
            parser.parse_type()


class TestParseRelationTerm:
    def test_greater_expression(self):
        parser = create_parser("1 > 0")
        assert isinstance(parser.parse_relation_term(), GreaterExpression)

    def test_greater_equal_expression(self):
        parser = create_parser("1 >= 0")
        assert isinstance(parser.parse_relation_term(), GreaterEqualExpression)

    def test_less_expression(self):
        parser = create_parser("1 < 0")
        assert isinstance(parser.parse_relation_term(), LessExpression)

    def test_less_equal_expression(self):
        parser = create_parser("1 <= 0")
        assert isinstance(parser.parse_relation_term(), LessEqualExpression)

    def test_equal_expression(self):
        parser = create_parser("1 == 0")
        assert isinstance(parser.parse_relation_term(), EqualExpression)

    def test_not_equal_expression(self):
        parser = create_parser("1 != 0")
        assert isinstance(parser.parse_relation_term(), NotEqualExpression)


class TestParseAdditiveTerm:
    def test_add_expression(self):
        parser = create_parser("1 + 1")
        assert isinstance(parser.parse_additive_term(), AdditionExpression)

    def test_subtract_expression(self):
        parser = create_parser("1 - 1")
        assert isinstance(parser.parse_additive_term(), SubtractionExpression)


class TestParseMultiplicativeTerm:
    def test_multiply_expression(self):
        parser = create_parser("1 * 1")
        assert isinstance(parser.parse_multiplicative_term(), MultiplicationExpression)

    def test_divide_expression(self):
        parser = create_parser("1 / 1")
        assert isinstance(parser.parse_multiplicative_term(), DivisionExpression)


# class TestP