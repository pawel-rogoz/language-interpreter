from src.filter.filter import Filter
from io import StringIO
from src.lexer.lexer import Lexer
from src.scanner.position import Position
from src.scanner.scanner import Scanner
from src.tokens.token_type import TokenType
from src.tokens.token import Token

from src.parser.classes.program import Program
from src.parser.classes.function_definition import FunctionDefinition
from src.parser.classes.parameter import Parameter
from src.parser.classes.block import Block
from src.parser.classes.linq_expression import LINQExpression

from src.parser.classes.type import *
from src.parser.classes.expression import *
from src.parser.classes.statement import *
from src.parser.classes.if_parts import *
from src.parser.parser_error import *


class Parser:
    def __init__(self, filter: Filter):
        self.filter = filter
        self.current_token = None
        self._previous_position = Position(1, 1)
        self._consume_token()

    base_type_set = {
        TokenType.INT,
        TokenType.FLOAT,
        TokenType.STRING,
        TokenType.BOOL
    }

    key_value_type_set = {
        TokenType.DICT,
        TokenType.PAIR
    }

    element_type_set = {
        TokenType.LIST
    }

    class_type_set = key_value_type_set | element_type_set
    function_type_set = {TokenType.VOID} | base_type_set | class_type_set

    token_type_to_type = {
        TokenType.INT: Type.INT,
        TokenType.FLOAT: Type.FLOAT,
        TokenType.BOOL: Type.BOOL,
        TokenType.STRING: Type.STRING,
        TokenType.VOID: Type.VOID,
        TokenType.DICT: Type.DICT,
        TokenType.PAIR: Type.PAIR,
        TokenType.LIST: Type.LIST,
        TokenType.INT_VALUE: Type.INT,
        TokenType.STRING_VALUE: Type.STRING,
        TokenType.BOOL_VALUE: Type.BOOL,
        TokenType.FLOAT_VALUE: Type.FLOAT
    }

    relation_operators = {
        TokenType.LESS,
        TokenType.GREATER,
        TokenType.GREATER_EQUAL,
        TokenType.LESS_EQUAL,
        TokenType.EQUAL,
        TokenType.NOT_EQUAL
    }

    def _get_expression(self, operator, left, right=None) -> Expression | None:
        relation_operators = {
            TokenType.GREATER: GreaterExpression(left, right),
            TokenType.GREATER_EQUAL: GreaterEqualExpression(left, right),
            TokenType.LESS: LessExpression(left, right),
            TokenType.LESS_EQUAL: LessEqualExpression(left, right),
            TokenType.EQUAL: EqualExpression(left, right),
            TokenType.NOT_EQUAL: NotEqualExpression(left, right),
            TokenType.PLUS: AdditionExpression(left, right),
            TokenType.MINUS: SubtractionExpression(left, right),
            TokenType.MULTIPLY: MultiplicationExpression(left, right),
            TokenType.DIVIDE: DivisionExpression(left, right),
        }

        return relation_operators.get(operator)

    def _consume_token(self) -> None:
        if self.current_token:
            self._previous_position = self._get_position()
        self.current_token = self.filter.try_build_token()

    def _get_position(self) -> Position:
        return self.current_token.position

    def _get_previous_position(self) -> Position:
        return self._previous_position

    def _can_be(self, token_types: set) -> Token | None:
        if (token := self.current_token).type not in token_types:
            return None
        self._consume_token()
        return token

    def _must_be(self, token_types: set, exception: Exception) -> Token:
        if (token := self.current_token).type not in token_types:
            raise exception

        self._consume_token()
        return token

    # program = { functionDefinition }
    def parse_program(self) -> Program:
        functions = dict()
        while function_definition := self._parse_function_definition():
            if function_definition.name in functions.keys():
                raise FunctionExistsError(f"Function {function_definition.name} has been already implemented",
                                          function_definition.position)
            else:
                functions.update({function_definition.name: function_definition})

        return Program(functions)

    # functionDefinition = functionType, id, "(", [ functionParameter, { ",", functionParameter } ], ")", body
    def _parse_function_definition(self) -> FunctionDefinition | None:
        position = self._get_position()
        type = self._parse_function_type()
        if type is None:
            return None
        name = (self._must_be({TokenType.ID},
                              IdMissingError("Function has missing id", self._get_position()))
                .value)
        self._must_be({TokenType.ROUND_OPEN},
                      BracketMissingError("Round-open bracket expected", self._get_position()))
        parameters = self._parse_parameters()
        self._must_be({TokenType.ROUND_CLOSE},
                      BracketMissingError("Round-close bracket expected", self._get_position()))
        block = self._parse_block()
        return FunctionDefinition(name=name, type=type, parameters=parameters, block=block, position=position)

    # block = "{", { statement }, "}"
    def _parse_block(self) -> Block:
        statements = []
        self._must_be({TokenType.CURLY_OPEN},
                      BracketMissingError("Square-open bracket expected", self._get_position()))
        while statement := self._parse_statement():
            statements.append(statement)

        self._must_be({TokenType.CURLY_CLOSE},
                      BracketMissingError("Square-close bracket expected", self._get_position()))
        return Block(statements=statements)

    # statement = { initialization | assignmentOrCall | return | ifStatement | whileLoop }
    def _parse_statement(self) -> Statement | None:
        statement = self._parse_initialization() \
                    or self._parse_assignment_or_call() \
                    or self._parse_return() \
                    or self._parse_if_statement() \
                    or self._parse_while_loop()

        if statement:
            return statement
        return None

    # initialization = declaration, [assignment], ";"
    # declaration = type, id
    def _parse_initialization(self) -> Statement | None:
        type = self._parse_type()
        if not type:
            return None
        id = self._must_be({TokenType.ID},
                           IdMissingError("Variable doesn't have id", self._get_position()))
        expression = self._parse_assignment()
        self._must_be({TokenType.SEMICOLON},
                      SemicolonMissingError("Semicolon expected", self._get_position()))
        if not expression:
            return DeclarationStatement(type, id)
        return InitializationStatement(type, id, expression)

    # assignment = "=", expression
    def _parse_assignment(self) -> Expression | None:
        if not self._can_be({TokenType.ASSIGN}):
            return None
        if not (expression := self._parse_expression()):
            raise ExpressionMissingError("Expression after assign expected", self._get_position())
        return expression

    def parse_expression(self):
        return self._parse_expression()

    # expression = conjunction, { "||", conjunction }
    def _parse_expression(self):
        if not (left := self._parse_conjunction()):
            return None
        right = None
        if self._can_be({TokenType.OR}):
            if not (right := self._parse_expression()):
                raise ExpressionMissingError("Expression after \'||\' expected", self._get_position())
            if right.right is None:
                right = right.left
        return OrExpression(left, right)

    # conjunction = relationTerm, { "&&", relationTerm }
    def _parse_conjunction(self):
        if not (left := self._parse_relation_term()):
            return None
        right = None
        if self._can_be({TokenType.AND}):
            if not (right := self._parse_conjunction()):
                raise ExpressionMissingError("Expression after \'&&\' expected", self._get_position())
            if right.right is None:
                right = right.left
        return AndExpression(left, right)

    # relationTerm = additiveTerm, [relationOperator, additiveTerm]
    def _parse_relation_term(self):
        if not (left := self._parse_additive_term()):
            return None
        right = None
        if operator := self._can_be(self.relation_operators):
            if not (right := self._parse_relation_term()):
                raise ExpressionMissingError("Expression after relation operator expected", self._get_position())
            if right.right is None:
                right = right.left
        if operator:
            return self._get_expression(operator.type, left, right)
        return RelationExpression(left, right)

    # additiveTerm = multiplicativeTerm, {("+" | "-"), multiplicativeTerm}
    def _parse_additive_term(self):
        if not (left := self._parse_multiplicative_term()):
            return None
        right = None
        if operator := self._can_be({TokenType.PLUS, TokenType.MINUS}):
            if not (right := self._parse_additive_term()):
                raise ExpressionMissingError("Expression after additive operator expected", self._get_position())
            if right.right is None:
                right = right.left
        if operator:
            return self._get_expression(operator.type, left, right)
        return BinaryExpression(left, right)

    # multiplicativeTerm = unaryApplication, {("*" | "/"), unaryApplication}
    def _parse_multiplicative_term(self):
        if not (left := self._parse_unary_application()):
            return None
        right = None
        if operator := self._can_be({TokenType.MULTIPLY, TokenType.DIVIDE}):
            if not (right := self._parse_multiplicative_term()):
                raise ExpressionMissingError("Expression after multiplicative operator expected", self._get_position())
            if right.right is None:
                right = right.left
        if operator:
            return self._get_expression(operator.type, left, right)
        return BinaryExpression(left, right)

    # unaryApplication = [ ( "-" | "!" ) ], castingIndexingTerm
    def _parse_unary_application(self):
        operator = self._can_be({TokenType.MINUS, TokenType.NEGATE})
        if not (expression := self._parse_casting_indexing_term()):
            return None
        if operator is None:
            return UnaryExpression(expression)
        elif operator.type == TokenType.NEGATE:
            return NegationExpression(expression)
        elif operator.type == TokenType.MINUS:
            return UnarySubtractionExpression(expression)

    # castingIndexingTerm = ["(", type, ")"], term, ["[", expression, "]"]
    def _parse_casting_indexing_term(self):
        type = expression = None
        if self._can_be({TokenType.ROUND_OPEN}):
            type = self._parse_type()
            self._must_be({TokenType.ROUND_CLOSE},
                          BracketMissingError("Expected round-close bracket after casting expression",
                                              self._get_position()))
        if not (term := self._parse_term()):
            return None
        if self._can_be({TokenType.SQUARE_OPEN}):
            expression = self._parse_expression()
            self._must_be({TokenType.SQUARE_CLOSE},
                          BracketMissingError("Expected square-close bracket after indexing expression",
                                              self._get_position()))
        return CastingExpression(expression=IndexingExpression(term, index=expression), type=type)

    # term = literal | idOrCall | "(", expression, ")" | linqOperation | classInitialization
    def _parse_term(self):
        expression = self._parse_literal() \
                     or self._parse_id_or_call() \
                     or self._parse_linq_expression() \
                     or self._parse_class_initialization()

        if not expression:
            if self._can_be({TokenType.ROUND_OPEN}):
                expression = self._parse_expression()
                self._must_be({TokenType.ROUND_CLOSE},
                              BracketMissingError("Expected round-close bracket after expression",
                                                  self._get_position()))
            else:
                return None

        return expression

    # literal = bool | string | number | floatNumber
    def _parse_literal(self):
        if token := self._can_be({TokenType.BOOL_VALUE, TokenType.STRING_VALUE, TokenType.INT_VALUE,
                                  TokenType.FLOAT_VALUE}):
            return LiteralExpression(type=(self.token_type_to_type[token.type]), value=token.value)
        return None

    # linqOperation = "from", expression, [ "where", expression ], [ "orderby", expression, ( "ASC", "DESC" ) ],
    # "select", expression, ";"
    def _parse_linq_expression(self):
        where_expression = orderby_expression = orderby_sorting = None
        if not self._can_be({TokenType.FROM}):
            return None
        if not (from_expression := self._parse_expression()):
            raise Exception
        if self._can_be({TokenType.WHERE}):
            where_expression = self._parse_expression()
        if self._can_be({TokenType.ORDER_BY}):
            orderby_expression = self._parse_expression()
            orderby_sorting = self._must_be({TokenType.ASC, TokenType.DESC})
        self._must_be({TokenType.SELECT})
        if not (select_expression := self._parse_expression()):
            raise Exception
        return LINQExpression(from_expression=from_expression,
                              where_expression=where_expression,
                              orderby_expression=orderby_expression,
                              orderby_sorting=orderby_sorting,
                              select_expression=select_expression)

    # classInitialization = "new", className, "(", arguments, ")"
    def _parse_class_initialization(self):
        if not self._can_be({TokenType.NEW}):
            return None
        type = self._parse_class_type()
        self._must_be({TokenType.ROUND_OPEN},
                      BracketMissingError("Expected round-open error",
                                          self._get_position()))
        arguments = self._parse_arguments()
        self._must_be({TokenType.ROUND_CLOSE},
                      BracketMissingError("Expected round-close error",
                                          self._get_position()))
        return ClassInitializationExpression(type, arguments)

    # assignmentOrCall = idOrCall, [ "=", expression ], ";"
    def _parse_assignment_or_call(self) -> Statement | None:
        expression = None
        if not (id_or_call := self._parse_id_or_call()):
            return None
        if self._can_be({TokenType.ASSIGN}):
            if not (expression := self._parse_expression()):
                raise Exception
        self._must_be({TokenType.SEMICOLON},
                      SemicolonMissingError("Semicolon expected",
                                            self._get_position()))
        if expression:
            return AssignmentStatement(id_or_call, expression)
        return IdOrCallStatement(id_or_call)

    # idOrCall = id, [ callOrIndex ], [ { "." id, [ callOrIndex ] } ]
    # callOrIndex = "(", parameters, ")", "[" expression, "]"
    # instead of
    # [ { [ ".", id ], "(", parameters, ")", } ], [ "[", expression, "]" ]
    def _parse_id_or_call(self) -> Expression | None:
        if not (id := self._can_be({TokenType.ID})):
            return None
        call, index = self._parse_call_or_index()
        nested_id_or_call = None
        if self._can_be({TokenType.DOT}):
            if not (nested_id_or_call := self._parse_id_or_call()):
                raise IdOrCallMissingError("Expected id after dot",
                                           self._get_position())
        return IdOrCallExpression(id, call, index, nested_id_or_call)

    # callOrIndex = [ call ], [ index ]
    def _parse_call_or_index(self):
        call = self._parse_call()
        index = self._parse_index()
        return call, index

    # call = "(", { expression }, ")"
    def _parse_call(self) -> list[Expression] | None:
        if not self._can_be({TokenType.ROUND_OPEN}):
            return None
        arguments = self._parse_arguments()
        self._must_be({TokenType.ROUND_CLOSE},
                      BracketMissingError("Expected round-close bracket",
                                          self._get_position()))
        return arguments

    # index = expression
    def _parse_index(self) -> Expression | None:
        if not self._can_be({TokenType.SQUARE_OPEN}):
            return None
        index = self._parse_expression()
        self._must_be({TokenType.SQUARE_CLOSE},
                      BracketMissingError("Expected round-close bracket",
                                          self._get_position()))
        return index

    # arguments = [ argument, { ",", argument } ]
    def _parse_arguments(self) -> list[Expression]:
        arguments = list()
        while argument := self._parse_argument():
            arguments.append(argument)
        return arguments

    # argument = expression
    def _parse_argument(self) -> Expression | None:
        if not (expression := self._parse_expression()):
            return None
        return expression

    # return = "return", expression, ";"
    def _parse_return(self) -> Statement | None:
        if not self._can_be({TokenType.RETURN}):
            return None
        expression = self._parse_expression()
        self._must_be({TokenType.SEMICOLON},
                      SemicolonMissingError("Expected semicolon",
                                            self._get_position()))
        return ReturnStatement(expression)

    # ifStatement = "if", "(", expression, ")", body, [{"else", "if", "(", expression, ")", body}, "else", body]
    def _parse_if_statement(self) -> Statement | None:
        if not self._can_be({TokenType.IF}):
            return None
        else_if_parts = list()
        else_part = None
        expression = self._parse_if_expression()
        block = self._parse_block()
        if_part = IfPart(expression, block)
        while self._can_be({TokenType.ELSE}):
            if self._can_be({TokenType.IF}):
                expression = self._parse_if_expression()
                block = self._parse_block()
                else_if_parts.append(ElseIfPart(block, expression))
            else:
                block = self._parse_block()
                else_part = ElsePart(block)
                break
        return IfStatement(if_part, else_if_parts, else_part)

    # "(", expression, ")"
    def _parse_if_expression(self) -> Expression:
        self._must_be({TokenType.ROUND_OPEN},
                      BracketMissingError("Expected round-open error",
                                          self._get_position()))
        expression = self._parse_expression()
        self._must_be({TokenType.ROUND_CLOSE},
                      BracketMissingError("Expected round-close error",
                                          self._get_position()))
        return expression

    def _parse_while_loop(self):
        if not self._can_be({TokenType.WHILE}):
            return None
        self._must_be({TokenType.ROUND_OPEN},
                      BracketMissingError("Expected round-open error",
                                          self._get_position()))
        expression = self._parse_expression()
        self._must_be({TokenType.ROUND_CLOSE},
                      BracketMissingError("Expected round-close error",
                                          self._get_position()))
        block = self._parse_block()
        return WhileStatement(expression, block)

    # functionParameters = [ declaration, { ",", declaration } ]
    def _parse_parameters(self) -> list[Parameter]:
        parameters = list()
        while parameter := self._parse_parameter():
            parameters.append(parameter)
        return parameters

    # declaration = type, id
    def _parse_parameter(self) -> Parameter | None:
        type = self._parse_type()
        if not (type := self._parse_type()):
            return None
        id = self._must_be({TokenType.ID},
                           IdMissingError("Expected id",
                                          self._get_position()))
        return Parameter(type=type, id=id)

    # functionType = type | "void"
    def _parse_type(self) -> Type | None:
        type = self._parse_base_type() \
               or self._parse_class_type() \
               or self._parse_function_type()
        return type

    def _parse_function_type(self) -> BaseType | None:
        if not (token := self._can_be(self.function_type_set)):
            return None
        return FunctionType(self.token_type_to_type[token.type])

    # type = "int" | "float" | "string" | "bool" | classType
    def _parse_base_type(self) -> BaseType | None:
        if not (token := self._can_be(self.base_type_set)):
            return None
        return BaseType(self.token_type_to_type[token.type])

    # classType = className, "<" type, [ ",", type ], ">"
    # className = "Dict" | "List" | "Pair"
    def _parse_class_type(self) -> BaseType | None:
        if not (token := self._can_be(self.class_type_set)):
            return None
        class_type = None
        self._must_be({TokenType.LESS},
                      ClassDeclarationError("Expected \'<\'",
                                            self._get_position()))
        first_type = self._parse_type()
        if token.type in self.key_value_type_set:
            self._must_be({TokenType.COMMA},
                          ClassDeclarationError("Key-Value type needs two types in declaration",
                                                self._get_position()))
            second_type = self._parse_type()
            class_type = KeyValueType(self.token_type_to_type[token.type], first_type, second_type)
        self._must_be({TokenType.GREATER},
                      ClassDeclarationError("Expected \'>\'",
                                            self._get_position()))
        if not class_type:
            class_type = ElementType(self.token_type_to_type[token.type], first_type)
        return class_type


text = StringIO("1 && 2 + 3 * !5 > 3 + 4 || 2 && 3 || 3 && 4 || 5")
scanner = Scanner(text)
lexer = Lexer(scanner)
filter = Filter(lexer)
parser = Parser(filter)
expression = parser.parse_expression()
expression