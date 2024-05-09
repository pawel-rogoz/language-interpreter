import math
import argparse
import os
from io import StringIO

from src.scanner.scanner import Scanner
from src.tokens.token_type import TokenType
from src.tokens.token import Token
from src.lexer.lexer_error import *


class Lexer:
    def __init__(self, scanner: Scanner, max_string=256, max_digit=10) -> None:
        self._scanner = scanner
        self._max_string = max_string
        self._max_digit = max_digit

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
        "bool": TokenType.BOOL,
        "Pair": TokenType.PAIR,
        "List": TokenType.LIST,
        "Dict": TokenType.DICT,
        "void": TokenType.VOID
    }

    escape_characters = {
        "n": "\n",
        "t": "\t",
        "r": "\r",
        "f": "\f",
        "b": "\b",
        "\"": "\"",
        "\\": "\\",
        "\'": "\'"
    }

    def get_scanner(self):
        return self._scanner

    def get_position(self):
        return self._scanner.get_position()

    def _get_char(self):
        return self._scanner.get_char()
    
    def _next_char(self):
        self._scanner.next_char()

    def _skip_whitespaces(self):
        while self._get_char().isspace() or self._get_char() == "\n":
            self._next_char()

    def try_build_token(self):
        self._skip_whitespaces()

        position = self.get_position()

        token = self._try_build_divide_or_comment() \
            or self._try_build_eof() \
            or self._try_build_number() \
            or self._try_build_string() \
            or self._try_build_keyword_or_type_or_id() \
            or self._try_build_single_operator() \
            or self._try_build_operator()
        
        if token:
            return token
        
        raise CreateTokenError("Cannot create token", position)

    def _try_build_eof(self):
        position = self.get_position()
        if self._get_char() == 'EOF':
            return Token(TokenType.EOF, position)
        return None
    
    def _try_build_number(self):
        position = self.get_position()

        if not self._scanner.get_char().isdigit():
            return None
        
        integer = self._try_build_integer()

        if self._get_char() == ".":
            return self._try_build_float(integer)
        return Token(TokenType.INT_VALUE, position, integer)

    def _try_build_float(self, integer):
        position = self.get_position()

        self._next_char()
        if not self._get_char().isdigit():
            raise FloatError("can't create float without any number after \".\"", self.get_position())

        float_part = self._try_build_integer()
        num_digits = int(math.log10(float_part)) + 1
        number = float(integer) + float_part * 10 ** -num_digits

        return Token(TokenType.FLOAT_VALUE, position, number)

    def _try_build_integer(self):
        position = self.get_position()

        char = self._scanner.get_char()

        number = 0
        i = 0

        while char.isdigit():
            if i == self._max_digit:
                raise IntError(f"int too big (max {10 ** self._max_digit - 1})", position)
            number = number * 10 + int(char)
            i += 1
            self._next_char()
            char = self._get_char()
        
        return number

    def _try_build_string(self):
        position = self.get_position()

        char = self._scanner.get_char()

        if char != "\"":
            return None

        self._next_char()
        char = self._get_char()
        i = 0
        chars_array = []

        while char != "\"":
            prev_position = self.get_position()
            if i == self._max_string:
                raise StringError(f"string too long (max {self._max_string})", position)
            i += 1

            if char == "EOF":
                raise StringError(f"can't find closing \" for string: {''.join(chars_array)}", prev_position)
            elif char == "\\":
                self._next_char()
                if (char := self._get_char()) in ["t", "n", "'", "\"", "\\", "r", "b", "f"]:
                    chars_array.append(self.escape_characters[char])
                else:
                    raise EscapeCharacterError(f"can't find escape character like: \\{char}", prev_position)
                self._next_char()
                char = self._get_char()
                continue

            chars_array.append(char)

            self._next_char()
            char = self._get_char()

        token = Token(TokenType.STRING_VALUE, position, ''.join(chars_array))
        self._next_char()
        return token

    def _try_build_single_operator(self):
        position = self.get_position()

        char = self._scanner.get_char()

        if char in self.single_operators:
            self._next_char()
            return Token(self.single_operators[char], position)
        return None

    def _try_build_two_char_operator(self):
        position = self.get_position()

        char = self._get_char()

        if char in self.double_operators:
            self._next_char()
            if self._get_char() == char:
                self._next_char()
                return Token(self.double_operators[char], position)
            raise TwoCharOperatorError("Cannot create two char operator", position)
        return None

    def _try_build_one_or_two_char_operator(self):
        position = self.get_position()

        char = self._get_char()

        if char in self.conflict_operators["single"]:
            prev_position = self.get_position()
            self._next_char()
            if self._get_char() == "=":
                self._next_char()
                return Token(self.conflict_operators["double"][char+"="], position)
            return Token(self.conflict_operators["single"][char], position)

        return None

    def _try_build_operator(self):
        token = self._try_build_two_char_operator() \
            or self._try_build_one_or_two_char_operator()

        if token:
            return token
        return None

    def _try_build_divide_or_comment(self):
        position = self.get_position()

        char = self._get_char()

        if char != "/":
            return None

        self._next_char()
        if self._get_char() == "/":
            self._next_char()
            chars_array = []
            while (char := self._get_char()) != "EOF":
                if char == "\n":
                    break
                chars_array.append(char)
                self._next_char()
            return Token(TokenType.COMMENT, position, ''.join(chars_array))
        else:
            return Token(TokenType.DIVIDE, position)

    def _try_build_keyword_or_type_or_id(self):
        position = self.get_position()

        char = self._get_char()

        if not char.isalpha():
            return None
        
        id_or_keyword_chars = [char]
        i = 1

        self._next_char()
        char = self._get_char()

        while (char.isalpha() or char.isdigit() or char == "_") and char != "EOF":
            if i > self._max_string:
                raise IdentifierError(f"ID too long (max {self._max_string})", position)
            i += 1
            id_or_keyword_chars.append(char)
            self._next_char()
            char = self._get_char()

        if len(id_or_keyword_chars) == 0:
            return None
        elif (result := ''.join(id_or_keyword_chars)) in self.keywords:
            if result in ['true', 'false']:
                return Token(TokenType.BOOL_VALUE, position, result)
            return Token(self.keywords[result], position)
        else:
            return Token(TokenType.ID, position, result)

    def generate_tokens(self):
        while (token := self.try_build_token()).type != TokenType.EOF:
            yield token
        yield token


def main():
    parser = argparse.ArgumentParser(description="Creates Lexer object for given string or file")
    parser.add_argument("source", help="String or path to file")
    parser.add_argument("--max_digit",
                        help="Declare max number of digits that integer part of int or float can contain",
                        type=int, default=10)
    parser.add_argument("--max_string",
                        help="Declare max number of digits that integer part of int or float can contain",
                        type=int, default=256)
    args = parser.parse_args()

    source = args.source
    max_digit = args.max_digit
    max_string = args.max_string

    try:
        if os.path.exists(source):
            source = open(source, "r", encoding="utf-8")
        else:
            source = StringIO(source)

        scanner = Scanner(source)
        lexer = Lexer(scanner, max_string=max_string, max_digit=max_digit)
        for token in lexer.generate_tokens():
            print(token)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
