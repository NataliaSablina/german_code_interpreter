import pytest

from errors import LexerError, ErrorCode
from tokens import *


def test_error_str():
    lexer_error = LexerError(
        error_code=ErrorCode.UNEXPECTED_TOKEN,
        token=Token(PLUS, "+", 1, 0),
        message="wrong token",
    )
    assert str(lexer_error) == "LexerError: wrong token"
