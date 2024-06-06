import pytest
from io import StringIO

from src.scanner.position import Position
from src.scanner.scanner import Scanner

from src.lexer.lexer import Lexer

from src.parser.parser_interface import ParserInterface
from src.parser.classes.program import Program
from src.parser.classes.function_definition import FunctionDefinition
from src.parser.classes.block import Block
from src.parser.classes.statement import (ReturnStatement, InitializationStatement, DeclarationStatement, AssignmentStatement,
                                          ExpressionStatement)
from src.parser.classes.expression import (LiteralExpression, ClassInitializationExpression, GreaterExpression,
                                           LessExpression, LessEqualExpression, GreaterEqualExpression, EqualExpression,
                                           NotEqualExpression, MultiplicationExpression, DivisionExpression, AdditionExpression,
                                           SubtractionExpression, NegationExpression, UnarySubtractionExpression, IdExpression,
                                           FunctionCallExpression, DotCallExpression)
from src.parser.parser import Parser
from src.parser.classes.type import Type, BaseType, KeyValueType, ElementType

from src.filter.filter import Filter

from src.interpreter.value import Value
from src.interpreter.interpreter import Interpreter
from src.interpreter.interpreter_error import InterpreterError, ReturnTypeError, MainNotImplementedError, \
    ExpressionTypeError, DivisionError, InitializationError, AssignmentError
from src.interpreter.embedded_functions import KeyFunctionDefinition


class MockedParser(ParserInterface):
    def __init__(self, ast_tree):
        self.ast_tree = ast_tree

    def parse_program(self):
        return self.ast_tree


def create_interpreter(string) -> Interpreter:
    text = StringIO(string)
    scanner = Scanner(text)
    lexer = Lexer(scanner)
    filter = Filter(lexer)
    parser = Parser(filter)
    program = parser.parse_program()
    interpreter = Interpreter(program)
    return interpreter


def create_mocked_interpreter(ast_tree) -> Interpreter:
    parser = MockedParser(ast_tree)
    program = parser.parse_program()
    interpreter = Interpreter(program)
    return interpreter


# Unit Tests
class TestMockedFunctionReturn:
    def test_interpreting_string_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.STRING), [],
                                                       Block([ReturnStatement(LiteralExpression(BaseType(Type.STRING),
                                                                                                "string",
                                                                                                position=Position(1,
                                                                                                                  1)),
                                                                              position=Position(1, 1)
                                                                              ),
                                                              ]),
                                                       Position(1, 1))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.STRING), "string")

    def test_interpreting_int_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block(
                                                           [ReturnStatement(LiteralExpression(BaseType(Type.INT), 1))])
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), 1)

    def test_interpreting_bool_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LiteralExpression(BaseType(Type.BOOL), True))]),
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_interpreting_pair_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', KeyValueType(Type.PAIR, Type.STRING, Type.INT), [],
                                                       Block([ReturnStatement(
                                                           ClassInitializationExpression(
                                                               KeyValueType(Type.PAIR, Type.STRING, Type.INT),
                                                               [LiteralExpression(BaseType(Type.STRING), "a"),
                                                                LiteralExpression(BaseType(Type.INT), 10)]))])
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(KeyValueType(Type.PAIR, Type.STRING, Type.INT), {"a": 10})

    def test_interpreting_dict_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', KeyValueType(Type.DICT, Type.STRING, Type.INT), [],
                                                       Block([ReturnStatement(ClassInitializationExpression(
                                                           KeyValueType(Type.DICT, Type.STRING, Type.INT), [
                                                               ClassInitializationExpression(
                                                                   KeyValueType(Type.PAIR, Type.STRING, Type.INT),
                                                                   [LiteralExpression(BaseType(Type.STRING), "a"),
                                                                    LiteralExpression(BaseType(Type.INT), 10)])]))]),
                                                       Position(1, 1))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(KeyValueType(Type.DICT, Type.STRING, Type.INT), {"a": 10})

    def test_interpreting_list_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', ElementType(Type.LIST, Type.INT), [],
                                                       Block([ReturnStatement(ClassInitializationExpression(
                                                           ElementType(Type.LIST, Type.INT),
                                                           [LiteralExpression(BaseType(Type.INT), 10)]))]),
                                                       Position(1, 1))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(ElementType(Type.LIST, Type.INT), [10])

    def test_interpreting_void_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.VOID), [],
                                                       Block([]),
                                                       Position(1, 1))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.VOID), None)


class TestFunctionReturnErrors:
    def test_interpreting_void_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.VOID), [],
                                                       Block([ReturnStatement(
                                                           LiteralExpression(BaseType(Type.BOOL), True))]),
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ReturnTypeError):
            interpreter.interpret()

    def test_interpreting_int_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([ReturnStatement(
                                                           LiteralExpression(BaseType(Type.BOOL), True))]),
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ReturnTypeError):
            interpreter.interpret()

    def test_interpreting_string_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           LiteralExpression(BaseType(Type.BOOL), True))]),
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ReturnTypeError):
            interpreter.interpret()

    def test_interpreting_bool_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LiteralExpression(BaseType(Type.STRING), "return"))]),
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ReturnTypeError):
            interpreter.interpret()

    def test_interpreting_pair_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', KeyValueType(Type.PAIR, Type.INT, Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           LiteralExpression(BaseType(Type.STRING), "return"))]),
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ReturnTypeError):
            interpreter.interpret()

    def test_interpreting_dict_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', KeyValueType(Type.DICT, Type.INT, Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           LiteralExpression(BaseType(Type.STRING), "return"))]),
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ReturnTypeError):
            interpreter.interpret()

    def test_interpreting_list_function(self):
        ast_tree = Program({'main': FunctionDefinition('main', ElementType(Type.LIST, Type.INT), [],
                                                       Block([ReturnStatement(
                                                           LiteralExpression(BaseType(Type.STRING), "return"))]),
                                                       )})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ReturnTypeError):
            interpreter.interpret()


class TestProgram:
    def test_main_not_implemented_error(self):
        ast_tree = Program({'abc': FunctionDefinition('abc', BaseType(Type.INT), [],
                                                      Block(
                                                          [ReturnStatement(LiteralExpression(BaseType(Type.INT), 1))]),
                                                      )})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(MainNotImplementedError):
            interpreter.interpret()


class TestBlock:
    def test_nothing_in_block(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.VOID), [], Block([]))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.VOID), None)


class TestRelationExpression:
    def test_false_greater_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           GreaterExpression(LiteralExpression(BaseType(Type.INT), 1),
                                                                             LiteralExpression(BaseType(Type.INT), 2)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_true_greater_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           GreaterExpression(LiteralExpression(BaseType(Type.INT), 2),
                                                                             LiteralExpression(BaseType(Type.INT), 1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_greater_expression_with_float_and_int(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           GreaterExpression(LiteralExpression(BaseType(Type.FLOAT), 2.9),
                                                                             LiteralExpression(BaseType(Type.INT), 1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_error_greater_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           GreaterExpression(LiteralExpression(BaseType(Type.INT), 2),
                                                                             LiteralExpression(BaseType(Type.BOOL),
                                                                                               False)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()

    def test_false_less_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LessExpression(LiteralExpression(BaseType(Type.INT), 2),
                                                                          LiteralExpression(BaseType(Type.INT), 1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_true_less_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LessExpression(LiteralExpression(BaseType(Type.INT), 1),
                                                                          LiteralExpression(BaseType(Type.INT), 2)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_less_expression_with_float_and_int(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LessExpression(LiteralExpression(BaseType(Type.FLOAT), 1.5),
                                                                          LiteralExpression(BaseType(Type.INT), 2)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_error_less_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LessExpression(LiteralExpression(BaseType(Type.INT), 1),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()

    def test_false_less_equal_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LessEqualExpression(LiteralExpression(BaseType(Type.INT), 2),
                                                                          LiteralExpression(BaseType(Type.INT), 1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_true_less_equal_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LessEqualExpression(LiteralExpression(BaseType(Type.INT), 1),
                                                                          LiteralExpression(BaseType(Type.INT), 2)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_less_equal_expression_with_float_and_int(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LessEqualExpression(LiteralExpression(BaseType(Type.FLOAT), 1.99),
                                                                          LiteralExpression(BaseType(Type.INT), 2)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_less_equal_expression_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           LessEqualExpression(LiteralExpression(BaseType(Type.FLOAT), 1.99),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()

    def test_false_greater_equal_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           GreaterEqualExpression(LiteralExpression(BaseType(Type.INT), 1),
                                                                          LiteralExpression(BaseType(Type.INT), 2)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_true_greater_equal_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           GreaterEqualExpression(LiteralExpression(BaseType(Type.INT), 2),
                                                                          LiteralExpression(BaseType(Type.INT), 1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_greater_equal_expression_with_float_and_int(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           GreaterEqualExpression(LiteralExpression(BaseType(Type.FLOAT), 1.99),
                                                                          LiteralExpression(BaseType(Type.INT), 2)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_greater_equal_expression_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           GreaterEqualExpression(LiteralExpression(BaseType(Type.FLOAT), 1.99),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()

    def test_false_equal_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           EqualExpression(LiteralExpression(BaseType(Type.INT), 1),
                                                                          LiteralExpression(BaseType(Type.INT), 2)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_true_equal_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           EqualExpression(LiteralExpression(BaseType(Type.INT), 1),
                                                                          LiteralExpression(BaseType(Type.INT), 1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_equal_expression_with_float_and_int(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           EqualExpression(LiteralExpression(BaseType(Type.FLOAT), 1.00),
                                                                          LiteralExpression(BaseType(Type.INT), 1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_equal_expression_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           EqualExpression(LiteralExpression(BaseType(Type.FLOAT), 1.99),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()

    def test_equal_expression_string(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           EqualExpression(LiteralExpression(BaseType(Type.STRING), "A"),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_equal_expression_list(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           EqualExpression(ClassInitializationExpression(ElementType(Type.LIST, Type.INT), [LiteralExpression(BaseType(Type.INT), 1)]),
                                                                          ClassInitializationExpression(ElementType(Type.LIST, Type.INT), [LiteralExpression(BaseType(Type.INT), 1)])))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_equal_expression_pair(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           EqualExpression(ClassInitializationExpression(KeyValueType(Type.PAIR, Type.INT, Type.INT), [LiteralExpression(BaseType(Type.INT), 1), LiteralExpression(BaseType(Type.INT), 1)]),
                                                                          ClassInitializationExpression(KeyValueType(Type.PAIR, Type.INT, Type.INT), [LiteralExpression(BaseType(Type.INT), 1), LiteralExpression(BaseType(Type.INT), 1)])))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_false_not_equal_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           NotEqualExpression(LiteralExpression(BaseType(Type.INT), 1),
                                                                          LiteralExpression(BaseType(Type.INT), 1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_true_not_equal_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           NotEqualExpression(LiteralExpression(BaseType(Type.INT), 1),
                                                                          LiteralExpression(BaseType(Type.INT), 2)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_not_equal_expression_with_float_and_int(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           NotEqualExpression(LiteralExpression(BaseType(Type.FLOAT), 1.00),
                                                                          LiteralExpression(BaseType(Type.INT), 1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_not_equal_expression_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           EqualExpression(LiteralExpression(BaseType(Type.FLOAT), 1.99),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()

    def test_not_equal_expression_string(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           NotEqualExpression(LiteralExpression(BaseType(Type.STRING), "A"),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_not_equal_expression_list(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           NotEqualExpression(ClassInitializationExpression(ElementType(Type.LIST, Type.INT), [LiteralExpression(BaseType(Type.INT), 1)]),
                                                                          ClassInitializationExpression(ElementType(Type.LIST, Type.INT), [LiteralExpression(BaseType(Type.INT), 1)])))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)

    def test_not_equal_expression_pair(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           NotEqualExpression(ClassInitializationExpression(KeyValueType(Type.PAIR, Type.INT, Type.INT), [LiteralExpression(BaseType(Type.INT), 1), LiteralExpression(BaseType(Type.INT), 1)]),
                                                                          ClassInitializationExpression(KeyValueType(Type.PAIR, Type.INT, Type.INT), [LiteralExpression(BaseType(Type.INT), 1), LiteralExpression(BaseType(Type.INT), 1)])))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), False)


class TestMultiplicationExpression:
    def test_multiplication_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([ReturnStatement(
                                                           MultiplicationExpression(LiteralExpression(BaseType(Type.INT),10),
                                                                          LiteralExpression(BaseType(Type.INT), 10)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), 100)

    def test_multiplication_float_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.FLOAT), [],
                                                       Block([ReturnStatement(
                                                           MultiplicationExpression(LiteralExpression(BaseType(Type.INT),10),
                                                                          LiteralExpression(BaseType(Type.FLOAT), 9.3)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.FLOAT), 93)

    def test_multiplication_string_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           MultiplicationExpression(LiteralExpression(BaseType(Type.INT),10),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.STRING), "AAAAAAAAAA")

    def test_multiplication_error_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           MultiplicationExpression(LiteralExpression(BaseType(Type.FLOAT),10.5),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestDivisionExpression:
    def test_division_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.FLOAT), [],
                                                       Block([ReturnStatement(
                                                           DivisionExpression(LiteralExpression(BaseType(Type.INT),10),
                                                                          LiteralExpression(BaseType(Type.INT), 10)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.FLOAT), 1)

    def test_division_by_zero_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           DivisionExpression(LiteralExpression(BaseType(Type.INT),10),
                                                                          LiteralExpression(BaseType(Type.INT), 0)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(DivisionError):
            interpreter.interpret()

    def test_division_error_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           DivisionExpression(LiteralExpression(BaseType(Type.FLOAT),10.5),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestAdditionExpression:
    def test_addition_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([ReturnStatement(
                                                           AdditionExpression(LiteralExpression(BaseType(Type.INT),10),
                                                                          LiteralExpression(BaseType(Type.INT), 10)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), 20)

    def test_addition_float_int(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.FLOAT), [],
                                                       Block([ReturnStatement(
                                                           AdditionExpression(LiteralExpression(BaseType(Type.FLOAT),10.5),
                                                                          LiteralExpression(BaseType(Type.INT), 3)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.FLOAT), 13.5)

    def test_addition_string(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           AdditionExpression(LiteralExpression(BaseType(Type.STRING),"b"),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.STRING), "bA")

    def test_addition_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           AdditionExpression(LiteralExpression(BaseType(Type.INT),1),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestSubtractionExpression:
    def test_subtraction_expression(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([ReturnStatement(
                                                           SubtractionExpression(LiteralExpression(BaseType(Type.INT),10),
                                                                          LiteralExpression(BaseType(Type.INT), 10)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), 0)

    def test_subtraction_float_int(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.FLOAT), [],
                                                       Block([ReturnStatement(
                                                           SubtractionExpression(LiteralExpression(BaseType(Type.FLOAT),10.5),
                                                                          LiteralExpression(BaseType(Type.INT), 3)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.FLOAT), 7.5)

    def test_subtraction_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.STRING), [],
                                                       Block([ReturnStatement(
                                                           SubtractionExpression(LiteralExpression(BaseType(Type.STRING),"b"),
                                                                          LiteralExpression(BaseType(Type.STRING), "A")))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestNegationExpression:
    def test_negation(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           NegationExpression(LiteralExpression(BaseType(Type.BOOL),False)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_negation_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           NegationExpression(LiteralExpression(BaseType(Type.INT),1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestUnarySubtractionExpression:
    def test_unary_subtraction(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([ReturnStatement(
                                                           UnarySubtractionExpression(LiteralExpression(BaseType(Type.INT),1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), -1)

    def test_unary_subtraction_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.BOOL), [],
                                                       Block([ReturnStatement(
                                                           UnarySubtractionExpression(LiteralExpression(BaseType(Type.BOOL),1)))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestInitializationStatement:
    def test_initialization(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([InitializationStatement(BaseType(Type.INT), 'zmienna',
                                                                                      LiteralExpression(BaseType(Type.INT),1)),
                                                              ReturnStatement(IdExpression('zmienna'))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), 1)

    def test_initialization_wrong_type_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([InitializationStatement(BaseType(Type.INT), 'zmienna',
                                                                                      LiteralExpression(BaseType(Type.BOOL),False)),
                                                              ReturnStatement(IdExpression('zmienna'))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(InitializationError):
            interpreter.interpret()


class TestAssignmentStatement:
    def test_assignment(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([DeclarationStatement(BaseType(Type.INT), 'zmienna'),
                                                              AssignmentStatement(IdExpression('zmienna'),
                                                                                  LiteralExpression(BaseType(Type.INT), 1)),
                                                              ReturnStatement(IdExpression('zmienna'))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), 1)

    def test_assignment_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([DeclarationStatement(BaseType(Type.INT), 'wartosc'),
                                                              InitializationStatement(BaseType(Type.INT), 'zmienna', LiteralExpression(BaseType(Type.INT), 1)),
                                                              AssignmentStatement(IdExpression('zmienna'),
                                                                                  IdExpression('wartosc')),
                                                              ReturnStatement(IdExpression('zmienna'))]
                                                       ))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(AssignmentError):
            interpreter.interpret()


class TestValueFunction:
    def test_value(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([InitializationStatement(KeyValueType(Type.PAIR, Type.INT, Type.INT),
                                                                                      'para',
                                                                                      ClassInitializationExpression(KeyValueType(Type.PAIR, Type.INT, Type.INT),
                                                                                                                    [LiteralExpression(BaseType(Type.INT), 1),
                                                                                                                     LiteralExpression(BaseType(Type.INT), 100)])),
                                                             ReturnStatement(DotCallExpression(IdExpression('para'),
                                                                                               FunctionCallExpression('value', [])))]))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), 100)

    def test_value_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([InitializationStatement(BaseType(Type.INT),
                                                                                      'numer',
                                                                                      LiteralExpression(BaseType(Type.INT), 1)),
                                                             ReturnStatement(DotCallExpression(IdExpression('numer'),
                                                                                               FunctionCallExpression('value', [])))]))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestKeyFunction:
    def test_key(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([InitializationStatement(KeyValueType(Type.PAIR, Type.INT, Type.INT),
                                                                                      'para',
                                                                                      ClassInitializationExpression(KeyValueType(Type.PAIR, Type.INT, Type.INT),
                                                                                                                    [LiteralExpression(BaseType(Type.INT), 1),
                                                                                                                     LiteralExpression(BaseType(Type.INT), 100)])),
                                                             ReturnStatement(DotCallExpression(IdExpression('para'),
                                                                                               FunctionCallExpression('key', [])))]))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), 1)

    def test_key_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([InitializationStatement(BaseType(Type.INT),
                                                                                      'numer',
                                                                                      LiteralExpression(BaseType(Type.INT), 1)),
                                                             ReturnStatement(DotCallExpression(IdExpression('numer'),
                                                                                               FunctionCallExpression('key', [])))]))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestKeysFunction:
    def test_key(self):
        ast_tree = Program({'main': FunctionDefinition('main', ElementType(Type.LIST, Type.INT), [],
                                                       Block([InitializationStatement(KeyValueType(Type.DICT, Type.INT, Type.INT),
                                                                                      'slownik',
                                                                                      ClassInitializationExpression(KeyValueType(Type.DICT, Type.INT, Type.INT),
                                                                                                                    [ClassInitializationExpression(KeyValueType(Type.PAIR, Type.INT, Type.INT), [LiteralExpression(BaseType(Type.INT), 1),
                                                                                                                     LiteralExpression(BaseType(Type.INT), 100)])])),
                                                             ReturnStatement(DotCallExpression(IdExpression('slownik'),
                                                                                               FunctionCallExpression('keys', [])))]))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(ElementType(Type.LIST, Type.INT), [1])

    def test_keys_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([InitializationStatement(BaseType(Type.INT),
                                                                                      'numer',
                                                                                      LiteralExpression(BaseType(Type.INT), 1)),
                                                             ReturnStatement(DotCallExpression(IdExpression('numer'),
                                                                                               FunctionCallExpression('keys', [])))]))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestValuesFunction:
    def test_values(self):
        ast_tree = Program({'main': FunctionDefinition('main', ElementType(Type.LIST, Type.INT), [],
                                                       Block([InitializationStatement(KeyValueType(Type.DICT, Type.INT, Type.INT),
                                                                                      'slownik',
                                                                                      ClassInitializationExpression(KeyValueType(Type.DICT, Type.INT, Type.INT),
                                                                                                                    [ClassInitializationExpression(KeyValueType(Type.PAIR, Type.INT, Type.INT), [LiteralExpression(BaseType(Type.INT), 1),
                                                                                                                     LiteralExpression(BaseType(Type.INT), 100)])])),
                                                             ReturnStatement(DotCallExpression(IdExpression('slownik'),
                                                                                               FunctionCallExpression('values', [])))]))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(ElementType(Type.LIST, Type.INT), [100])

    def test_values_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.INT), [],
                                                       Block([InitializationStatement(BaseType(Type.INT),
                                                                                      'numer',
                                                                                      LiteralExpression(BaseType(Type.INT), 1)),
                                                             ReturnStatement(DotCallExpression(IdExpression('numer'),
                                                                                               FunctionCallExpression('values', [])))]))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


class TestPrintFunction:
    def test_print(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.VOID), [],
                                                       Block([ExpressionStatement(FunctionCallExpression('print', [LiteralExpression(BaseType(Type.STRING), "zmienna")])),]))})
        interpreter = create_mocked_interpreter(ast_tree)
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.VOID), None)

    def test_print_error(self):
        ast_tree = Program({'main': FunctionDefinition('main', BaseType(Type.VOID), [],
                                                       Block([ExpressionStatement(FunctionCallExpression('print', [LiteralExpression(BaseType(Type.INT), 1)])),]))})
        interpreter = create_mocked_interpreter(ast_tree)
        with pytest.raises(ExpressionTypeError):
            interpreter.interpret()


# Integration Tests
class TestInterpretingFunction:
    def test_interpreting_void_function(self):
        interpreter = create_interpreter("void main() { 1 > 0; }")
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.VOID), None)

    def test_interpreting_int_function(self):
        interpreter = create_interpreter("int main() { return 1; }")
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.INT), 1)

    def test_interpreting_string_function(self):
        interpreter = create_interpreter("string main() { return \"string\"; }")
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.STRING), "string")

    def test_interpreting_bool_function(self):
        interpreter = create_interpreter("bool main() { return true; }")
        interpreter.interpret()
        assert interpreter.last_result == Value(BaseType(Type.BOOL), True)

    def test_interpreting_pair_function(self):
        interpreter = create_interpreter("Pair<string,int> main() { return new Pair<string,int>(\"a\", 10); }")
        interpreter.interpret()
        assert interpreter.last_result == Value(KeyValueType(Type.PAIR, Type.STRING, Type.INT), {'a': 10})

    def test_interpreting_dict_function(self):
        interpreter = create_interpreter(
            "Dict<string,int> main() { return new Dict<string,int>(new Pair<string,int>(\"a\", 10)); }")
        interpreter.interpret()
        assert interpreter.last_result == Value(KeyValueType(Type.DICT, Type.STRING, Type.INT), {'a': 10})

    def test_interpreting_list_function(self):
        interpreter = create_interpreter("List<int> main() { return new List<int>(1,2,3,4,5); }")
        interpreter.interpret()
        assert interpreter.last_result == Value(ElementType(Type.LIST, Type.INT), [1, 2, 3, 4, 5])
