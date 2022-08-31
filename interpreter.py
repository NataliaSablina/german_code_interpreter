from semantic_analyzer import *


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.MEMORY = {}

    def visit_Program(self, node):
        print('visit_Program')
        self.visit(node.compound_statement)

    def visit_Compound(self, node):
        print('visit_Compound')
        for child in node.children:
            print(child)
            if isinstance(child, list):
                for decl in child:
                    self.visit(decl)
            else:
                self.visit(child)

    def visit_BinOp(self, node):
        print('visit_BinOp')
        if node.op.token_type == PLUS:
            # print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', node.left.value)
            return self.visit(node.left) + self.visit(node.right)
        if node.op.token_type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.token_type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.token_type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def UnaryOp(self, node):
        print('UnaryOp')
        if node.op.token_type == MINUS:
            return -self.visit(node.expr)
        if node.op.token_type == PLUS:
            return self.visit(node.expr)

    def visit_Num(self, node):
        print('visit_Num')
        return node.value

    def visit_VarAssignDecl(self, node):
        print('visit_VarAssignDecl')
        self.MEMORY[node.var_name] = node.value
        return node.value

    def visit_Assign(self, node):
        print('visit_Assign')
        var_name = node.left.value
        var_value = self.visit(node.right)
        self.MEMORY[var_name] = var_value

    def visit_Var(self, node):
        print('visit_Var')
        var_name = node.value
        print(var_name)
        var_value = self.MEMORY.get(var_name)
        print('99999999999999999999')
        print(var_value)
        return var_value

    def visit_VarDecl(self, node):
        print('visit_VarDecl')

    def visit_Type(self, node):
        print('visit_Type')

    def visit_NoOp(self, node):
        print('visit_NoOp')

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)
