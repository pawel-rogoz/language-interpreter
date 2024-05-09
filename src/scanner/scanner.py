from typing import Union
from io import StringIO, TextIOBase

from src.scanner.position import Position


class Scanner:
    def __init__(self, source: Union[TextIOBase, StringIO]) -> None:
        self.current_position: Position = Position(1, 0)
        self.current_char: str | None = None
        self.source: Union[TextIOBase, StringIO] = source
        self.next_char()

    # escape_characters = {
    #     "n": "\n",
    #     "t": "\t",
    #     "r": "\r",
    #     "f": "\f",
    #     "b": "\b",
    #     "\"": "\"",
    #     "\\": "\\",
    #     "\'": "\'"
    # }

    def next_char(self):
        char = self.source.read(1)
        
        if not char:
            self.current_char = 'EOF'
            self.current_position = self.current_position.next_column()

        elif char == "\n":
            self.current_char = "\n"
            self.current_position = self.current_position.next_line()

        elif char == "\r":
            current_position = self.source.tell()
            if (self.source.read(1)) == "\n":
                self.current_char = "\n"
                self.current_position = self.current_position.next_line()
            else:
                self.source.seek(current_position)
                self.current_char = "\r"
                self.current_position = self.current_position.next_column()

        else:
            self.current_char = char
            self.current_position = self.current_position.next_column()

    def get_char(self):
        return self.current_char
    
    def get_position(self):
        return self.current_position


if __name__ == "__main__":
    scanner = Scanner(StringIO("\r\n"))