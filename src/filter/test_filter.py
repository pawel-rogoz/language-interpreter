from src.lexer.lexer import Lexer
from src.lexer.lexer_error import LexerError
from src.scanner.position import Position
from src.scanner.scanner import Scanner
from src.tokens.token_type import TokenType
from src.tokens.token import Token
from src.filter.filter import Filter

from io import StringIO, TextIOBase
import pytest


class TestInit:
    def test_filter_init_value(self):
        text = StringIO("")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        filter = Filter(lexer)
        assert filter.lexer == lexer

class TestComments:
    def test_filter_skip_comments(self):
        text = StringIO("//comment\n1")
        scanner = Scanner(text)
        lexer = Lexer(scanner)
        filter = Filter(lexer)
        tokens_types = []
        for token in filter.generate_tokens():
            tokens_types.append(token.type)
        assert tokens_types == [TokenType.INT_VALUE, TokenType.EOF]