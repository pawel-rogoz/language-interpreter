from typing import TYPE_CHECKING, Union, Optional

from src.parser.classes.statement import ReturnStatement
from src.parser.classes.type import BaseType, KeyValueType, ElementType, Type
from src.parser.classes.expression import FunctionCallExpression

from src.interpreter.visitor import Visitor
from src.interpreter.interpreter_error import InterpreterError
from src.interpreter.variable import Variable
from src.interpreter.value import Value, BaseValue, KeyValueValue, ElementValue
from src.interpreter.stack import ExecutionStack, FunctionContext, BlockVariables
from src.interpreter.embedded_functions import PrintFunctionDefinition
from src.interpreter.base_function_definition import BaseFunctonDefinition

if TYPE_CHECKING:
    from src.parser.classes.block import Block
    from src.parser.classes.expression import (TermExpression, UnarySubtractionExpression, NegationExpression,
                                               DotCallExpression, SubtractionExpression, AdditionExpression,
                                               DivisionExpression, MultiplicationExpression,
                                               NotEqualExpression, EqualExpression, LessEqualExpression,
                                               GreaterEqualExpression, LessExpression,
                                               GreaterExpression, AndExpression, OrExpression,
                                               ClassInitializationExpression, FunctionCallAndIndexExpression,
                                               IndexAccessExpression,
                                               MethodCallAndFieldAccessExpression, MethodCallExpression,
                                               FieldAccessExpression,
                                               IdExpression, IdOrCallExpression, LiteralExpression,
                                               IndexingExpression, CastingExpression, BinaryExpression, UnaryExpression,
                                               Expression)
    from src.parser.classes.function_definition import FunctionDefinition
    from src.parser.classes.linq_expression import LINQExpression
    from src.parser.classes.program import Program
    from src.parser.classes.statement import (ReturnStatement, DeclarationStatement, InitializationStatement,
                                              WhileStatement, IfStatement, AssignmentStatement, ExpressionStatement)
    from src.parser.classes.if_parts import Part, ExpressionPart


class Interpreter(Visitor):
    def __init__(self, program: 'Program'):
        self._program = program
        program_functions = program.get_functions()
        self._functions_definition = {**program_functions, **self.system_methods}
        self._execution_stack = ExecutionStack()
        self._last_result: Optional[Value] = None
        self._was_return = False
        self._max_recursion = 100
        self._current_recursion = 1

    system_methods = {
        # 'keys',
        # 'values',
        # 'remove',
        # 'forEach',
        # 'isKey',
        # 'length',
        # 'push',
        # 'pop',
        # 'key',
        # 'value',
        'print': PrintFunctionDefinition()
    }

    def interpret(self):
        self.visit_program(self._program)

    @property
    def program(self) -> 'Program':
        return self._program

    @property
    def functions_definition(self) -> dict[str, 'BaseFunctonDefinition']:
        return self._functions_definition

    @property
    def execution_stack(self) -> ExecutionStack:
        return self._execution_stack

    @property
    def last_result(self) -> Value:
        return self._last_result

    def find_function_definition(self, key: str) -> Optional['BaseFunctonDefinition']:
        if key in self._functions_definition.keys():
            return self._functions_definition[key]
        return None

    def _stop_program_execution(self):
        fun_stack_length = len(self._execution_stack.function_contexts)
        if self._current_recursion > self._max_recursion or fun_stack_length > self._max_recursion:
            raise InterpreterError(message=f"Maximum recursion. Program stopped")

    def _get_left_and_right_element(self, element: 'BinaryExpression') -> tuple[Value, Value]:
        element.left.accept(self)
        left = self._last_result
        element.right.accept(self)
        right = self._last_result
        return left, right

    def _get_expression_from_element(self, element: 'UnaryExpression') -> Value:
        element.expression.accept(self)
        expression = self._last_result
        return expression

    def _push_function_context(self, function_context: FunctionContext) -> None:
        self._execution_stack.push_function_context(function_context)

    def _pop_function_context(self) -> Optional[FunctionContext]:
        return self._execution_stack.pop_function_context()

    def _push_block_variables(self, block_variable: BlockVariables) -> None:
        self._execution_stack.push_block_variables(block_variable)

    def _pop_block_variables(self) -> Optional[BlockVariables]:
        return self._execution_stack.pop_block_variables()

    def _add_variable(self, variable: Variable) -> None:
        self._execution_stack.add_variable(variable)

    def _find_variable(self, key: str) -> Optional[Variable]:
        return self._execution_stack.find_variable(key)

    def visit_print_function(self, element: 'PrintFunctionDefinition'):
        variable = self._find_variable("_")
        print(f"{variable.value.value}")

    def visit_expression_statement(self, element: 'ExpressionStatement'):
        element.expression.accept(self)

    def visit_assignment_statement(self, element: 'AssignmentStatement'):
        element.expression.accept(self)
        current_value = self._last_result
        element.assign_expression.accept(self)
        assign_value = self._last_result
        current_value.change_value(assign_value)

    def visit_if_statement(self, element: 'IfStatement') -> None:
        if self._execute_condition_expression_and_block(element.if_part):
            return
        for part in element.else_if_parts:
            if self._execute_condition_expression_and_block(part):
                return
        self._execute_else(element.else_part)

    def _execute_condition_expression_and_block(self, element: Union['ExpressionPart', 'WhileStatement']) -> bool:
        element.expression.accept(self)
        result = self._last_result
        if result.type != BaseType(Type.BOOL):
            raise InterpreterError(message=f"Expression placed as condition must evaluate to bool")
        if result.value:
            block_variables = BlockVariables()
            self._execution_stack.push_block_variables(block_variables)
            element.block.accept(self)
            self._execution_stack.pop_block_variables()
            return True
        return False

    def _execute_else(self, element: 'Part'):
        element.block.accept(self)

    def visit_while_statement(self, element: 'WhileStatement'):
        self._current_recursion += 1
        self._stop_program_execution()
        if self._execute_condition_expression_and_block(element):
            if self._was_return:
                return
            self.visit_while_statement(element)
        self._current_recursion = 1

    def visit_linq_expression(self, element: 'LINQExpression'):
        pass

    def visit_casting_expression(self, element: 'CastingExpression') -> None:
        casting_type = element.type
        expression = self._get_expression_from_element(element)
        expression_type = expression.type
        if casting_type == BaseType(Type.STRING):
            if expression_type in {BaseType(Type.INT), BaseType(Type.FLOAT), BaseType(Type.BOOL)}:
                self._last_result = Value(BaseType(Type.STRING), f"{expression.value}")
            else:
                raise InterpreterError(f"Cannot cast {expression_type} to {casting_type}")
        elif casting_type == BaseType(Type.INT):
            if expression_type in {BaseType(Type.FLOAT), BaseType(Type.BOOL)}:
                self._last_result = Value(BaseType(Type.INT), int(expression.value))
            else:
                raise InterpreterError(f"Cannot cast {expression_type} to {casting_type}")
        else:
            raise InterpreterError(f"Cannot cast {expression_type} to {casting_type}")

    def visit_indexing_expression(self, element: 'IndexingExpression'):
        element.index.accept(self)
        index = self._last_result
        expression = self._get_expression_from_element(element)
        if isinstance(expression, ElementValue):
            if index.type != Type.INT:
                raise InterpreterError(f"Cannot evaluate indexing with value type: {index.type}")
            value = expression.get_value(index.value)
            self._last_result = Value(BaseType(expression.type.element_type), value.value)
        elif isinstance(expression, KeyValueValue):
            if index.type != expression.type.key_type:
                raise InterpreterError(f"Key-type is: {expression.type.key_type}, not: {index.type}")
            value = expression.get_value(index.value)
            self._last_result = Value(BaseType(expression.type.value_type), value.value)
        else:
            raise InterpreterError("Cannot evaluate indexing from this object")

    def visit_literal_expression(self, element: 'LiteralExpression'):
        self._last_result = Value(BaseType(element.type), element.value)

    def visit_id_or_call_expression(self, element: 'IdOrCallExpression'):
        element.left.accept(self)
        element.right.accept(self)

    def visit_id_expression(self, element: 'IdExpression'):
        if not (variable := self._find_variable(element.id)):
            raise InterpreterError(message=f"Can't find variable with id: {element.id}")
        self._last_result = variable.value

    def visit_function_call_expression(self, element: 'FunctionCallExpression'):
        function_name = element.id
        function_arguments = element.arguments
        if function_definition := self.find_function_definition(function_name):
            params = function_definition.parameters

            if len(function_arguments) != len(params):
                raise InterpreterError(f"Number of arguments and parameters doesn't match")

            function_context, block_variables = FunctionContext(), BlockVariables()

            for i in range(0, len(function_arguments)):
                param_type, param_id = params[i].type, params[i].id
                function_arguments[i].accept(self)
                argument = self._last_result
                if argument.type == param_type:
                    block_variables.add_variable(Variable(argument.type, param_id, argument))
                else:
                    raise InterpreterError(message=f"Param: {param_id} takes value type {param_type}, not {argument.type}")

            self._push_function_context(function_context)
            self._push_block_variables(block_variables)
            function_definition.accept(self)

            self._pop_block_variables()
            self._pop_function_context()
        else:
            raise InterpreterError(f"There is no function with id: {function_name}")

    def visit_field_access_expression(self, element: 'FieldAccessExpression'):
        pass

    def visit_method_call_expression(self, element: 'MethodCallExpression'):
        pass

    def visit_method_call_and_field_access_expression(self, element: 'MethodCallAndFieldAccessExpression'):
        pass

    def visit_index_access_expression(self, element: 'IndexAccessExpression'):
        # index = element.index
        # index.accept(self)
        pass

    def visit_function_call_and_index_expression(self, element: 'FunctionCallAndIndexExpression'):
        evaluated_arguments = []
        if element.id in self.system_methods:
            arguments = element.arguments
            for argument in arguments:
                argument.accept(self)
                evaluated_arguments.append(self._last_result)
            self._execute_system_method(element.id, evaluated_arguments)
        else:
            raise InterpreterError(message=f"There is no system function like: {element.id}")

    def _execute_system_method(self, function_name: str, arguments: ['Expression']):
        current_result = self._last_result

        type = current_result.type.type
        match function_name:
            case 'keys':
                if type != Type.DICT:
                    raise InterpreterError(message=f"Can't execute \"keys\" method on object type {type}")
                if len(arguments) != 0:
                    raise InterpreterError(message=f"Method \"keys\" takes 0 arguments, {len(arguments)} given")
                self._last_result = Value(ElementType(Type.LIST, current_result.type.key_type),
                                          current_result.value.keys())
            case 'values':
                if type not in {Type.DICT}:
                    raise InterpreterError(message=f"Can't execute \"values\" method on object type {type}")
                if len(arguments) != 0:
                    raise InterpreterError(message=f"Method \"keys\" takes 0 arguments, {len(arguments)} given")
                self._last_result = Value(ElementType(Type.LIST, current_result.type.value_type),
                                          current_result.value.values())
            case 'add':
                if type not in {Type.PAIR}:
                    raise InterpreterError(message=f"Can't execute \"add\" method on object type {type}")
                if len(arguments) != 1:
                    raise InterpreterError(message=f"Method \"keys\" takes 0 arguments, {len(arguments)} given")
                if arguments[0].type != current_result.type.type:
                    raise InterpreterError(message=f"Cannot add element type {arguments[0].type} to object type"
                                                   f" {current_result.type.type}")
                current_result.value.add_value(arguments)

    def visit_class_initialization_expression(self, element: 'ClassInitializationExpression'):
        type = element.type
        arguments = element.arguments
        result = None
        if isinstance(type, ElementType):
            result = self._handle_element_type_arguments(type, arguments)
        elif isinstance(type, KeyValueType):
            if type.type == Type.PAIR:
                result = self._handle_pair_type_arguments(type, arguments)
            elif type.type == Type.DICT:
                result = self._handle_dict_type_arguments(type, arguments)
        else:
            raise InterpreterError(message=f"Can't initialize class with type: {type.type}")
        self._last_result = result

    def _handle_element_type_arguments(self, type: 'ElementType', arguments: ['Expression']) -> Value:
        element_type = type.element_type
        results = list()
        for argument in arguments:
            argument.accept(self)
            result = self._last_result
            if result.type.type == element_type:
                results.append(result.value)
            else:
                raise InterpreterError(message=f"Element type takes values type: {type.element_type}, not: {result.type}")
        return Value(type, results)

    def _handle_pair_type_arguments(self, type: 'KeyValueType', arguments: ['Expression']) -> Value:
        key_type = type.key_type
        value_type = type.value_type
        if len(arguments) != 2:
            raise InterpreterError(message=f"Pair type takes 0 or 2 positional arguments, not {len(arguments)}")
        arguments[0].accept(self)
        key_value = self._last_result
        if key_value.type.type != key_type:
            raise InterpreterError(message=f"Key should be type {key_type}, not {key_value.type}")
        arguments[0].accept(self)
        element_value = self._last_result
        if element_value.type.type != value_type:
            raise InterpreterError(message=f"Key should be type {key_type}, not {key_value.type}")
        value = dict()
        value[key_value.value] = element_value.value
        return Value(type, value)

    def _handle_dict_type_arguments(self, type: 'KeyValueType', arguments: ['Expression']) -> Value:
        dictionary = dict()
        for argument in arguments:
            argument.accept(self)
            result = self._last_result
            if result.type != KeyValueType(Type.PAIR, type.key_type, type.value_type):
                raise InterpreterError(message=f"Element should be type: {type.type} [ {type.key_type} : {type.value_type} ]")
            if not isinstance(result.value, dict):
                raise InterpreterError(message=f"Element given as Dict Initialization argument should be pair value")
            key = result.value.keys()[0]
            value = result.value[key]
            if key in dictionary.keys():
                raise InterpreterError(message=f"Can't add {key} to Dict - already has this key")
            dictionary[key] = value
        return Value(type, dictionary)

    def visit_or_expression(self, element: 'OrExpression') -> None:
        element.left.accept(self)
        if (left := self._last_result).type != BaseType(Type.BOOL):
            raise InterpreterError(message="Can't evaluate or expression with non-bool types")
        if not left.value:
            element.right.accept(self)
            if self._last_result.type != BaseType(Type.BOOL):
                raise InterpreterError(message="Can't evaluate or expression with non-bool types")

    def visit_and_expression(self, element: 'AndExpression') -> None:
        element.left.accept(self)
        if (left := self._last_result).type != BaseType(Type.BOOL):
            raise InterpreterError(message="Can't evaluate AND expression with non-bool types")
        if left.value:
            element.right.accept(self)
            if self._last_result.type != BaseType(Type.BOOL):
                raise InterpreterError(message="Can't evaluate or expression with non-bool types")

    def visit_greater_expression(self, element: 'GreaterExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} <= {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(BaseType(Type.BOOL), left.value > right.value)
        else:
            raise InterpreterError(
                message=f"Can't evaluate greater expression between objects type: {left.type} and {right.type}")

    def visit_less_expression(self, element: 'LessExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} <= {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(BaseType(Type.BOOL), left.value < right.value)
        else:
            raise InterpreterError(
                message=f"Cannot evaluate less expression between objects type: {left.type} and {right.type}")

    def visit_greater_equal_expression(self, element: 'GreaterEqualExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} <= {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(BaseType(Type.BOOL), left.value >= right.value)
        else:
            raise InterpreterError(message=f"Cannot evaluate greater-equal expression between objects type: {left.type}"
                                           f" and {right.type}")

    def visit_less_equal_expression(self, element: 'LessEqualExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} <= {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(BaseType(Type.BOOL), left.value <= right.value)
        raise InterpreterError(
            f"Cannot evaluate less-equal expression between objects type: {left.type} and {right.type}")

    def visit_equal_expression(self, element: 'EqualExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {Type.INT, Type.FLOAT} or left.type == right.type:
            self._last_result = Value(BaseType(Type.BOOL), left.value == right.value)
        else:
            raise InterpreterError(
                f"Cannot evaluate equal expression between objects type: {left.type} and {right.type}")

    def visit_not_equal_expression(self, element: 'NotEqualExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {Type.INT, Type.FLOAT} or left.type == right.type:
            self._last_result = Value(BaseType(Type.BOOL), left.value != right.value)
        else:
            raise InterpreterError(
                f"Cannot evaluate not equal expression between objects type: {left.type} and {right.type}")

    def visit_multiplication_expression(self, element: 'MultiplicationExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {Type.INT, Type.STRING}:
            self._last_result = Value(BaseType(Type.STRING), left.value * right.value)
        elif {left.type, right.type} == {Type.INT, Type.FLOAT} or left.type == right.type == Type.FLOAT:
            self._last_result = Value(BaseType(Type.FLOAT), left.value * right.value)
        elif left.type == right.type == Type.INT:
            self._last_result = Value(BaseType(Type.INT), left.value * right.value)
        else:
            raise InterpreterError(f"Cannot evaluate multiplication expression between objects type: {left.type}"
                                   f" and {right.type}")

    def visit_division_expression(self, element: 'DivisionExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {Type.INT, Type.FLOAT}:
            self._last_result = Value(BaseType(Type.FLOAT), left.value / right.value)
        else:
            raise InterpreterError(
                f"Cannot evaluate division expression between objects type: {left.type} and {right.type}")

    def visit_addition_expression(self, element: 'AdditionExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {BaseType(Type.INT), BaseType(Type.FLOAT)} or left.type == right.type == BaseType(
                Type.FLOAT):
            self._last_result = Value(BaseType(Type.FLOAT), left.value + right.value)
        elif left.type == right.type and left.type in {BaseType(Type.INT), BaseType(Type.STRING)}:
            self._last_result = Value(left.type, left.value + right.value)
        else:
            raise InterpreterError(
                f"Cannot evaluate addition expression between objects type: {left.type} and {right.type}")

    def visit_subtraction_expression(self, element: 'SubtractionExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {BaseType(Type.INT), BaseType(Type.FLOAT)} or left.type == right.type == BaseType(
                Type.FLOAT):
            self._last_result = Value(BaseType(Type.FLOAT), left.value - right.value)
        elif left.type == right.type == BaseType(Type.INT):
            self._last_result = Value(BaseType(Type.INT), left.value - right.value)
        else:
            raise InterpreterError(f"Cannot evaluate subtraction expression between objects type: {left.type}"
                                   f" and {right.type}")

    def visit_dot_call_expression(self, element: 'DotCallExpression') -> None:
        element.left.accept(self)
        element.right.accept(self)

    def visit_negation_expression(self, element: 'NegationExpression') -> None:
        expression = self._get_expression_from_element(element)
        if expression.type == BaseType(Type.BOOL):
            self._last_result = Value(BaseType(Type.BOOL), not expression)
        else:
            raise InterpreterError(f"Cannot evaluate negation expression with object type: {expression.type}")

    def visit_unary_subtraction_expression(self, element: 'UnarySubtractionExpression') -> None:
        expression = self._get_expression_from_element(element)
        if expression.type in {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(expression.type, -expression.value)
        else:
            raise InterpreterError(f"Cannot evaluate unary subtraction expression with object type: {expression.type}")

    def visit_term_expression(self, element: 'TermExpression'):
        element.expression.accept(self)

    def visit_initialization_statement(self, element: 'InitializationStatement'):
        type, id, expression = element.type, element.id, element.expression
        expression.accept(self)
        value = self._last_result
        if value.type == type:
            variable = Variable(value.type, id, value)
            self._add_variable(variable)
        else:
            raise InterpreterError(message=f"Can't assign value type: {value.type} to variable type: {type}")

    def visit_declaration_statement(self, element: 'DeclarationStatement'):
        type, id = element.type, element.id
        variable = Variable(type, id, None)
        self._add_variable(variable)

    def visit_return_statement(self, element: 'ReturnStatement') -> None:
        expression = element.expression
        expression.accept(self)
        result = self._last_result
        self._last_result = Value(result.type, result.value)
        self._was_return = True

    def visit_block(self, element: 'Block') -> None:
        for statement in element.statements:
            statement.accept(self)
            if self._was_return:
                return
        self._last_result = Value(BaseType(Type.VOID), None)

    def visit_function_definition(self, element: 'FunctionDefinition'):
        self._stop_program_execution()
        block = element.block
        block.accept(self)
        result = self._last_result

        if result.type != element.type:
            raise InterpreterError(message=f"Function {element.name} should return value type: {element.type},"
                                           f" not {result.type}")

        self._was_return = False

    def visit_program(self, element: 'Program'):
        functions = self._functions_definition
        if "main" not in functions.keys():
            raise InterpreterError(message="Main function must be implemented")
        main = FunctionCallExpression(id="main", arguments=[])
        main.accept(self)
        result = self._last_result
        print(f"Program exited with value: {result.value} ({result.type})\n")


if __name__ == "__main__":
    from io import StringIO
    from src.scanner.scanner import Scanner
    from src.lexer.lexer import Lexer
    from src.filter.filter import Filter
    from src.parser.parser import Parser

    text = StringIO("int main() { List<int> a = new List<int>(1); } string b() { return \"dupa\"; }}")
    scanner = Scanner(text)
    lexer = Lexer(scanner)
    filter = Filter(lexer)
    parser = Parser(filter)
    program = parser.parse_program()
    interpreter = Interpreter(program)
    interpreter.interpret()
