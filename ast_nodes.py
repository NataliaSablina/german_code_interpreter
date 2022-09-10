class AST:
    pass


class Program(AST):
    def __init__(self, name, declarations, compound_statement):
        self.name = name
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


class VarAssignDecl(VarDecl):
    def __init__(self, var_name, type_name, right_var):
        super().__init__(var_name, type_name)
        self.value = right_var


# class ProcDecl(AST):
#     def __init__(self, proc_name, params, block):
#         self.proc_name = proc_name
#         self.params = params
#         self.block = block


class CallableDecl(AST):
    def __init__(self, call_name, params, block):
        self.call_name = call_name
        self.params = params
        self.block = block


class Return(AST):
    def __init__(self, token, expr):
        self.token = token
        self.expr = expr


class CallableCall(AST):
    def __init__(self, call_name, actual_params, token):
        self.call_name = call_name
        self.actual_params = actual_params
        self.token = token
        self.call_symbol = None


# class FunctionDecl(AST):
#     def __init__(self, func_name, params, block):
#         self.func_name = func_name
#         self.params = params
#         self.block = block
