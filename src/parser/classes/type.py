from abc import ABC, abstractmethod


class Type:
    def __init__(self, type):
        self._type = type

    @property
    def type(self):
        return self._type


class FunctionType(Type):
    pass


class KeyValueType(Type):
    def __init__(self, type, key_type, value_type):
        super().__init__(type)
        self._key_type = key_type
        self._value_type = value_type

    @property
    def key_type(self):
        return self._key_type

    @property
    def value_type(self):
        return self._value_type


class ValueType(Type):
    def __init__(self, type, value_type):
        super().__init__(type)
        self._value_type = value_type

    @property
    def value_type(self):
        return self._value_type


# class PairType(KeyValueType):
#     pass
#
#
# class DictType(KeyValueType):
#     pass
#
#
# class ListType(ValueType):
#     pass
#
#
# class IntType(Type):
#     pass
#
#
# class FloatType(Type):
#     pass
#
#
# class StringType(Type):
#     pass
#
#
# class BoolType(Type):
#     pass
#
#
# class VoidType(Type):
#     pass