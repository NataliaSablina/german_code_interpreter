from errors import *
from tokens import *


class Lexer:
    def __init__(self, text):
        print("lexer")
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.column = 0

    def error(self):
        s = "Lexer error on '{lexeme}' line: {line} column: {column}".format(
            lexeme=self.current_char,
            line=self.line,
            column=self.column,
        )
        raise LexerError(message=s)

    def advance(self):
        print('advance')
        if self.current_char == "\n":
            self.line += 1
            self.column = 0

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

    def skip_whitespace(self):
        print('skip_whitespace')
        if self.current_char is not None and self.current_char.isspace():
            self.advance()

    def while_whitespace(self):
        print('while_whitespace')
        while self.current_char is not None and self.current_char.isspace():
            self.skip_whitespace()
        return self.current_char

    def number(self):
        print("number")
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == ".":
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(FLOAT, float(result), self.line, self.column)
        else:
            return Token(INTEGER, int(result), self.line, self.column)

    def _id(self):
        print("_id")
        result = ""
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(
            result.upper(), Token(ID, result, self.line, self.column)
        )
        return token

    def get_next_token(self):
        print("get_next_token")
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+", self.line, self.column)

            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-", self.line, self.column)

            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*", self.line, self.column)

            if self.current_char == "/":
                self.advance()
                return Token(FLOAT_DIV, "/", self.line, self.column)

            if self.current_char == ".":
                self.advance()
                return Token(DOT, ".", self.line, self.column)

            if self.current_char == "{":
                self.advance()
                return Token(LBRAKET, "{", self.line, self.column)

            if self.current_char == "}":
                self.advance()
                return Token(RBRAKET, "}", self.line, self.column)
            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(", self.line, self.column)

            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")", self.line, self.column)

            if self.current_char == "=":
                self.advance()
                return Token(ASSIGN, "=", self.line, self.column)

            if self.current_char == ";":
                self.advance()
                return Token(SEMI, ";", self.line, self.column)

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == ",":
                self.advance()
                return Token(COMMA, ",", self.line, self.column)

            self.error()
        return Token(EOF, None, self.line, self.column)
