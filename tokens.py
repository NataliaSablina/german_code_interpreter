INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
EOF = 'EOF'
ASSIGN = 'ASSIGN'
PLUS = 'PLUS'
MINUS = 'MINUS'
DOT = 'DOT'
FLOAT_DIV = 'FLOAT_DIV'
MUL = 'MUL'
LBRAKET = 'LBRAKET'
RBRAKET = 'RBRAKET'
SEMI = 'SEMI'
MAIN = 'MAIN'
ID = 'ID'
INTEGER_TYPE = 'INTEGER_TYPE'
FLOAT_TYPE = 'FLOAT_TYPE'
COMMA = 'COMMA'


class Token:
    def __init__(self, token_type, value, line=None, column=None):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token({self.token_type}, {self.value}) on position {self.line}:{self.column}"

    __repr__ = __str__


RESERVED_KEYWORDS = {
    'AUSFUHRUNG': Token(MAIN, 'MAIN'),
    'INT': Token(INTEGER_TYPE, 'INTEGER_TYPE'),
    'FLOAT': Token(FLOAT_TYPE, 'FLOAT_TYPE'),
}
