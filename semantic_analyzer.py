from parser import *


class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type
        self.scope_level = 0


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type,
        )

    __repr__ = __str__


class BuiltInSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


class CallableSymbol(Symbol):
    def __init__(self, name, params=None):
        super().__init__(name)
        self.params = params if params is not None else []
        self.block_ast = None
        self.return_node = Num(Token(INTEGER, 0))

    def __str__(self):
        return "<{class_name}(name={name}, parameters={params})>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params,
        )

    __repr__ = __str__


class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope

    def __str__(self):
        h1 = "SCOPE (SCOPED SYMBOL TABLE)"
        lines = ["\n", h1, "=" * len(h1)]
        for header_name, header_value in (
            ("Scope name", self.scope_name),
            ("Scope level", self.scope_level),
            (
                "Enclosing scope",
                self.enclosing_scope.scope_name if self.enclosing_scope else None,
            ),
        ):
            lines.append("%-15s: %s" % (header_name, header_value))
        h2 = "Scope (Scoped symbol table) contents"
        lines.extend([h2, "-" * len(h2)])
        lines.extend(("%7s: %r" % (key, value)) for key, value in self._symbols.items())
        lines.append("\n")
        s = "\n".join(lines)
        return s

    __repr__ = __str__

    def _init_builtins(self):
        self.insert(BuiltInSymbol("INTEGER_TYPE"))
        self.insert(BuiltInSymbol("FLOAT_TYPE"))

    def insert(self, symbol):
        print(f"Insert symbol {symbol.name}")
        symbol.scope_level = self.scope_level
        self._symbols[symbol.name] = symbol

    def lookup(self, name, only_current_scope=False):
        print(f"LookUp for symbol {name}")
        symbol = self._symbols.get(name)
        if symbol is not None:
            return symbol
        if only_current_scope:
            return None
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.error_visit)
        return visitor(node)

    def error_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None

    def visit_Program(self, node):
        print("visit_Program")
        print("Enter scope: global")
        global_scope = ScopedSymbolTable(
            scope_name="global", scope_level=1, enclosing_scope=self.current_scope
        )
        global_scope._init_builtins()
        self.current_scope = global_scope
        for decl in node.declarations:
            self.visit(decl)
        self.visit(node.compound_statement)
        print(global_scope)
        self.current_scope = global_scope.enclosing_scope
        print("Leave scope: global")

    def visit_CallableDecl(self, node):
        print("visit_CallableDecl")
        call_name = node.call_name
        call_symbol = CallableSymbol(call_name)
        self.current_scope.insert(call_symbol)

        print("ENTER scope: ", call_name)
        procedure_scope = ScopedSymbolTable(
            scope_name=call_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope,
        )
        self.current_scope = procedure_scope

        for param in node.params:
            param_type = self.current_scope.lookup(param.type_name.value)
            param_name = param.var_name.value
            var_symbol = VarSymbol(param_name, param_type)
            self.current_scope.insert(var_symbol)
            call_symbol.params.append(var_symbol)

        for block in node.block:
            if isinstance(block, list):
                for i in block:
                    if isinstance(i, Return):
                        call_symbol.return_node = i
                        self.visit(i)
                        block.remove(i)
                        continue
                    self.visit(i)
            else:
                if isinstance(block, Return):
                    call_symbol.return_node = block
                    self.visit(block)
                    node.block.remove(block)
                    continue
                self.visit(block)
        print(procedure_scope)
        self.current_scope = self.current_scope.enclosing_scope
        print("LEAVE scope: %s" % call_name)
        call_symbol.block_ast = node.block

    def visit_Return(self, node):
        print('visit_Return')
        self.visit(node.value)

    def visit_Compound(self, node):
        print("visit_Compound")
        print("Enter scope: Ausf??hrung")
        main_scope = ScopedSymbolTable(
            scope_name="Ausf??hrung", scope_level=2, enclosing_scope=self.current_scope
        )
        self.current_scope = main_scope
        for child in node.children:
            if isinstance(child, list):
                for decl in child:
                    self.visit(decl)
            else:
                self.visit(child)
        print(main_scope)
        self.current_scope = self.current_scope.enclosing_scope
        print("Leave Ausf??hrung scope")

    def visit_VarDecl(self, node):
        print("visit_VarDecl")
        type_name = node.type_name.value
        type_symbol = self.current_scope.lookup(type_name)
        var_name = node.var_name.value
        var_symbol = VarSymbol(var_name, type_symbol)

        if self.current_scope.lookup(var_name, only_current_scope=True):
            raise Exception("Error: Duplicate identifier '%s' found" % var_name)

        self.current_scope.insert(var_symbol)

    def visit_Var(self, node):
        print("visit_Var")
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise Exception("Error: Symbol(identifier) not found '%s'" % var_name)

    def visit_BinOp(self, node):
        print("visit_BinOp")
        self.visit(node.left)
        self.visit(node.right)

    def visit_Assign(self, node):
        print("visit_Assign")
        self.visit(node.right)
        print(node.left)
        self.visit(node.left)

    def visit_NoOp(self, node):
        print("visit_NoOp")
        pass

    def visit_Num(self, node):
        print("visit_Num")
        pass

    def visit_VarAssignDecl(self, node):
        print("visit_VarAssignDecl")
        print(node.type_name)
        type_name = node.type_name.value
        print(type_name)
        type_symbol = self.current_scope.lookup(type_name)
        var_name = node.var_name
        var_symbol = VarSymbol(var_name, type_symbol)

        if self.current_scope.lookup(var_name, only_current_scope=True):
            raise Exception("Error: Duplicate identifier '%s' found" % var_name)

        self.current_scope.insert(var_symbol)

    def visit_CallableCall(self, node):
        print('visit_CallableCall')
        for param_node in node.actual_params:
            self.visit(param_node)

        call_symbol = self.current_scope.lookup(node.call_name)
        node.call_symbol = call_symbol

    def visit_UnaryOp(self, node):
        self.visit(node.value)
