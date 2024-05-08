from src.tokens.token_type import TokenType
from src.parser.classes.parameter import Parameter
from src.parser.classes.block import Block
from src.scanner.position import Position


class FunctionDefinition:
    def __init__(self, name, type, parameters, block, position):
        self.name: str = name
        self.type: TokenType = type
        self.parameters: list[Parameter] = parameters
        self.block: Block = block
        self.position: Position = position
