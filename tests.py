from unittest import TestCase
from lexer import *


class InterpreterTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        lexer1 = Lexer("1+2+3+4+5")

    def test_lexer_numbers(self):
        pass
        # self.assertEqual(Token(INTEGER, 1, 1, 1), lexer1.get_next_token())
