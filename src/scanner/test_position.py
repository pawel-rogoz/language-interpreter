from src.scanner.position import Position

import pytest


class TestInit:
    def test_column_init_value(self):
        position = Position()
        assert position.column == 0

    def test_line_init_value(self):
        position = Position()
        assert position.line == 1


class TestNextLine:
    def test_line(self):
        position = Position()
        new_position = position.next_line()
        assert new_position.line == 2

    def test_column(self):
        position = Position()
        new_position = position.next_line()
        assert new_position.column == 0

    def test_column_value_back_to_one(self):
        position = Position()
        new_position = position.next_column()
        new_position = new_position.next_line()
        assert new_position.column == 0


class TestNextColumn:
    def test_line(self):
        position = Position()
        new_position = position.next_column()
        assert new_position.line == 1

    def test_column(self):
        position = Position()
        new_position = position.next_column()
        assert new_position.column == 1
