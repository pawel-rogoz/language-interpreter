from src.scanner.scanner import Scanner
from src.scanner.position import Position

import pytest
from io import StringIO


class TestGetChar:
    def test_eof(self):
        text = StringIO("")
        scanner = Scanner(text)
        assert scanner.get_char() == "EOF"

    def test_newline(self):
        text = StringIO("\n")
        scanner = Scanner(text)
        assert scanner.get_char() == "\n"

    def test_multiple_chars(self):
        chars = ['a', 'b', 'c']
        text = StringIO(''.join(chars))
        scanner = Scanner(text)
        scanner_chars = []
        while (char := scanner.get_char()) != "EOF":
            scanner_chars.append(char)
            scanner.next_char()

        assert chars == scanner_chars

    def test_more_next_chars_than_chars(self):
        text = StringIO("a")
        scanner = Scanner(text)
        scanner.next_char()
        scanner.next_char()
        scanner.next_char()
        assert scanner.get_char() == "EOF"

    def test_escape_characters(self):
        text = StringIO("\t")
        scanner = Scanner(text)
        assert scanner.get_char() == "\t"


class TestPosition:
    def test_position_after_newline(self):
        text = StringIO("\n")
        scanner = Scanner(text)
        assert scanner.get_position() == Position(2, 0)

    def test_position_after_eof(self):
        text = StringIO("")
        scanner = Scanner(text)
        assert scanner.get_position() == Position(1, 1)

    def test_position_after_one_char(self):
        text = StringIO("a")
        scanner = Scanner(text)
        assert scanner.get_position() == Position(1, 1)

    def test_position_after_char_and_newline(self):
        text = StringIO("a\n")
        scanner = Scanner(text)
        scanner.next_char()
        assert scanner.get_position() == Position(2, 0)

    def test_char_after_windows_newline(self):
        text = StringIO("\r\na")
        scanner = Scanner(text)
        assert scanner.current_char == "\n"

    def test_position_with_newlines(self):
        text = StringIO("a\nb\nc")
        scanner = Scanner(text)
        positions = list()
        while True:
            positions.append(scanner.get_position())
            if scanner.current_char == 'EOF':
                break
            scanner.next_char()
        assert positions == [Position(1, 1), Position(2, 0), Position(2, 1), Position(3, 0), Position(3, 1), Position(3, 2)]

    def test_position_multiple_in_one_line(self):
        text = StringIO("a b c")
        scanner = Scanner(text)
        positions = list()
        while True:
            if scanner.current_char.isspace():
                scanner.next_char()
                continue
            positions.append(scanner.get_position())
            if scanner.current_char == 'EOF':
                break
            scanner.next_char()
        assert positions == [Position(1, 1), Position(1, 3), Position(1, 5), Position(1, 6)]

    def test_position_eof(self):
        text = StringIO("")
        scanner = Scanner(text)
        assert scanner.get_position() == Position(1, 1)
        assert scanner.get_char() == 'EOF'

    def test_position_of_eof(self):
        text = StringIO("a")
        scanner = Scanner(text)
        scanner.next_char()
        assert scanner.get_position() == Position(1, 2)
        assert scanner.get_char() == 'EOF'


class TestEscapeCharacters:
    def test_newline(self):
        text = StringIO("\n")
        scanner = Scanner(text)
        assert scanner.current_char == "\n"

    def test_apostrophe(self):
        text = StringIO("\'")
        scanner = Scanner(text)
        assert scanner.current_char == "\'"

    def test_quotation_mark(self):
        text = StringIO("\"")
        scanner = Scanner(text)
        assert scanner.current_char == "\""

    def test_tab(self):
        text = StringIO("\t")
        scanner = Scanner(text)
        assert scanner.current_char == "\t"

    def test_carriage_return(self):
        text = StringIO("\r")
        scanner = Scanner(text)
        assert scanner.current_char == "\r"

    def test_backslash(self):
        text = StringIO("\\")
        scanner = Scanner(text)
        assert scanner.current_char == "\\"
