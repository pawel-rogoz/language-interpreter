from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.parser.classes.function_definition import FunctionDefinition
    from src.parser.classes.program import Program
    from src.parser.classes.block import Block
    from src.parser.classes.statement import (ReturnStatement, DeclarationStatement, InitializationStatement,
                                              ExpressionStatement, AssignmentStatement, IfStatement, WhileStatement)
    from src.parser.classes.expression import (CastingExpression, IndexingExpression, LiteralExpression,
                                               IdOrCallExpression, IdExpression, FunctionCallExpression,
                                               FieldAccessExpression, MethodCallExpression,
                                               MethodCallAndFieldAccessExpression, IndexAccessExpression,
                                               FunctionCallAndIndexExpression, ClassInitializationExpression, OrExpression,
                                               AndExpression, GreaterExpression, LessExpression, GreaterEqualExpression,
                                               LessEqualExpression, EqualExpression, NotEqualExpression,
                                               MultiplicationExpression, DivisionExpression, AdditionExpression,
                                               SubtractionExpression, DotCallExpression, NegationExpression,
                                               UnarySubtractionExpression, TermExpression)
    from src.interpreter.embedded_functions import (PrintFunctionDefinition, ValueFunctionDefinition,
                                                    KeyFunctionDefinition, KeysFunctionDefinition, ValuesFunctionDefinition,
                                                    AddFunctionDefinition, IsKeyFunctionDefinition, LengthFunctionDefinition,
                                                    PushFunctionDefinition, PopFunctionDefinition, RemoveFunctionDefinition,
                                                    ForEachFunctionDefinition, WhereFunctionDefinition,
                                                    SelectFunctionDefinition, OrderByFunctionDefinition)


class Visitor(ABC):
    @abstractmethod
    def visit_program(self, element: 'Program'):
        pass

    @abstractmethod
    def visit_function_definition(self, element: 'FunctionDefinition'):
        pass

    @abstractmethod
    def visit_block(self, element: 'Block'):
        pass

    @abstractmethod
    def visit_return_statement(self, element: 'ReturnStatement'):
        pass

    @abstractmethod
    def visit_declaration_statement(self, element: 'DeclarationStatement'):
        pass

    @abstractmethod
    def visit_initialization_statement(self, element: 'InitializationStatement'):
        pass

    @abstractmethod
    def visit_expression_statement(self, element: 'ExpressionStatement'):
        pass

    @abstractmethod
    def visit_assignment_statement(self, element: 'AssignmentStatement'):
        pass

    @abstractmethod
    def visit_if_statement(self, element: 'IfStatement'):
        pass

    @abstractmethod
    def visit_while_statement(self, element: 'WhileStatement'):
        pass

    @abstractmethod
    def visit_casting_expression(self, element: 'CastingExpression'):
        pass

    @abstractmethod
    def visit_indexing_expression(self, element: 'IndexingExpression'):
        pass

    @abstractmethod
    def visit_literal_expression(self, element: 'LiteralExpression'):
        pass

    @abstractmethod
    def visit_id_or_call_expression(self, element: 'IdOrCallExpression'):
        pass

    @abstractmethod
    def visit_id_expression(self, element: 'IdExpression'):
        pass

    @abstractmethod
    def visit_function_call_expression(self, element: 'FunctionCallExpression'):
        pass

    @abstractmethod
    def visit_field_access_expression(self, element: 'FieldAccessExpression'):
        pass

    @abstractmethod
    def visit_method_call_expression(self, element: 'MethodCallExpression'):
        pass

    @abstractmethod
    def visit_method_call_and_field_access_expression(self, element: 'MethodCallAndFieldAccessExpression'):
        pass

    @abstractmethod
    def visit_index_access_expression(self, element: 'IndexAccessExpression'):
        pass

    @abstractmethod
    def visit_function_call_and_index_expression(self, element: 'FunctionCallAndIndexExpression'):
        pass

    @abstractmethod
    def visit_class_initialization_expression(self, element: 'ClassInitializationExpression'):
        pass

    @abstractmethod
    def visit_or_expression(self, element: 'OrExpression'):
        pass

    @abstractmethod
    def visit_and_expression(self, element: 'AndExpression'):
        pass

    @abstractmethod
    def visit_greater_expression(self, element: 'GreaterExpression'):
        pass

    @abstractmethod
    def visit_less_expression(self, element: 'LessExpression'):
        pass

    @abstractmethod
    def visit_greater_equal_expression(self, element: 'GreaterEqualExpression'):
        pass

    @abstractmethod
    def visit_less_equal_expression(self, element: 'LessEqualExpression'):
        pass

    @abstractmethod
    def visit_equal_expression(self, element: 'EqualExpression'):
        pass

    @abstractmethod
    def visit_not_equal_expression(self, element: 'NotEqualExpression'):
        pass

    @abstractmethod
    def visit_multiplication_expression(self, element: 'MultiplicationExpression'):
        pass

    @abstractmethod
    def visit_division_expression(self, element: 'DivisionExpression'):
        pass

    @abstractmethod
    def visit_addition_expression(self, element: 'AdditionExpression'):
        pass

    @abstractmethod
    def visit_subtraction_expression(self, element: 'SubtractionExpression'):
        pass

    @abstractmethod
    def visit_dot_call_expression(self, element: 'DotCallExpression'):
        pass

    @abstractmethod
    def visit_negation_expression(self, element: 'NegationExpression'):
        pass

    @abstractmethod
    def visit_unary_subtraction_expression(self, element: 'UnarySubtractionExpression'):
        pass

    @abstractmethod
    def visit_term_expression(self, element: 'TermExpression'):
        pass

    @abstractmethod
    def visit_print_function(self, element: 'PrintFunctionDefinition'):
        pass

    @abstractmethod
    def visit_value_function(self, element: 'ValueFunctionDefinition'):
        pass

    @abstractmethod
    def visit_key_function(self, element: 'KeyFunctionDefinition'):
        pass

    @abstractmethod
    def visit_keys_function(self, element: 'KeysFunctionDefinition'):
        pass

    @abstractmethod
    def visit_values_function(self, element: 'ValuesFunctionDefinition'):
        pass

    @abstractmethod
    def visit_add_function(self, element: 'AddFunctionDefinition'):
        pass

    @abstractmethod
    def visit_is_key_function(self, element: 'IsKeyFunctionDefinition'):
        pass

    @abstractmethod
    def visit_length_function(self, element: 'LengthFunctionDefinition'):
        pass

    @abstractmethod
    def visit_push_function(self, element: 'PushFunctionDefinition'):
        pass

    @abstractmethod
    def visit_pop_function(self, element: 'PopFunctionDefinition'):
        pass

    @abstractmethod
    def visit_remove_function(self, element: 'RemoveFunctionDefinition'):
        pass

    @abstractmethod
    def visit_for_each_function(self, element: 'ForEachFunctionDefinition'):
        pass

    @abstractmethod
    def visit_where_function(self, element: 'WhereFunctionDefinition'):
        pass

    @abstractmethod
    def visit_select_function(self, element: 'SelectFunctionDefinition'):
        pass

    @abstractmethod
    def visit_orderby_function(self, element: 'OrderByFunctionDefinition'):
        pass
