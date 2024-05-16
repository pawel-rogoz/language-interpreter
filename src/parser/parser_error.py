from src.scanner.position import Position
from src.tokens.token_type import TokenType


class ParserError(Exception):
    def __init__(self, position=None, message=None, expected_token=None, actual_token=None) -> None:
        self.position: Position | None = position
        self.message: str | None = message
        self.expected_token: set = expected_token
        self.actual_token: TokenType | None = actual_token

    def __str__(self) -> str:
        message = ''
        if self.expected_token and self.actual_token:
            expected_tokens = "" if len(self.expected_token) <= 1 else "one of: "
            for token in self.expected_token:
                expected_tokens += f"{token}, "
            message += f"Expected {expected_tokens}got: {self.actual_token}"
        elif self.message:
            message += self.message
        else:
            message += "Undefined error"
        if self.position:
            message += f", at line {self.position.line}, column: {self.position.column}"
        return message


class FunctionExistsError(ParserError):
    pass


class IdMissingError(ParserError):
    pass


class BracketMissingError(ParserError):
    pass


class SemicolonMissingError(ParserError):
    pass


class ExpressionMissingError(ParserError):
    pass


class IdOrCallMissingError(ParserError):
    pass


class ClassDeclarationError(ParserError):
    pass


class LinqExpressionError(ParserError):
    pass


class IdOrCallExpressionError(ParserError):
    pass


class IndexExpressionError(ParserError):
    pass
