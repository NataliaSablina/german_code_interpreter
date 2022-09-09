import pytest
from tokens import *


def test_token_str():
    assert str(Token(PLUS, "+", 1, 0)) == "Token(PLUS, +) on position 1:0"


def test_token_eq_error():
    with pytest.raises(TypeError):
        Token(PLUS, "+", 1, 0) == "Token(PLUS, +) on position 1:0"


def test_token_nq_error():
    with pytest.raises(TypeError):
        Token(PLUS, "+", 1, 0) != "Token(PLUS, +) on position 1:0"


def test_eq_return_false():
    assert (Token(PLUS, "+", 1, 0) == Token(PLUS, "+", 1, 1)) == False


def test_nq_return_true():
    assert Token(PLUS, "+", 1, 0) != Token(PLUS, "+", 1, 1)
