from src.scanner.position import Position
from src.tokens.token_type import TokenType


class ParserError(Exception):
    def __init__(self, message, expected_token, actual_token, position) -> None:
        self.message: str | None = message
        self.expected_token: TokenType | None = expected_token
        self.actual_token: TokenType | None = actual_token
        self.position: Position = position

    def __str__(self) -> str:
        message = ''
        if self.expected_token and self.actual_token:
            message += f"Expected {self.expected_token}, got: {self.actual_token}"
        elif self.message:
            message += self.message
        else:
            message += "Undefined error"
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
