import pytest
from lexer import *
from parser import *


def test_parser_node_program():
    with open("G-code/test_code/test_code1", "r+", encoding="utf-8") as f:
        code = f.read()
    lexer = Lexer(code)
    parser = Parser(lexer)
    tree = parser.parse()
    assert type(tree).__name__ == "Program"
