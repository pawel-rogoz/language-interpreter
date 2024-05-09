from dataclasses import dataclass


@dataclass
class Position:
    line: int = 1
    column: int = 0

    def next_line(self):
        return Position(self.line + 1, 0)
    
    def next_column(self):
        return Position(self.line, self.column + 1)