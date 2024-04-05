from typing import Union
from io import StringIO, TextIOBase

from .position import Position

class Scanner:
    def __init__(self, source: Union[TextIOBase, StringIO]) -> None:
        self.current_position = Position(1,0)
        self.current_char = None
        self.source = source
        self.next_char()

    def next_char(self):
        char = self.source.read(1)
        
        if not char:
            print('EOF')
            self.current_char = 'EOF'
            self.current_position = self.current_position.next_line()

        elif char == "\n":
            print("newline")
            self.current_char = "\n"
            self.current_position = self.current_position.next_line()

        else:
            print(char)
            self.current_char = char
            self.current_position = self.current_position.next_column()

    def get_char(self):
        return self.current_char
    
    def get_position(self):
        return self.current_position