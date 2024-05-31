from src.scanner.position import Position


class InterpreterError(Exception):
    def __init__(self, position=None, message=None) -> None:
        self.position: Position | None = position
        self.message: str | None = message

    def __str__(self) -> str:
        message = ''
        if self.message:
            message += self.message
        else:
            message += "Undefined error"
        if self.position:
            message += f", at line {self.position.line}, column: {self.position.column}"
        return message
