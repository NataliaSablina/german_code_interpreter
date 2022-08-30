class AST:
    pass


class Program(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class Compound(AST):
    def __init__(self):
        self.children = []


class VarDecl(AST):
    def __init__(self, var_name, type_name):
        self.var_name = var_name
        self.type_name = type_name


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

