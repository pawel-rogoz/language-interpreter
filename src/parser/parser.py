from src.filter.filter import Filter
from io import StringIO
from src.lexer.lexer import Lexer
from src.parser.classes.type import Type, BaseType, FunctionType, KeyValueType, ElementType
from src.scanner.position import Position
from src.scanner.scanner import Scanner
from src.tokens.token import Token

from src.parser.parser_interface import ParserInterface
from src.parser.classes.program import Program
from src.parser.classes.function_definition import FunctionDefinition
from src.parser.classes.parameter import Parameter
from src.parser.classes.block import Block

from src.parser.classes.expression import Expression, GreaterExpression, GreaterEqualExpression, LessExpression, \
    LessEqualExpression, EqualExpression, NotEqualExpression, AdditionExpression, SubtractionExpression, \
    MultiplicationExpression, DivisionExpression, OrExpression, AndExpression, NegationExpression, \
    UnarySubtractionExpression, CastingExpression, IndexingExpression, LiteralExpression, ClassInitializationExpression, \
    FunctionCallAndIndexExpression, FunctionCallExpression, IndexAccessExpression, IdExpression, IdOrCallExpression, \
    DotCallExpression, MethodCallAndFieldAccessExpression, MethodCallExpression, FieldAccessExpression
from src.parser.classes.statement import Statement, DeclarationStatement, InitializationStatement, AssignmentStatement, \
    ExpressionStatement, ReturnStatement, IfStatement, WhileStatement
from src.parser.classes.if_parts import ElseIfPart, IfPart, ElsePart
from src.parser.parser_error import ParserError, FunctionExistsError, MainNotImplementedError, IdMissingError, \
    BracketMissingError, SemicolonMissingError, ExpressionMissingError, ClassDeclarationError, \
    IdOrCallMissingError, IndexExpressionError
from src.tokens.token_type import TokenType


class Parser(ParserInterface):
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

    def _get_expression(self, operator: Token, left: Expression, right: Expression) -> Expression | None:
        relation_operators = {
            TokenType.GREATER: GreaterExpression(left, right, operator.position),
            TokenType.GREATER_EQUAL: GreaterEqualExpression(left, right, operator.position),
            TokenType.LESS: LessExpression(left, right, operator.position),
            TokenType.LESS_EQUAL: LessEqualExpression(left, right, operator.position),
            TokenType.EQUAL: EqualExpression(left, right, operator.position),
            TokenType.NOT_EQUAL: NotEqualExpression(left, right, operator.position),
            TokenType.PLUS: AdditionExpression(left, right, operator.position),
            TokenType.MINUS: SubtractionExpression(left, right, operator.position),
            TokenType.MULTIPLY: MultiplicationExpression(left, right, operator.position),
            TokenType.DIVIDE: DivisionExpression(left, right, operator.position),
        }

        return relation_operators.get(operator.type)

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

    def _must_be(self, token_types: set, exception: ParserError) -> Token:
        # TODO -> don't create a new object every time you call _must_be()
        if (token := self.current_token).type not in token_types:
            exception.expected_token = token_types
            exception.actual_token = token.type
            exception.position = token.position
            raise exception

        self._consume_token()
        return token

    # program = { functionDefinition }
    def parse_program(self) -> Program:
        functions = dict()
        while function_definition := self.parse_function_definition():
            if function_definition.name in functions.keys():
                raise FunctionExistsError(message=f"Function {function_definition.name} has been already implemented",
                                          position=function_definition.position)
            else:
                functions.update({function_definition.name: function_definition})

        if "main" not in functions.keys():
            raise MainNotImplementedError(message=f"Function main must be implemented", position=None)

        return Program(functions)

    # functionDefinition = functionType, id, "(", [ functionParameter, { ",", functionParameter } ], ")", body
    def parse_function_definition(self) -> FunctionDefinition | None:
        position = self._get_position()
        type = self.parse_function_type()
        if type is None:
            return None
        name = self._must_be({TokenType.ID}, IdMissingError()).value
        self._must_be({TokenType.ROUND_OPEN}, BracketMissingError())
        parameters = self.parse_parameters()
        self._must_be({TokenType.ROUND_CLOSE}, BracketMissingError())
        block = self.parse_block()
        return FunctionDefinition(name=name, type=type, parameters=parameters, block=block, position=position)

    # block = "{", { statement }, "}"
    def parse_block(self) -> Block:
        statements = []
        self._must_be({TokenType.CURLY_OPEN}, BracketMissingError())
        while statement := self.parse_statement():
            statements.append(statement)

        self._must_be({TokenType.CURLY_CLOSE}, BracketMissingError())
        return Block(statements=statements)

    # statement = { initialization | assignmentOrCall | return | ifStatement | whileLoop }
    def parse_statement(self) -> Statement | None:
        statement = self.parse_initialization() \
                    or self.parse_assignment_or_expression() \
                    or self.parse_return_statement() \
                    or self.parse_if_statement() \
                    or self.parse_while_loop()

        if statement:
            return statement
        return None

    # initialization = declaration, [assignment], ";"
    # declaration = type, id
    def parse_initialization(self) -> Statement | None:
        type = self.parse_type()
        if not type:
            return None
        id = self._must_be({TokenType.ID}, IdMissingError())
        expression = self._parse_assignment()
        self._must_be({TokenType.SEMICOLON}, SemicolonMissingError())
        if not expression:
            return DeclarationStatement(type, id.value, id.position)
        return InitializationStatement(type, id.value, expression, id.position)

    # assignment = "=", expression
    def _parse_assignment(self) -> Expression | None:
        if not self._can_be({TokenType.ASSIGN}):
            return None
        if not (expression := self.parse_expression()):
            raise ExpressionMissingError(message="Expected expression after \"=\"", position=self._get_position())
        return expression

    # expression = conjunction, { "||", conjunction }
    def parse_expression(self):
        if not (left := self.parse_conjunction()):
            return None
        if operator := self._can_be({TokenType.OR}):
            if not (right := self.parse_expression()):
                raise ExpressionMissingError(message="Expression after \'||\' expected", position=self._get_position())
            return OrExpression(left, right, operator.position)
        return left

    # conjunction = relationTerm, { "&&", relationTerm }
    def parse_conjunction(self):
        if not (left := self.parse_relation_term()):
            return None
        if operator := self._can_be({TokenType.AND}):
            if not (right := self.parse_conjunction()):
                raise ExpressionMissingError(message="Expression after \"&&\" expected", position=self._get_position())
            return AndExpression(left, right, operator.position)
        return left

    # relationTerm = additiveTerm, [relationOperator, additiveTerm]
    def parse_relation_term(self):
        if not (left := self.parse_additive_term()):
            return None
        if operator := self._can_be(self.relation_operators):
            if not (right := self.parse_relation_term()):
                raise ExpressionMissingError(message="Expression after relation operator expected",
                                             position=self._get_position())
            return self._get_expression(operator, left, right)
        return left

    # additiveTerm = multiplicativeTerm, {("+" | "-"), multiplicativeTerm}
    def parse_additive_term(self):
        if not (left := self.parse_multiplicative_term()):
            return None
        if operator := self._can_be({TokenType.PLUS, TokenType.MINUS}):
            if not (right := self.parse_additive_term()):
                raise ExpressionMissingError(message="Expression after additive operator expected", position=self._get_position())
            return self._get_expression(operator, left, right)
        return left

    # multiplicativeTerm = unaryApplication, {("*" | "/"), unaryApplication}
    def parse_multiplicative_term(self):
        if not (left := self.parse_unary_application()):
            return None
        if operator := self._can_be({TokenType.MULTIPLY, TokenType.DIVIDE}):
            if not (right := self.parse_multiplicative_term()):
                raise ExpressionMissingError(message="Expression after multiplicative operator expected", position=self._get_position())
            return self._get_expression(operator, left, right)
        return left

    # unaryApplication = [ ( "-" | "!" ) ], castingIndexingTerm
    def parse_unary_application(self):
        operator = self._can_be({TokenType.MINUS, TokenType.NEGATE})
        if not (expression := self.parse_casting_indexing_term()):
            return None
        if operator is None:
            return expression
        elif operator.type == TokenType.NEGATE:
            return NegationExpression(expression, operator.position)
        elif operator.type == TokenType.MINUS:
            return UnarySubtractionExpression(expression, operator.position)

    # castingIndexingTerm = ["(", type, ")"], term, ["[", expression, "]"]
    def parse_casting_indexing_term(self):
        type = index = None
        if casting_position := self._can_be({TokenType.ROUND_OPEN}):
            type = self.parse_type()
            self._must_be({TokenType.ROUND_CLOSE}, BracketMissingError())
        if not (expression := self.parse_term()):
            return None
        if indexing_position := self._can_be({TokenType.SQUARE_OPEN}):
            index = self.parse_expression()
            self._must_be({TokenType.SQUARE_CLOSE}, BracketMissingError())
        if index and type:
            return CastingExpression(IndexingExpression(expression, index, indexing_position.position), type, casting_position.position)
        elif index:
            return IndexingExpression(expression, index, indexing_position.position)
        elif type:
            return CastingExpression(expression, type, casting_position.position)
        else:
            return expression

    # term = literal | idOrCall | "(", expression, ")" | classInitialization
    def parse_term(self):
        expression = self.parse_literal() \
                     or self.parse_id_or_call() \
                     or self.parse_class_initialization()

        if not expression:
            if self._can_be({TokenType.ROUND_OPEN}):
                expression = self.parse_expression()
                self._must_be({TokenType.ROUND_CLOSE}, BracketMissingError())
            else:
                return None

        return expression

    # literal = bool | string | number | floatNumber
    def parse_literal(self):
        if token := self._can_be({TokenType.BOOL_VALUE, TokenType.STRING_VALUE, TokenType.INT_VALUE,
                                  TokenType.FLOAT_VALUE}):
            return LiteralExpression(type=(self.token_type_to_type[token.type]), value=token.value, position=token.position)
        return None

    # classInitialization = "new", className, "(", arguments, ")"
    def parse_class_initialization(self):
        if not (operator := self._can_be({TokenType.NEW})):
            return None
        if not (type := self.parse_class_type()):
            raise ClassDeclarationError(message="Expected class type", position=self._get_position())
        arguments = self._parse_arguments()
        return ClassInitializationExpression(type, arguments, operator.position)

    def _parse_class_initialization_type(self):
        if type := self._can_be(self.class_type_set):
            return type
        return None

    # assignmentOrExpression = expression, [ "=", expression ], ";"
    def parse_assignment_or_expression(self) -> Statement | None:
        assign_expression = None
        if not (expression := self.parse_expression()):
            return None
        if operator := self._can_be({TokenType.ASSIGN}):
            if not (assign_expression := self.parse_expression()):
                raise ExpressionMissingError(message="Expression expected after \"=\"", position=self._get_position())
        self._must_be({TokenType.SEMICOLON}, SemicolonMissingError())
        if assign_expression:
            return AssignmentStatement(expression, assign_expression, operator.position)
        return ExpressionStatement(expression, expression.position)

    # idOrCall = id, [ callOrIndex ], [ { "." id, [ callOrIndex ] } ]
    # callOrIndex = "(", parameters, ")", "[" expression, "]"
    # instead of
    # [ { [ ".", id ], "(", parameters, ")", } ], [ "[", expression, "]" ]
    def parse_id_or_call(self) -> Expression | None:
        if not (id := self._can_be({TokenType.ID})):
            return None
        arguments, index = self._parse_arguments_or_index()
        if arguments is not None and index:
            left = FunctionCallAndIndexExpression(id.value, arguments, index, id.position)
        elif arguments is not None:
            left = FunctionCallExpression(id.value, arguments, id.position)
        elif index:
            left = IndexAccessExpression(id.value, index, id.position)
        else:
            left = IdExpression(id.value, id.position)
        while self._can_be({TokenType.DOT}):
            if not (right := self.parse_dot_expression()):
                raise IdOrCallMissingError(message="Expected expression after \".\"", position=self._get_position())
            return IdOrCallExpression(left, right, id.position)
        return left

    def parse_dot_expression(self) -> Expression | None:
        if not (left := self.parse_single_dot_expression()):
            return None
        if operator := self._can_be({TokenType.DOT}):
            if not (right := self.parse_dot_expression()):
                raise ExpressionMissingError(message="Expected expression after \".\"", position=self._get_position())
            return DotCallExpression(left, right, operator.position)
        return left

    def parse_single_dot_expression(self) -> Expression | None:
        if not (id := self._can_be({TokenType.ID})):
            return None
        arguments, index = self._parse_arguments_or_index()
        if arguments is not None and index:
            return MethodCallAndFieldAccessExpression(id.value, arguments, index, id.position)
        elif arguments is not None:
            return MethodCallExpression(id.value, arguments, id.position)
        elif index:
            return IndexAccessExpression(id.value, index, id.position)
        else:
            return FieldAccessExpression(id.value, id.position)

    # callOrIndex = [ call ], [ index ]
    def _parse_arguments_or_index(self):
        arguments = self._parse_arguments()
        index = self._parse_index()
        return arguments, index

    # call = "(", { expression }, ")"
    # arguments = [ argument, { ",", argument } ]
    def _parse_arguments(self) -> [Expression]:
        if not self._can_be({TokenType.ROUND_OPEN}):
            return None
        arguments = list()
        while argument := self._parse_argument():
            arguments.append(argument)
            self._can_be({TokenType.COMMA})
        self._must_be({TokenType.ROUND_CLOSE}, BracketMissingError())
        return arguments

    # index = expression
    def _parse_index(self) -> Expression | None:
        if not self._can_be({TokenType.SQUARE_OPEN}):
            return None
        if not (index := self.parse_expression()):
            raise IndexExpressionError("", self._get_position())
        self._must_be({TokenType.SQUARE_CLOSE}, BracketMissingError())
        return index

    # argument = expression
    def _parse_argument(self) -> Expression | None:
        if not (expression := self.parse_expression()):
            return None
        return expression

    # return = "return", expression, ";"
    def parse_return_statement(self) -> Statement | None:
        if not (operator := self._can_be({TokenType.RETURN})):
            return None
        expression = self.parse_expression()
        self._must_be({TokenType.SEMICOLON}, SemicolonMissingError())
        return ReturnStatement(expression, operator.position)

    # ifStatement = "if", "(", expression, ")", body, [{"else", "if", "(", expression, ")", body}, "else", body]
    def parse_if_statement(self) -> Statement | None:
        if not (operator := self._can_be({TokenType.IF})):
            return None
        else_if_parts = list()
        else_part = None
        if not (expression := self._parse_if_expression()):
            raise ExpressionMissingError(message="Expected condition expression inside of \"if\"", position=self._get_position())
        block = self.parse_block()
        if_part = IfPart(block, expression)
        while self._can_be({TokenType.ELSE}):
            if self._can_be({TokenType.IF}):
                if not (expression := self._parse_if_expression()):
                    raise ExpressionMissingError(message="Expected condition expression inside of \"else if\"", position=self._get_position())
                block = self.parse_block()
                else_if_parts.append(ElseIfPart(block, expression))
            else:
                block = self.parse_block()
                else_part = ElsePart(block)
                break
        return IfStatement(if_part, else_if_parts, else_part, operator.position)

    # "(", expression, ")"
    def _parse_if_expression(self) -> Expression:
        self._must_be({TokenType.ROUND_OPEN}, BracketMissingError())
        expression = self.parse_expression()
        self._must_be({TokenType.ROUND_CLOSE}, BracketMissingError())
        return expression

    def parse_while_loop(self):
        if not (operator := self._can_be({TokenType.WHILE})):
            return None
        self._must_be({TokenType.ROUND_OPEN}, BracketMissingError())
        if not (expression := self.parse_expression()):
            raise ExpressionMissingError(message="Expected expression after \"while\"", position=self._get_position())
        self._must_be({TokenType.ROUND_CLOSE}, BracketMissingError())
        block = self.parse_block()
        return WhileStatement(expression, block, operator.position)

    # functionParameters = [ declaration, { ",", declaration } ]
    def parse_parameters(self) -> list[Parameter]:
        parameters = list()
        while parameter := self._parse_parameter():
            parameters.append(parameter)
        return parameters

    # declaration = type, id
    def _parse_parameter(self) -> Parameter | None:
        if not (type := self.parse_type()):
            return None
        id = self._must_be({TokenType.ID}, IdMissingError())
        return Parameter(type=type, id=id.value)

    # functionType = type | "void"
    def parse_type(self) -> BaseType | None:
        type = self.parse_class_type() \
            or self.parse_base_type()
        return type

    def parse_function_type(self) -> BaseType | None:
        if type := self.parse_type():
            return type
        if self._can_be({TokenType.VOID}):
            return BaseType(Type.VOID)
        return None

    # type = "int" | "float" | "string" | "bool" | classType
    def parse_base_type(self) -> BaseType | None:
        if not (token := self._can_be(self.base_type_set)):
            return None
        return BaseType(self.token_type_to_type[token.type])

    # classType = className, "<" type, [ ",", type ], ">"
    # className = "Dict" | "List" | "Pair"
    def parse_class_type(self) -> BaseType | None:
        if not (token := self._can_be(self.class_type_set)):
            return None
        class_type = None
        self._must_be({TokenType.LESS}, ClassDeclarationError())
        first_type = self.parse_type().type
        if token.type in self.key_value_type_set:
            self._must_be({TokenType.COMMA},
                          ClassDeclarationError(message="Key-Value type needs two types in declaration",
                                                position=self._get_position()))
            second_type = self.parse_type().type
            class_type = KeyValueType(self.token_type_to_type[token.type], first_type, second_type)
        self._must_be({TokenType.GREATER}, ClassDeclarationError())
        if not class_type:
            class_type = ElementType(self.token_type_to_type[token.type], first_type)
        return class_type
