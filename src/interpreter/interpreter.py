import argparse
from typing import TYPE_CHECKING, Union, Optional

from src.scanner.position import Position

from src.parser.classes.statement import ReturnStatement
from src.parser.classes.type import BaseType, KeyValueType, ElementType, Type
from src.parser.classes.expression import FunctionCallExpression, LiteralExpression
from src.parser.classes.parameter import Parameter, ThisParameter, FunctionParameter
from src.parser.classes.function_definition import FunctionDefinition


from src.interpreter.visitor import Visitor
from src.interpreter.interpreter_error import (InterpreterError, DivisionError, ReturnTypeError, MainNotImplementedError,
                                               ExpressionTypeError, InitializationError, AssignmentError)
from src.interpreter.variable import Variable
from src.interpreter.value import Value, BaseValue, KeyValueValue, ElementValue
from src.interpreter.stack import ExecutionStack, FunctionContext, BlockVariables
from src.interpreter.embedded_functions import (PrintFunctionDefinition, ValueFunctionDefinition, KeyFunctionDefinition,
                                                KeysFunctionDefinition, ValuesFunctionDefinition, AddFunctionDefinition,
                                                IsKeyFunctionDefinition, LengthFunctionDefinition, PushFunctionDefinition,
                                                PopFunctionDefinition, RemoveFunctionDefinition, ForEachFunctionDefinition,
                                                WhereFunctionDefinition, SelectFunctionDefinition, OrderByFunctionDefinition)
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
        self._was_linq = False
        self._max_recursion = 100
        self._current_recursion = 1
        self._last_function_call: Optional[FunctionCallExpression] = None

    system_methods = {
        'keys': KeysFunctionDefinition(),
        'values': ValuesFunctionDefinition(),
        'add': AddFunctionDefinition(),
        'remove': RemoveFunctionDefinition(),
        'forEach': ForEachFunctionDefinition(),
        'isKey': IsKeyFunctionDefinition(),
        'length': LengthFunctionDefinition(),
        'push': PushFunctionDefinition(),
        'pop': PopFunctionDefinition(),
        'key': KeyFunctionDefinition(),
        'value': ValueFunctionDefinition(),
        'print': PrintFunctionDefinition(),
        'orderBy': OrderByFunctionDefinition(),
        'where': WhereFunctionDefinition(),
        'select': SelectFunctionDefinition()
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
        variable = self._find_variable("_print")
        print(f"{variable.value.value}")

    def visit_value_function(self, element: 'ValueFunctionDefinition'):
        value = self._last_result
        if value.type.type != Type.PAIR:
            raise ExpressionTypeError(message=f"can't evaluate value on {value.type.type} object")
        self._last_result = Value(BaseType(value.type.value_type), list(value.value.values())[0])

    def visit_key_function(self, element: 'KeyFunctionDefinition'):
        value = self._last_result
        if value.type.type != Type.PAIR:
            raise ExpressionTypeError(message=f"can't evaluate key on {value.type.type} object")
        self._last_result = Value(BaseType(value.type.key_type), list(value.value.keys())[0])

    def visit_keys_function(self, element: 'KeysFunctionDefinition'):
        value = self._last_result
        if value.type.type != Type.DICT:
            raise ExpressionTypeError(message=f"can't evaluate key on {value.type.type} object")
        self._last_result = Value(ElementType(Type.LIST, value.type.key_type), list(value.value.keys()))

    def visit_values_function(self, element: 'ValuesFunctionDefinition'):
        value = self._last_result
        if value.type.type != Type.DICT:
            raise ExpressionTypeError(message=f"can't evaluate key on {value.type.type} object")
        self._last_result = Value(ElementType(Type.LIST, value.type.value_type), list(value.value.values()))

    def visit_add_function(self, element: 'AddFunctionDefinition'):
        variable = self._find_variable("_add")
        this = self._find_variable("_add_this")
        if not (isinstance(this.type, KeyValueType) and isinstance(variable.type, KeyValueType)):
            raise InterpreterError(message=f"Can't evaluate add with non-key-value type object")
        if not (variable.type.key_type == this.type.key_type and variable.type.value_type == this.type.value_type):
            raise InterpreterError(message=f"Can't evaluate add with different type objects ("
                                           f" {variable.type.key_type} : {variable.type.value_type} ) !="
                                           f"  {this.type.key_type} : {this.type.value_type} )")
        new_value = this.value.value
        new_value[list(variable.value.value.keys())[0]] = list(variable.value.value.values())[0]
        this.value.change_value(Value(this.type, new_value))

    def visit_is_key_function(self, element: 'IsKeyFunctionDefinition'):
        variable = self._find_variable("_is_key")
        this = self._find_variable("_is_key_this")
        if not isinstance(this.type, KeyValueType):
            raise InterpreterError(message=f"Can't evaluate \"is key\" on non-key-value object")
        if not variable.type.type == this.type.key_type:
            raise InterpreterError(message=f"Given key type is different from object key type")
        self._last_result = Value(BaseType(Type.BOOL), variable.value.value in this.value.value.keys())

    def visit_length_function(self, element: 'LengthFunctionDefinition'):
        this = self._find_variable("_length_this")
        if not isinstance(this.type, ElementType):
            raise InterpreterError(message=f"Can't evaluate \"length\" on non-element object")
        self._last_result = Value(BaseType(Type.INT), len(this.value.value))

    def visit_push_function(self, element: 'PushFunctionDefinition'):
        variable = self._find_variable("_push")
        this = self._find_variable("_push_this")
        if not isinstance(this.type, ElementType):
            raise InterpreterError(message=f"Can't evaluate \"push\" on non-element object")
        if this.type.element_type != variable.type.type:
            raise InterpreterError(message=f"Types of object and push-element doesn't match")
        new_value = this.value.value
        new_value.append(variable.value.value)
        this.value.change_value(Value(this.type, new_value))

    def visit_pop_function(self, element: 'PopFunctionDefinition'):
        this = self._find_variable("_pop_this")
        if not isinstance(this.type, ElementType):
            raise InterpreterError(message=f"Can't evaluate \"pop\" on non-element object")
        value = this.value.value.pop()
        self._last_result = Value(BaseType(this.type.element_type), value)

    def visit_remove_function(self, element: 'RemoveFunctionDefinition'):
        this = self._find_variable("_remove_this")
        variable = self._find_variable("_remove")
        if not isinstance(this.type, KeyValueType):
            raise InterpreterError(message=f"Can't evaluate \"remove\" on non-key-value object")
        if variable.type.type != this.type.key_type:
            raise InterpreterError(message=f"Key type and object-key type doesn't match")
        if variable.value.value not in this.value.value.keys():
            raise InterpreterError(message=f"There is no object with key: {variable.value.value}")
        del this.value.value[variable.value.value]

    def visit_for_each_function(self, element: 'ForEachFunctionDefinition'):
        this = self._find_variable("_for_each_this")
        this_values = None
        this_type = None
        if isinstance(this.type, ElementType):
            this_values = this.value.value
            this_type = this.type.element_type
            if isinstance(this_type, Type):
                this_type = BaseType(this_type)
        elif isinstance(this.type, KeyValueType):
            this_values = [{key: value} for key, value in this.value.value.items()]
            this_type = KeyValueType(Type.PAIR, this.type.key_type, this.type.value_type)
        else:
            raise InterpreterError(message=f"For each function doesn't work with type: {this.type}")
        callback_function = self._last_function_call

        for value in this_values:
            argument_expression = LiteralExpression(this_type, value)
            callback_function.arguments = [argument_expression]
            callback_function.accept(self)

        self._last_function_call = None

    def visit_where_function(self, element: 'WhereFunctionDefinition'):
        this_values, this_type, callback_function = self._get_callback_data(element, "_where_this")

        result_values = list()

        for value in this_values:
            if isinstance(this_type, ElementType):
                argument_expression = LiteralExpression(this_type.element_type, value, Position(1, 1))
            elif this_type.type == Type.DICT:
                argument_expression = LiteralExpression(KeyValueType(Type.PAIR, this_type.key_type, this_type.value_type), value, Position(1, 1))
            callback_function.arguments = [argument_expression]
            callback_function.accept(self)
            result = self._last_result
            if result.type != BaseType(Type.BOOL):
                raise InterpreterError(f"{element.__class__.__name__} callback function must return bool")
            if result.value:
                result_values.append(value)

        if isinstance(this_type, KeyValueType):
            result_values = dict(result_values)

        self._last_result = Value(this_type, result_values)
        self._last_function_call = None

    def visit_select_function(self, element: 'SelectFunctionDefinition'):
        this_values, this_type, callback_function = self._get_callback_data(element, "_select_this")

        result_values = list()

        type = None

        function = self.find_function_definition(callback_function.id)

        for value in this_values:
            if isinstance(this_type, ElementType):
                argument_expression = LiteralExpression(this_type.element_type, value, Position(1, 1))
            elif this_type.type == Type.DICT:
                argument_expression = LiteralExpression(
                    KeyValueType(Type.PAIR, this_type.key_type, this_type.value_type), value, Position(1, 1))
            callback_function.arguments = [argument_expression]
            callback_function.accept(self)
            result = self._last_result
            result_values.append(result.value)

        if isinstance(function, FunctionDefinition):
            function_type = function.type
            if isinstance(function_type, KeyValueType):
                type = KeyValueType(Type.DICT, function_type.key_type, function_type.value_type)
                temp_result = dict()
                for pair in result_values:
                    key, value = pair
                    if key in temp_result:
                        raise InterpreterError(message=f"Key {key} already exists")
                    temp_result[key] = value
                result_values = temp_result
            else:
                type = ElementType(Type.LIST, function_type.type)
        else:
            raise InterpreterError(message=f"Can't execute function")

        self._last_result = Value(type, result_values)
        self._last_function_call = None

    def visit_orderby_function(self, element: 'OrderByFunctionDefinition'):
        this_values, this_type, callback_function = self._get_callback_data(element, "_orderby_this")

        result_values = list()

        type = None

        for value in this_values:
            if isinstance(this_type, ElementType):
                argument_expression = LiteralExpression(this_type.element_type, value, Position(1, 1))
            elif this_type.type == Type.DICT:
                argument_expression = LiteralExpression(
                    KeyValueType(Type.PAIR, this_type.key_type, this_type.value_type), value, Position(1, 1))
            callback_function.arguments = [argument_expression]
            callback_function.accept(self)
            result = self._last_result
            result_values.append({result.value: value})

        sorted_values = self._sort_dicts_by_key(result_values)

        def get_values_from_sorted_dicts(sorted_dicts):
            return [list(d.values())[0] for d in sorted_dicts]

        sorted_values = get_values_from_sorted_dicts(sorted_values)

        self._last_result = Value(this_type, sorted_values)
        self._last_function_call = None

    def _sort_dicts_by_key(self, dicts_list):
        def get_key(d):
            return next(iter(d.keys()))
        sorted_list = sorted(dicts_list, key=lambda d: (str(type(get_key(d))), get_key(d)))
        return sorted_list

    def _get_callback_data(self, element, variable_name: str):
        this = self._find_variable(variable_name)
        this_values = None
        this_type = None
        if isinstance(this.type, ElementType):
            this_values = this.value.value
            this_type = this.type
            if isinstance(this_type, Type):
                this_type = BaseType(this_type)
        elif isinstance(this.type, KeyValueType):
            this_values = [{key: value} for key, value in this.value.value.items()]
            this_type = this.type
        else:
            raise InterpreterError(message=f"For each function doesn't work with type: {this.type}")

        if self._last_function_call is not None:
            callback_function = self._last_function_call
        else:
            raise InterpreterError(message=f"{element.__class__.__name__} needs callback function")

        return this_values, this_type, callback_function

    def visit_expression_statement(self, element: 'ExpressionStatement'):
        element.expression.accept(self)

    def visit_assignment_statement(self, element: 'AssignmentStatement'):
        element.expression.accept(self)
        current_value = self._last_result
        element.assign_expression.accept(self)
        assign_value = self._last_result
        if isinstance(assign_value, Value) and assign_value.value is not None:
            current_value.change_value(assign_value)
        else:
            raise AssignmentError(message=f"Can't assign value to variable - it has null value")

    def visit_if_statement(self, element: 'IfStatement') -> None:
        if self._execute_condition_expression_and_block(element.if_part):
            return
        for part in element.else_if_parts:
            if self._execute_condition_expression_and_block(part):
                return
        if element.else_part is not None:
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

    def visit_casting_expression(self, element: 'CastingExpression') -> None:
        casting_type = element.type
        expression = self._get_expression_from_element(element)
        expression_type = expression.type
        if casting_type == expression_type:
            return
        elif casting_type == BaseType(Type.STRING):
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
        type = element.type
        if isinstance(element.type, Type):
            type = BaseType(element.type)
        self._last_result = Value(type, element.value)

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

            function_context, block_variables = FunctionContext(), BlockVariables()

            number_params = len(params)

            if number_params > 0 and isinstance(params[-1], ThisParameter):
                number_params -= 1
                this = self._last_result
                block_variables.add_variable(Variable(this.type, params[-1].id, this))

            if len(function_arguments) != number_params:
                raise InterpreterError(f"Number of arguments and parameters doesn't match")

            for i in range(0, len(function_arguments)):
                param_type, param_id = params[i].type, params[i].id
                if isinstance(params[i], FunctionParameter):
                    if isinstance(function_arguments[i], FunctionCallExpression):
                        self._last_function_call = function_arguments[i]
                    else:
                        raise InterpreterError(message=f"Function {function_name} requires function call as its parameter")
                else:
                    function_arguments[i].accept(self)
                    argument = self._last_result
                    param_type = self._define_types(param_type, argument.type)
                    if argument.type == param_type:
                        block_variables.add_variable(Variable(argument.type, param_id, argument))
                    else:
                        raise ExpressionTypeError(message=f"Param: {param_id} takes value type {param_type}, not {argument.type}")

            self._push_function_context(function_context)
            self._push_block_variables(block_variables)

            function_definition.accept(self)

            self._pop_block_variables()
            self._pop_function_context()
        else:
            raise InterpreterError(f"There is no function with id: {function_name}")

    def _define_types(self, param_type: 'BaseType', argument_type: 'BaseType') -> 'BaseType':
        if (isinstance(param_type, KeyValueType) and isinstance(argument_type, KeyValueType)
                and param_type.type == argument_type.type):
            if param_type.key_type == Type.UNKNOWN and param_type.value_type == Type.UNKNOWN:
                return argument_type
        elif (isinstance(param_type, ElementType) and isinstance(argument_type, ElementType)
              and param_type.type == argument_type.type):
            if param_type.element_type == Type.UNKNOWN:
                return argument_type
        elif isinstance(param_type, BaseType) and isinstance(argument_type, BaseType):
            if param_type.type == Type.UNKNOWN:
                return argument_type
        elif param_type == Type.UNKNOWN:
            return argument_type
        return param_type

    def visit_field_access_expression(self, element: 'FieldAccessExpression'):
        pass

    def visit_method_call_expression(self, element: 'MethodCallExpression'):
        id = element.id
        arguments = element.arguments
        function_call_expression = FunctionCallExpression(id, arguments)
        function_call_expression.accept(self)

    def visit_method_call_and_field_access_expression(self, element: 'MethodCallAndFieldAccessExpression'):
        id = element.id
        arguments = element.arguments
        function_call_expression = FunctionCallExpression(id, arguments)
        function_call_expression.accept(self)
        result = self._last_result
        element.index.accept(self)
        index = self._last_result
        self._evaluate_index(result.type, result, index)

    def visit_index_access_expression(self, element: 'IndexAccessExpression'):
        key = element.id
        if variable := self._find_variable(key):
            element.index.accept(self)
            index = self._last_result
            self._evaluate_index(variable.type, variable.value, index)
        else:
            raise InterpreterError(message=f"Can't find variable with id: {key}")

    def visit_function_call_and_index_expression(self, element: 'FunctionCallAndIndexExpression'):
        function_call = FunctionCallExpression(element.id, element.arguments, element.position)
        function_call.accept(self)
        function_result = self._last_result
        element.index.accept(self)
        index_result = self._last_result
        self._evaluate_index(function_result.type, function_result, index_result)

    def _evaluate_index(self, type: 'BaseType', value: 'Value', index: 'Value'):
        if isinstance(type, ElementType):
            if index.type != BaseType(Type.INT):
                raise InterpreterError(message=f"Index for element-type object must be int type")
            if len(value.value) < index.value:
                raise InterpreterError(message=f"Index out of range")
            self._last_result = Value(BaseType(type.element_type), value.value[index.value])
        elif isinstance(type, KeyValueType):
            if index.type.type != type.key_type:
                raise InterpreterError(message=f"Index for key-value-type object must be string type")
            if index.value not in value.value.keys():
                raise InterpreterError(message=f"No object with key: {index.value}")
            self._last_result = Value(BaseType(type.value_type), value.value[index.value])

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
        arguments[1].accept(self)
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
            key = next(iter(result.value.keys()))
            value = result.value[key]
            if key in dictionary.keys():
                raise InterpreterError(message=f"Can't add {key} to Dict - already has this key")
            dictionary[key] = value
        return Value(type, dictionary)

    def visit_or_expression(self, element: 'OrExpression') -> None:
        element.left.accept(self)
        if (left := self._last_result).type != BaseType(Type.BOOL):
            raise InterpreterError(message="Can't evaluate or expression with non-bool types", position=element.position)
        if not left.value:
            element.right.accept(self)
            if self._last_result.type != BaseType(Type.BOOL):
                raise InterpreterError(message="Can't evaluate or expression with non-bool types", position=element.position)

    def visit_and_expression(self, element: 'AndExpression') -> None:
        element.left.accept(self)
        if (left := self._last_result).type != BaseType(Type.BOOL):
            raise InterpreterError(message="Can't evaluate AND expression with non-bool types", position=element.position)
        if left.value:
            element.right.accept(self)
            if self._last_result.type != BaseType(Type.BOOL):
                raise InterpreterError(message="Can't evaluate or expression with non-bool types", position=element.position)

    def visit_greater_expression(self, element: 'GreaterExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} <= {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(BaseType(Type.BOOL), left.value > right.value)
        else:
            raise ExpressionTypeError(message=f"Can't evaluate greater expression between objects type: {left.type} and {right.type}",
                                   position=element.position)

    def visit_less_expression(self, element: 'LessExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} <= {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(BaseType(Type.BOOL), left.value < right.value)
        else:
            raise ExpressionTypeError(message=f"Cannot evaluate less expression between objects type: {left.type} and {right.type}",
                                      position=element.position)

    def visit_greater_equal_expression(self, element: 'GreaterEqualExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} <= {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(BaseType(Type.BOOL), left.value >= right.value)
        else:
            raise ExpressionTypeError(message=f"Cannot evaluate greater-equal expression between objects type: {left.type}"
                                           f" and {right.type}", position=element.position)

    def visit_less_equal_expression(self, element: 'LessEqualExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} <= {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(BaseType(Type.BOOL), left.value <= right.value)
        else:
            raise ExpressionTypeError(message=f"Cannot evaluate less-equal expression between objects type: {left.type} and {right.type}", position=element.position)

    def visit_equal_expression(self, element: 'EqualExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {BaseType(Type.INT), BaseType(Type.FLOAT)} or left.type == right.type:
            self._last_result = Value(BaseType(Type.BOOL), left.value == right.value)
        else:
            raise ExpressionTypeError(message=f"Cannot evaluate equal expression between objects type: {left.type} and {right.type}", position=element.position)

    def visit_not_equal_expression(self, element: 'NotEqualExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {BaseType(Type.INT), BaseType(Type.FLOAT)} or left.type == right.type:
            self._last_result = Value(BaseType(Type.BOOL), left.value != right.value)
        else:
            raise ExpressionTypeError(message=f"Cannot evaluate not equal expression between objects type: {left.type} and {right.type}", position=element.position)

    def visit_multiplication_expression(self, element: 'MultiplicationExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {BaseType(Type.INT), BaseType(Type.STRING)}:
            self._last_result = Value(BaseType(Type.STRING), left.value * right.value)
        elif {left.type, right.type} == {BaseType(Type.INT), BaseType(Type.FLOAT)} or left.type == right.type == BaseType(Type.FLOAT):
            self._last_result = Value(BaseType(Type.FLOAT), left.value * right.value)
        elif left.type == right.type == BaseType(Type.INT):
            self._last_result = Value(BaseType(Type.INT), left.value * right.value)
        else:
            raise ExpressionTypeError(message=f"Cannot evaluate multiplication expression between objects type: {left.type}"
                                   f" and {right.type}", position=element.position)

    def visit_division_expression(self, element: 'DivisionExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {BaseType(Type.INT), BaseType(Type.FLOAT)} or left.type == right.type and right.type in {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            if right.value == 0:
                raise DivisionError(message="Can't divide by zero", position=element.position)
            self._last_result = Value(BaseType(Type.FLOAT), left.value / right.value)
        else:
            raise ExpressionTypeError(message=f"Cannot evaluate division expression between objects type: {left.type} and {right.type}", position=element.position)

    def visit_addition_expression(self, element: 'AdditionExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {BaseType(Type.INT), BaseType(Type.FLOAT)} or left.type == right.type == BaseType(
                Type.FLOAT):
            self._last_result = Value(BaseType(Type.FLOAT), left.value + right.value)
        elif left.type == right.type and left.type in {BaseType(Type.INT), BaseType(Type.STRING)}:
            self._last_result = Value(left.type, left.value + right.value)
        else:
            raise ExpressionTypeError(message=f"Cannot evaluate addition expression between objects type: {left.type} and {right.type}", position=element.position)

    def visit_subtraction_expression(self, element: 'SubtractionExpression') -> None:
        left, right = self._get_left_and_right_element(element)
        if {left.type, right.type} == {BaseType(Type.INT), BaseType(Type.FLOAT)} or left.type == right.type == BaseType(
                Type.FLOAT):
            self._last_result = Value(BaseType(Type.FLOAT), left.value - right.value)
        elif left.type == right.type == BaseType(Type.INT):
            self._last_result = Value(BaseType(Type.INT), left.value - right.value)
        else:
            raise ExpressionTypeError(message=f"Cannot evaluate subtraction expression between objects type: {left.type}"
                                   f" and {right.type}", position=element.position)

    def visit_dot_call_expression(self, element: 'DotCallExpression') -> None:
        element.left.accept(self)
        element.right.accept(self)

    def visit_negation_expression(self, element: 'NegationExpression') -> None:
        expression = self._get_expression_from_element(element)
        if expression.type == BaseType(Type.BOOL):
            self._last_result = Value(BaseType(Type.BOOL), not expression.value)
        else:
            raise ExpressionTypeError(f"Cannot evaluate negation expression with object type: {expression.type}")

    def visit_unary_subtraction_expression(self, element: 'UnarySubtractionExpression') -> None:
        expression = self._get_expression_from_element(element)
        if expression.type in {BaseType(Type.INT), BaseType(Type.FLOAT)}:
            self._last_result = Value(expression.type, -expression.value)
        else:
            raise ExpressionTypeError(f"Cannot evaluate unary subtraction expression with object type: {expression.type}")

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
            raise InitializationError(message=f"Can't assign value type: {value.type} to variable type: {type}", position=element.position)

    def visit_declaration_statement(self, element: 'DeclarationStatement'):
        type, id = element.type, element.id
        variable = Variable(type, id, Value(type, None))
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
            raise ReturnTypeError(message=f"Function {element.name} should return value type: {element.type},"
                                           f" not {result.type}")

        self._was_return = False

    def visit_program(self, element: 'Program'):
        functions = self._functions_definition
        if "main" not in functions.keys():
            raise MainNotImplementedError(message="Main function must be implemented")
        main = FunctionCallExpression(id="main", arguments=[], position=Position(1, 1))
        main.accept(self)
        result = self._last_result
        print(f"Program exited with value: {result.value} ({result.type})\n")


def main(input_source):
    from io import StringIO
    from src.scanner.scanner import Scanner
    from src.lexer.lexer import Lexer
    from src.filter.filter import Filter
    from src.parser.parser import Parser
    if input_source == '-':
        text = StringIO(input("Enter code: "))
    else:
        with open(input_source, 'r') as file:
            text = StringIO(file.read())

    scanner = Scanner(text)
    lexer = Lexer(scanner)
    filter = Filter(lexer)
    parser = Parser(filter)
    program = parser.parse_program()
    interpreter = Interpreter(program)
    interpreter.interpret()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for a custom language.")
    parser.add_argument('source', type=str, help='Path to the source file or "-" to read from stdin')

    args = parser.parse_args()
    main(args.source)