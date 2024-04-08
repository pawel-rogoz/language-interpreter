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
        assert scanner.get_position() == Position(2, 1)

    def test_position_after_eof(self):
        text = StringIO("")
        scanner = Scanner(text)
        assert scanner.get_position() == Position(1, 0)

    def test_position_after_one_char(self):
        text = StringIO("a")
        scanner = Scanner(text)
        assert scanner.get_position() == Position(1, 1)

    def test_position_after_char_and_newline(self):
        text = StringIO("a\n")
        scanner = Scanner(text)
        scanner.next_char()
        assert scanner.get_position() == Position(2, 1)