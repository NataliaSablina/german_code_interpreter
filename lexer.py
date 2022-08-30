from errors import *
from token import *


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.column = 1

    def error(self):
        s = "Lexer error on '{lexeme}' line: {line} column: {column}".format(
            lexeme=self.current_char,
            line=self.line,
            column=self.column,
        )
        raise LexerError(message=s)

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0

        self.pos += 1
        if self.pos > len(self.text) + 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

    def skip_whitespace(self):
        if self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(FLOAT, float(result))
        else:
            return Token(INTEGER, int(result))

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '+')

            if self.current_char == '{':
                self.advance()
                return Token(LBRAKET, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRAKET, '}')

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self._id()

            self.error()
            return Token(EOF, None)
