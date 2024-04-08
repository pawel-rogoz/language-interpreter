# from typing import Union
import math
from io import StringIO, TextIOBase
from typing import Optional

from src.scanner.position import Position
from src.scanner.scanner import Scanner
from src.tokens.token_type import TokenType
from src.tokens.token import Token
from src.lexer.lexer_error import LexerError

MAX_STRING = 256
MAX_DIGIT = 10


class Lexer:
    def __init__(self, scanner: Scanner) -> None:
        self._position = Position(1, 0)
        self._scanner = scanner

    single_operators = {
        "(": TokenType.ROUND_OPEN,
        ")": TokenType.ROUND_CLOSE,
        "[": TokenType.SQUARE_OPEN,
        "]": TokenType.SQUARE_CLOSE,
        "{": TokenType.CURLY_OPEN,
        "}": TokenType.CURLY_CLOSE,
        ".": TokenType.DOT,
        ",": TokenType.COMMA,
        ";": TokenType.SEMICOLON,
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.MULTIPLY
    }

    double_operators = {
        "&": TokenType.AND,
        "|": TokenType.OR
    }

    conflict_operators = {
        "single": {
            "<": TokenType.LESS,
            ">": TokenType.GREATER,
            "=": TokenType.ASSIGN,
            "!": TokenType.NEGATE
        },
        "double": {
            "<=": TokenType.LESS_EQUAL,
            ">=": TokenType.GREATER_EQUAL,
            "==": TokenType.EQUAL,
            "!=": TokenType.NOT_EQUAL
        }
    }

    keywords = {
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "return": TokenType.RETURN,
        "new": TokenType.NEW,
        "select": TokenType.SELECT,
        "from": TokenType.FROM,
        "where": TokenType.WHERE,
        "orderby": TokenType.ORDER_BY,
        "asc": TokenType.ASC,
        "desc": TokenType.DESC,
        "true": TokenType.BOOL_VALUE,
        "false": TokenType.BOOL_VALUE,
        "int": TokenType.INT,
        "float": TokenType.FLOAT,
        "string": TokenType.STRING,
        "Pair": TokenType.PAIR,
        "List": TokenType.LIST,
        "Dict": TokenType.DICT
    }

    def get_scanner(self):
        return self._scanner

    def get_position(self):
        return self._position

    def _get_char(self):
        return self._scanner.get_char()
    
    def _next_char(self):
        self._scanner.next_char()
        self._position = self._scanner.current_position

    def _skip_whitespaces(self):
        while self._get_char().isspace():
            self._next_char()

    def try_build_token(self):
        self._skip_whitespaces()

        token = self._try_build_divide_or_comment() \
            or self._try_build_eof() \
            or self._try_build_number() \
            or self._try_build_string() \
            or self._try_build_keyword_or_type_or_id() \
            or self._try_build_single_operator() \
            or self._try_build_operator()
        
        if token:
            return token
        
        raise LexerError("Cannot create token", self._position)

    def _try_build_eof(self):
        if self._get_char() == 'EOF':
            return Token(TokenType.EOF, self._position)
        return None
    
    def _try_build_number(self):
        if not self._scanner.get_char().isdigit():
            return None
        
        integer = self._try_build_integer()

        if self._get_char() == ".":
            return self._try_build_float(integer)
        return Token(TokenType.INT_VALUE, self._position, integer)

    def _try_build_float(self, integer):
        prev_position = self._position
        self._next_char()
        if not self._get_char().isdigit():
            raise LexerError("can't create float without any number after \".\"", prev_position)

        float_part = self._try_build_integer()
        num_digits = int(math.log10(float_part)) + 1
        number = float(integer) + float_part * 10 ** -num_digits

        return Token(TokenType.FLOAT_VALUE, self._position, number)

    def _try_build_integer(self):
        char = self._scanner.get_char()

        power = 0
        number = 0
        i = 0

        while char.isdigit():
            if i == MAX_DIGIT:
                raise LexerError("int too big (max 999999999)", self._position)
            number = number * 10 + int(char)
            power += 1
            i += 1
            self._next_char()
            char = self._get_char()
        
        return number

    def _try_build_string(self):
        char = self._scanner.get_char()

        if char != "\"":
            return None

        self._next_char()
        char = self._get_char()
        i = 0
        chars_array = []

        while char != "\"":
            prev_position = self._position
            if i == MAX_STRING:
                raise LexerError("string too long (max 256)", self._position)
            if char in ["EOF", "\n"]:
                raise LexerError(f"can't find closing \" for string: {''.join(chars_array)}", prev_position)

            i += 1
            chars_array.append(char)

            self._next_char()
            char = self._get_char()

        token = Token(TokenType.STRING_VALUE, self._position, ''.join(chars_array))
        self._next_char()
        return token

    def _try_build_single_operator(self):
        char = self._scanner.get_char()

        if char in self.single_operators:
            self._next_char()
            return Token(self.single_operators[char], self._position)
        return None

    def _try_build_two_char_operator(self):
        char = self._get_char()

        if char in self.double_operators:
            self._next_char()
            if self._get_char() == char:
                return Token(self.double_operators[char], self._position)
        return None

    def _try_build_one_or_two_char_operator(self):
        char = self._get_char()

        if char in self.conflict_operators["single"]:
            self._next_char()
            if self._get_char() == "=":
                return Token(self.conflict_operators["double"][char+"="], self._position)
            return Token(self.conflict_operators["single"][char], self._position)

        return None

    def _try_build_operator(self):
        token = self._try_build_two_char_operator() \
            or self._try_build_one_or_two_char_operator()

        if token:
            return token
        return None

    def _try_build_divide_or_comment(self):
        char = self._get_char()

        if char != "/":
            return None

        self._next_char()
        if self._get_char() == "/":
            self._next_char()
            while self._get_char() != "EOF":
                if self._get_char() == "\n":
                    self._next_char()
                    self._try_build_divide_or_comment()
                    break
                self._next_char()
        else:
            return Token(TokenType.DIVIDE, self._position)
        return None

    def _try_build_keyword_or_type_or_id(self):
        char = self._get_char()

        if not char.isalpha():
            return None
        
        id_or_keyword_chars = []
        i = 0

        while char.isalpha() and char != "EOF":
            if i > MAX_STRING:
                raise LexerError("ID too long (max 256)", self._position)
            i += 1
            id_or_keyword_chars.append(char)
            self._next_char()
            char = self._get_char()

        if len(id_or_keyword_chars) == 0:
            return None
        elif (result := ''.join(id_or_keyword_chars)) in self.keywords:
            if result in ['true', 'false']:
                return Token(TokenType.BOOL_VALUE, self._position, result)
            return Token(self.keywords[result], self._position)
        else:
            return Token(TokenType.ID, self._position, result)

    def generate_tokens(self):
        while (token := self.try_build_token()).type != TokenType.EOF:
            yield token
        yield token


if __name__ == "__main__":
    scanner = Scanner(StringIO("l9"))
    lexer = Lexer(scanner)
    array = lexer.try_build_token()
