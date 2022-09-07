from semantic_analyzer import *
from call_stack import *


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.call_stack = CallStack()

    def visit_Program(self, node):
        print("visit_Program")
        prog_name = node.name
        ar = ActivationRecord(
            name=prog_name,
            type=ARType.PROGRAM,
            nesting_level=1
        )
        self.call_stack.push(ar)
        print(str(self.call_stack))
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)
        print(f'LEAVE: PROGRAM {prog_name}')
        print(str(self.call_stack))
        self.call_stack.pop()


    def visit_Compound(self, node):
        print("visit_Compound")
        for child in node.children:
            print(child)
            if isinstance(child, list):
                for decl in child:
                    self.visit(decl)
            else:
                self.visit(child)

    def visit_BinOp(self, node):
        print("visit_BinOp")
        if node.op.token_type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.token_type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.token_type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.token_type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_UnaryOp(self, node):
        print("UnaryOp")
        if node.op.token_type == MINUS:
            return -self.visit(node.expr)
        if node.op.token_type == PLUS:
            return self.visit(node.expr)

    def visit_Num(self, node):
        print("visit_Num")
        return node.value

    def visit_VarAssignDecl(self, node):
        print("visit_VarAssignDecl")
        value = self.visit(node.value)
        ar = self.call_stack.peek()
        ar[node.var_name] = value
        return value

    def visit_Assign(self, node):
        print("visit_Assign")
        var_name = node.left.value
        var_value = self.visit(node.right)
        ar = self.call_stack.peek()
        ar[var_name] = var_value


    def visit_Var(self, node):
        print("visit_Var")
        var_name = node.value
        ar = self.call_stack.peek()
        var_value = ar.get(var_name)
        return var_value

    def visit_VarDecl(self, node):
        print("visit_VarDecl")

    def visit_Type(self, node):
        print("visit_Type")

    def visit_NoOp(self, node):
        print("visit_NoOp")

    def visit_ProcDecl(self, node):
        print("visit_ProcDecl")
        # for param in node.params:
        #     value = self.visit(param.value)
        #     self.MEMORY[param.var_name] = value

    def visit_ProcedureCall(self, node):
        print("visit_ProcedureCall")
        pass

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ""
        return self.visit(tree)
