from semantic_analyzer import *
from call_stack import *


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.call_stack = CallStack()

    def visit_Program(self, node):
        print("visit_Program")
        prog_name = node.name
        ar = ActivationRecord(name=prog_name, type=ARType.PROGRAM, nesting_level=1)
        print(f"ENTER: PROGRAM {prog_name}")
        self.call_stack.push(ar)
        print(str(self.call_stack))
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)
        print(f"LEAVE: PROGRAM {prog_name}")
        print(str(self.call_stack))
        self.call_stack.pop()

    def visit_Compound(self, node):
        print("visit_Compound")
        for child in node.children:
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
        print("visit_UnaryOp")
        if node.op.token_type == MINUS:
            return -self.visit(node.value)
        if node.op.token_type == PLUS:
            return self.visit(node.value)

    def visit_Num(self, node):
        print("visit_Num")
        print(node.value)
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

    def visit_CallableDecl(self, node):
        print("visit_ProcDecl")

    def visit_CallableCall(self, node):
        print("visit_CallableCall")
        call_name = node.call_name
        call_symbol = node.call_symbol
        ar = ActivationRecord(
            name=call_name,
            nesting_level=call_symbol.scope_level + 1,
            type=ARType.PROCEDURE,
        )
        call_symbol = node.call_symbol
        formal_params = call_symbol.params
        actual_params = node.actual_params
        for formal_param, param_arg in zip(formal_params, actual_params):
            result = self.visit(param_arg)
            ar[formal_param.name] = result
            if formal_param.type != param_arg.token.token_type:
                if str(formal_param.type) == "FLOAT_TYPE" and isinstance(result, float):
                    continue
                elif str(formal_param.type) == "INTEGER_TYPE" and isinstance(
                    result, int
                ):
                    continue
                else:
                    raise ValueError(
                        "formal param type and actual param type must be the same"
                    )
            else:
                continue

        self.call_stack.push(ar)
        print(f"ENTER: PROCEDURE {call_name}")
        print(str(self.call_stack))
        for el in call_symbol.block_ast:
            if isinstance(el, list):
                for block in el:
                    self.visit(block)
            else:
                self.visit(el)
        print(f"LEAVE: PROCEDURE {call_name}")
        print(str(self.call_stack))
        result = self.visit(node.call_symbol.return_node)

        self.call_stack.pop()
        return result

    def visit_Return(self, node):
        print("visit_Return")
        result = self.visit(node.value)
        return result

    def interpret(self):
        print("visit_interpret")
        tree = self.tree
        if tree is None:
            return ""
        return self.visit(tree)
