from enum import Enum, auto


class TokenType(Enum):
    # KEYWORDS
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    NEW = auto()

    # LINQ KEYWORDS
    SELECT = auto()
    WHERE = auto()
    FROM = auto()
    ORDER_BY = auto()
    ASC = auto()
    DESC = auto()

    # TYPES
    VOID = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    PAIR = auto()
    LIST = auto()
    DICT = auto()

    # VALUES
    ID = auto()
    COMMENT = auto()
    STRING_VALUE = auto()
    INT_VALUE = auto()
    FLOAT_VALUE = auto()
    BOOL_VALUE = auto()

    # BRACKETS
    ROUND_OPEN = auto()
    ROUND_CLOSE = auto()
    CURLY_OPEN = auto()
    CURLY_CLOSE = auto()
    SQUARE_OPEN = auto()
    SQUARE_CLOSE = auto()
    
    # LOGICAL OPERANDS
    AND = auto()
    OR = auto()
    NEGATE = auto()

    # ARITHMETIC OPERANDS
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    # COMPARISION OPERANDS
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()

    # OTHERS
    DOT = auto()
    SEMICOLON = auto()
    COMMA = auto()
    ASSIGN = auto()
    EOF = auto()
