from typing import Union
from io import StringIO, TextIOBase

# from src.scanner.position import Position
from ..scanner.position import Position
from ..scanner.scanner import Scanner
# from src.scanner.scanner import Scanner
# from src.token.token_type import TokenType
from ..tokens.token_type import TokenType
# from src.token.token import Token
from ..tokens.token_2 import Token

class Lexer:
    def __init__(self, scanner: Scanner) -> None:
        self._position = Position(0,0)
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
        "desc": TokenType.DESC
    }

    def _get_char(self):
        return self._scanner.get_char()
    
    def _next_char(self):
        self._scanner.next_char()
        self._position = self._scanner.current_position

    def _skip_whitespaces(self):
        while self._scanner.get_char() == " ":
            self._scanner.next_char

    def _try_build_token(self):
        self._skip_whitespaces()

        token = \
            self._try_build_eof() \
            or self._try_build_number() \
            or self._try_build_string() \
            or self._try_build_keyword_or_id() \
            or self._try_build_type() \
            or self._try_build_single_operator() \

    def _try_build_eof(self):
        if self._scanner.get_char() == 'EOF':
            return Token(TokenType.EOF, self._position)
        return None
    
    def _try_build_number(self):
        if not self._scanner.get_char().isdigit():
            return None
        
        int_value = self._try_build_integer()

    def _try_build_integer(self):
        char = self._scanner.get_char()

        power = 0
        number = 0
        i = 0

        while char.isdigit():
            number = number * 10 + int(char)
            power += 1
            i += 1
            self._next_char()
            char = self._get_char()
        