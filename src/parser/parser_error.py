from src.scanner.position import Position


class ParserError(Exception):
    def __init__(self, message: str, position: Position) -> None:
        self.message = message
        self.position = position

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}, at line: {self.position.line}, column: {self.position.column}"


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
