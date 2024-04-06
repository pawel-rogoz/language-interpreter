from src.scanner.position import Position

class LexerError(Exception):
    def __init__(self, message: str, position: Position) -> None:
        self.message = message
        self.position = position

    def __str__(self) -> None:
        return f"ERROR: {self.message}, at line: {self.position.line}, column: {self.position.column}"