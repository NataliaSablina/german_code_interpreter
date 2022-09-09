import pytest

from lexer import Lexer
from tokens import *


def test_lexer():
    lexer = Lexer("+")
    result = lexer.get_next_token()
    assert result == Token(PLUS, "+", 1, 0)
