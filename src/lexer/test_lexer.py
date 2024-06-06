from src.lexer.lexer import Lexer
from src.lexer.lexer_error import *
from src.scanner.position import Position
from src.scanner.scanner import Scanner
from src.tokens.token_type import TokenType

from io import StringIO
import pytest


class TestInit:
    def test_scanner_init_value(self):
        text = StringIO("")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.get_scanner() == scanner

    def test_position_init_value(self):
        text = StringIO("")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.get_position() == Position(1, 1)


class TestKeywordsTokens:
    def test_token_eof(self):
        text = StringIO("")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.EOF

    def test_token_if(self):
        text = StringIO("if")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.IF

    def test_token_else(self):
        text = StringIO("else")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.ELSE

    def test_token_while(self):
        text = StringIO("while")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.WHILE

    def test_token_return(self):
        text = StringIO("return")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.RETURN

    def test_token_new(self):
        text = StringIO("new")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.NEW

    def test_token_select(self):
        text = StringIO("select")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.SELECT

    def test_token_from(self):
        text = StringIO("from")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.FROM

    def test_token_where(self):
        text = StringIO("where")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.WHERE

    def test_token_orderby(self):
        text = StringIO("orderby")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.ORDER_BY

    def test_token_asc(self):
        text = StringIO("asc")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.ASC

    def test_token_desc(self):
        text = StringIO("desc")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.DESC

    def test_token_int(self):
        text = StringIO("int")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.INT

    def test_token_float(self):
        text = StringIO("float")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.FLOAT

    def test_token_string(self):
        text = StringIO("string")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.STRING

    def test_token_pair(self):
        text = StringIO("Pair")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.PAIR

    def test_token_list(self):
        text = StringIO("List")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.LIST

    def test_token_dict(self):
        text = StringIO("Dict")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.DICT

    def test_token_id(self):
        text = StringIO("identifier")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.ID


class TestSingleOperatorsTokens:
    def test_round_open(self):
        text = StringIO("(")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.ROUND_OPEN

    def test_round_close(self):
        text = StringIO(")")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.ROUND_CLOSE

    def test_square_open(self):
        text = StringIO("[")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.SQUARE_OPEN

    def test_square_close(self):
        text = StringIO("]")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.SQUARE_CLOSE

    def test_curly_open(self):
        text = StringIO("{")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.CURLY_OPEN

    def test_curly_close(self):
        text = StringIO("}")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.CURLY_CLOSE

    def test_dot(self):
        text = StringIO(".")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.DOT

    def test_comma(self):
        text = StringIO(",")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.COMMA

    def test_semicolon(self):
        text = StringIO(";")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.SEMICOLON

    def test_plus(self):
        text = StringIO("+")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.PLUS

    def test_minus(self):
        text = StringIO("-")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.MINUS

    def test_multiply(self):
        text = StringIO("*")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.MULTIPLY


class TestInt:
    def test_int_token(self):
        text = StringIO("999")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.INT_VALUE

    def test_int_value(self):
        text = StringIO("999")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().value == 999

    def test_int_too_big_error(self):
        number = '9' * 100
        text = StringIO(number)
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(LexerError):
            lexer.try_build_token()


class TestFloat:
    def test_float_token(self):
        text = StringIO("9.99")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.FLOAT_VALUE

    def test_float_value(self):
        text = StringIO("9.99")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().value == 9.99

    def test_float_too_long(self):
        number = "0." + "9" * 100
        text = StringIO(number)
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(LexerError):
            lexer.try_build_token()

    def test_no_number_after_dot_error(self):
        number = "0."
        text = StringIO(number)
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(FloatError) as error:
            lexer.try_build_token()
        assert error.value.position == Position(1,3)


class TestString:
    def test_string_token(self):
        text = StringIO("\"string\"")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.STRING_VALUE

    def test_string_value(self):
        text = StringIO("\"string\"")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().value == "string"

    def test_no_closing_error(self):
        text = StringIO("\"string")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(LexerError):
            lexer.try_build_token()

    def test_no_closing_error_position_just_quotation(self):
        text = StringIO("\"")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(LexerError) as error:
            lexer.try_build_token()
        assert error.value.position == Position(1, 2)

    def test_no_closing_error_position_with_chars(self):
        text = StringIO("\"aaa")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(LexerError) as error:
            lexer.try_build_token()
        assert error.value.position == Position(1, 5)

    def test_too_long_error(self):
        string = 'a'*300
        text = StringIO(string)
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(LexerError):
            lexer.try_build_token()

    def test_string_with_escape_character(self):
        text = StringIO("\"Escape: \\n \\t \\r \\b \\f \\' \\\"\"")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().value == "Escape: \n \t \r \b \f \' \""


class TestDoubleOperators:
    def test_build_and(self):
        text = StringIO("&&")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.AND

    def test_build_or(self):
        text = StringIO("||")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.OR

    def test_build_multiple_or(self):
        text = StringIO("|| || ||")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        token_types = list()
        while (token := lexer.try_build_token()).type != TokenType.EOF:
            token_types.append(token.type)
        assert token_types == [TokenType.OR]*3

    def test_and_or_error(self):
        text = StringIO("&|")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(LexerError):
            lexer.try_build_token()

    def test_single_and_error(self):
        text = StringIO("&")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(LexerError):
            lexer.try_build_token()

    def test_single_or_error(self):
        text = StringIO("|")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        with pytest.raises(LexerError):
            lexer.try_build_token()


class TestSingleOrDoubleOperators:
    def test_build_negate(self):
        text = StringIO("!")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.NEGATE

    def test_build_not_equal(self):
        text = StringIO("!=")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.NOT_EQUAL

    def test_build_less(self):
        text = StringIO("<")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.LESS

    def test_build_less_or_not_equal(self):
        text = StringIO("<=")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.LESS_EQUAL

    def test_build_greater(self):
        text = StringIO(">")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.GREATER

    def test_build_greater_or_equal(self):
        text = StringIO(">=")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.GREATER_EQUAL

    def test_build_assign(self):
        text = StringIO("=")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.ASSIGN

    def test_build_equal(self):
        text = StringIO("==")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().type == TokenType.EQUAL


class TestMultipleTokens:
    # def test_no_token(self):
    #     text = StringIO("l9")
    #     scanner = Scanner(text)
    #     lexer = Lexer(scanner)
    #     assert lexer.try_build_token().value == "l"
    #     with pytest.raises(LexerError):
    #       lexer.try_build_token()

    def test_int_assignment(self):
        text = StringIO("int number = 1;")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT, TokenType.ID, TokenType.ASSIGN, TokenType.INT_VALUE, TokenType.SEMICOLON, TokenType.EOF]

    def test_skip_whitespaces_and_int_assignment(self):
        text = StringIO("                 int number = 1;")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT, TokenType.ID, TokenType.ASSIGN, TokenType.INT_VALUE, TokenType.SEMICOLON, TokenType.EOF]

    def test_skip_comment_and_build_tokens(self):
        text = StringIO("//comment\nint number = 1;")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.COMMENT, TokenType.INT, TokenType.ID, TokenType.ASSIGN, TokenType.INT_VALUE, TokenType.SEMICOLON, TokenType.EOF]

    def test_skip_comment(self):
        text = StringIO("//comment\n//comment\n//comment")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.COMMENT, TokenType.COMMENT, TokenType.COMMENT, TokenType.EOF]

    def test_string_assignment(self):
        text = StringIO("string a = \"string\";")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.STRING, TokenType.ID, TokenType.ASSIGN, TokenType.STRING_VALUE, TokenType.SEMICOLON, TokenType.EOF]

    def test_no_spaces(self):
        text = StringIO("int a=1;\n")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT, TokenType.ID, TokenType.ASSIGN, TokenType.INT_VALUE, TokenType.SEMICOLON, TokenType.EOF]

    def test_greater_equal_expression(self):
        text = StringIO("1 >= 0")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT_VALUE, TokenType.GREATER_EQUAL, TokenType.INT_VALUE, TokenType.EOF]

    def test_less_equal_expression(self):
        text = StringIO("1 <= 0")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT_VALUE, TokenType.LESS_EQUAL, TokenType.INT_VALUE, TokenType.EOF]

    def test_less_expression(self):
        text = StringIO("1 < 0")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT_VALUE, TokenType.LESS, TokenType.INT_VALUE, TokenType.EOF]

    def test_greater_expression(self):
        text = StringIO("1 > 0")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT_VALUE, TokenType.GREATER, TokenType.INT_VALUE, TokenType.EOF]

    def test_equal_expression(self):
        text = StringIO("1 == 0")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT_VALUE, TokenType.EQUAL, TokenType.INT_VALUE, TokenType.EOF]

    def test_not_equal_expression(self):
        text = StringIO("1 != 0")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT_VALUE, TokenType.NOT_EQUAL, TokenType.INT_VALUE, TokenType.EOF]

    def test_equal_strings(self):
        text = StringIO("\"abc\" != \"xyz\"")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.STRING_VALUE, TokenType.NOT_EQUAL, TokenType.STRING_VALUE, TokenType.EOF]

    def test_undefined_token_after_id_error(self):
        text = StringIO("a9?")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        lexer.try_build_token()
        with pytest.raises(LexerError):
            lexer.try_build_token()

    def test_work_with_file(self):
        file = open("main.pr", "r", encoding="utf-8")
        scanner = Scanner(file)
        lexer = Lexer(scanner)
        tokens_types = []
        for token in lexer.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT,
                                TokenType.ID,
                                TokenType.ROUND_OPEN,
                                TokenType.ROUND_CLOSE,
                                TokenType.CURLY_OPEN,
                                TokenType.STRING,
                                TokenType.ID,
                                TokenType.ASSIGN,
                                TokenType.STRING_VALUE,
                                TokenType.SEMICOLON,
                                TokenType.LIST,
                                TokenType.LESS,
                                TokenType.INT,
                                TokenType.GREATER,
                                TokenType.ID,
                                TokenType.ASSIGN,
                                TokenType.NEW,
                                TokenType.LIST,
                                TokenType.ROUND_OPEN,
                                TokenType.INT_VALUE,
                                TokenType.COMMA,
                                TokenType.INT_VALUE,
                                TokenType.COMMA,
                                TokenType.INT_VALUE,
                                TokenType.ROUND_CLOSE,
                                TokenType.SEMICOLON,
                                TokenType.INT,
                                TokenType.ID,
                                TokenType.ASSIGN,
                                TokenType.ID,
                                TokenType.SQUARE_OPEN,
                                TokenType.INT_VALUE,
                                TokenType.SQUARE_CLOSE,
                                TokenType.SEMICOLON,
                                TokenType.CURLY_CLOSE,
                                TokenType.EOF]


class TestPosition:
    def test_position_with_newlines(self):
        text = StringIO("a\nb\nc")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_position = list()
        for token in lexer.generate_tokens():
            tokens_position.append(token.position)
        assert tokens_position == [Position(1, 1), Position(2, 1), Position(3, 1), Position(3, 2)]

    def test_position_multiple_tokens_in_one_line(self):
        text = StringIO("a b c")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_position = list()
        for token in lexer.generate_tokens():
            tokens_position.append(token.position)
        assert tokens_position == [Position(1, 1), Position(1, 3), Position(1, 5), Position(1, 6)]

    def test_position_just_eof(self):
        text = StringIO("")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().position == Position(1, 1)

    def test_position_of_integer(self):
        text = StringIO("999")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().position == Position(1, 1)

    def test_position_of_string(self):
        text = StringIO("\"abc\"")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().position == Position(1, 1)

    def test_position_of_bool(self):
        text = StringIO("true")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        assert lexer.try_build_token().position == Position(1, 1)

    def test_position_of_operation(self):
        text = StringIO("a + b")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_position = list()
        for token in lexer.generate_tokens():
            tokens_position.append(token.position)
        assert tokens_position == [Position(1, 1), Position(1, 3), Position(1, 5), Position(1, 6)]

    def test_position_of_operation_without_spaces(self):
        text = StringIO("a+b")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        tokens_position = list()
        for token in lexer.generate_tokens():
            tokens_position.append(token.position)
        assert tokens_position == [Position(1, 1), Position(1, 2), Position(1, 3), Position(1, 4)]
