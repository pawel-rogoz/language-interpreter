from src.scanner.position import Position


class LexerError(Exception):
    def __init__(self, message: str, position: Position) -> None:
        self.message = message
        self.position = position

    def __str__(self) -> None:
        return f"{self.__class__.__name__}: {self.message}, at line: {self.position.line}, column: {self.position.column}"


class IntError(LexerError):
    def __init__(self, message: str, position: Position):
        super().__init__(message, position)


class FloatError(LexerError):
    def __init__(self, message: str, position: Position):
        super().__init__(message, position)


class StringError(LexerError):
    def __init__(self, message: str, position: Position):
        super().__init__(message, position)


class EscapeCharacterError(LexerError):
    def __init__(self, message: str, position: Position):
        super().__init__(message, position)


class IdentifierError(LexerError):
    def __init__(self, message: str, position: Position):
        super().__init__(message, position)


class CreateTokenError(LexerError):
    def __init__(self, message: str, position: Position):
        super().__init__(message, position)
