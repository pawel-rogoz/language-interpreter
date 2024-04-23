from src.lexer.lexer import Lexer
from src.tokens.token_type import TokenType


class Filter:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def try_build_token(self):
        token = self.lexer.try_build_token()

        while token.type == TokenType.COMMENT:
            token = self.lexer.try_build_token()

        return token

    def generate_tokens(self):
        while (token := self.try_build_token()).type != TokenType.EOF:
            yield token
        yield token
