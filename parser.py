from lexer import *
from ast_nodes import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, error_code, token, message):
        s = f'{error_code} {token} {message}'
        raise ParserError(s)

    def check_token(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)

    def program(self):
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        prog_node = Program(declarations, compound_statement)
        self.check_token(DOT)
        return prog_node

    def declarations(self):
        if self.current_token.token_type == INTEGER_TYPE:
            node = self.variable_declaration(INTEGER_TYPE)
        elif self.current_token.token_type == FLOAT_TYPE:
            node = self.variable_declaration(FLOAT_TYPE)
        else:
            node = self.empty()
        return node

    def variable_declaration(self, token_type):
        type_current_id = self.type_id()

        var_nodes = []
        while self.current_token.token_type != COMMA:
            self.check_token(COMMA)
            var_decl = self.variable()
            var_nodes.append(var_decl)
        self.check_token(SEMI)

        var_declarations = [VarDecl(var_node, type_current_id) for var_node in var_nodes]
        return var_declarations

    def variable(self):
        token = self.current_token
        # if self.current_token.token_type == self.assignment():
        #     node = self.assignment()
        #     return node
        self.current_token(ID)
        node = Var(token)
        return node

    def assignment(self):
        left = self.current_token()
        self.check_token(ID)
        op = self.current_token()
        self.check_token(ASSIGN)
        right = self.expr()
        node = Assign(left=left, op=op, right=right)
        return node

    def type_id(self):
        token = self.current_token
        if token.token_type == INTEGER_TYPE:
            self.current_token(token)
        if token.token_type == FLOAT_TYPE:
            self.current_token(token)
        return token

    def empty(self):
        return NoOp()

    def compound_statement(self):
        self.check_token(MAIN)
        self.check_token(LBRAKET)
        nodes = self.statement_list()
        root = Compound()
        for node in nodes:
            root.children.append(node)
        self.check_token(RBRAKET)
        return root

    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.token_type == SEMI:
            self.current_token(SEMI)
            results.append(self.statement())

        return results

    def statement(self):
        if self.current_token.token_type == ID:
            node = self.assignment()
        else:
            node = self.empty()
        return node

    def factor(self):
        token = self.current_token
        if token.token_type == INTEGER:
            self.check_token(INTEGER)
            return Num(token)
        elif token.token_type == FLOAT:
            self.check_token(FLOAT)
            return Num(token)
        elif token.token_type == PLUS:
            self.check_token(PLUS)
            return UnaryOp(token, self.factor())
        else:
            node = self.variable()
            return node

    def term(self):
        node = self.factor()

        while self.current_token.token_type in (MUL, FLOAT_DIV):
            token = self.current_token
            if token.token_type == MUL:
                self.check_token(MUL)
            elif token.token_type == FLOAT_DIV:
                self.check_token(FLOAT_DIV)

            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()

        while self.current_token.token_type in (PLUS, MINUS):
            token = self.current_token
            if token.token_type == PLUS:
                self.check_token(PLUS)
            elif token.token_type == MINUS:
                self.check_token(MINUS)

            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        tree = self.program()
        if self.current_token.token_type != EOF:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return tree
