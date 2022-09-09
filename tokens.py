INTEGER = "INTEGER"
FLOAT = "FLOAT"
EOF = "EOF"
ASSIGN = "ASSIGN"
PLUS = "PLUS"
MINUS = "MINUS"
DOT = "DOT"
FLOAT_DIV = "FLOAT_DIV"
MUL = "MUL"
LBRAKET = "LBRAKET"
RBRAKET = "RBRAKET"
SEMI = "SEMI"
MAIN = "MAIN"
ID = "ID"
INTEGER_TYPE = "INTEGER_TYPE"
FLOAT_TYPE = "FLOAT_TYPE"
COMMA = "COMMA"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
RETURN = "RETURN"
FUNCTION = "FUNCTION"
PROCEDURE = "PROCEDURE"


class Token:
    def __init__(self, token_type, value, line=None, column=None):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token({self.token_type}, {self.value}) on position {self.line}:{self.column}"

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Token):
            raise TypeError("Instance must be instance of class Token")
        if (
            self.token_type == other.token_type
            and self.value == other.value
            and self.line == other.line
            and self.column == other.column
        ):
            return True
        else:
            return False

    def __ne__(self, other):
        if not isinstance(other, Token):
            raise TypeError("Instance must be instance of class Token")
        return not self.__eq__(other)


RESERVED_KEYWORDS = {
    "AUSFÜHRUNG": Token(MAIN, "ausführung"),
    "INT": Token(INTEGER_TYPE, "INTEGER_TYPE"),
    "FLOAT": Token(FLOAT_TYPE, "FLOAT_TYPE"),
    "RÜCKKEHR": Token(RETURN, "RETURN"),
    "FUNKTION": Token(FUNCTION, "FUNCTION"),
    "PROZEDURE": Token(PROCEDURE, "PROCEDURE"),
}
