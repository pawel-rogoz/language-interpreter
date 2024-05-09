from src.scanner.position import Position


class LexerError(Exception):
    def __init__(self, message: str, position: Position) -> None:
        self.message = message
        self.position = position

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}, at line: {self.position.line}, column: {self.position.column}"


class IntError(LexerError):
    pass


class FloatError(LexerError):
    pass


class StringError(LexerError):
    pass


class EscapeCharacterError(LexerError):
    pass


class IdentifierError(LexerError):
    pass


class CreateTokenError(LexerError):
    pass


class TwoCharOperatorError(LexerError):
    pass
