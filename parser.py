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
            print(self.current_token)
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token, message='Incorrect token')

    def program(self):
        print('program')
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        prog_node = Program(declarations, compound_statement)
        self.check_token(DOT)
        return prog_node

    def declarations(self):
        print('declarations')
        if self.current_token.token_type == INTEGER_TYPE:
            node = self.variable_declaration()
        elif self.current_token.token_type == FLOAT_TYPE:
            node = self.variable_declaration()
        else:
            node = self.empty()
        return node

    def variable_declaration(self):
        print('variable_declarations')
        type_current_id = self.type_id()
        print(self.current_token)
        var_nodes = [self.variable()]
        print(self.current_token)

        while self.current_token.token_type == COMMA:
            self.check_token(COMMA)
            var_decl = self.variable()
            var_nodes.append(var_decl)
            print(self.current_token)
            # self.check_token(SEMI)
        # else:
        #     var_nodes.append(self.variable())
        #     # self.check_token(SEMI)

        var_declarations = [VarDecl(var_node, type_current_id) for var_node in var_nodes]
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        return var_declarations

    def variable(self):
        print('variable')
        token = self.current_token
        print('==========================', token)
        # if self.current_token.token_type == self.assignment():
        #     node = self.assignment()
        #     return node
        self.check_token(ID)

        node = Var(token)
        return node

    def assignment(self):
        print('assignment')
        left = self.current_token
        self.check_token(ID)
        op = self.current_token
        self.check_token(ASSIGN)
        right = self.expr()
        node = Assign(left=left, op=op, right=right)
        return node

    def type_id(self):
        print(self.current_token)
        print('type_id')
        token = self.current_token
        if token.token_type == INTEGER_TYPE:
            self.check_token(INTEGER_TYPE)
        if token.token_type == FLOAT_TYPE:
            self.check_token(FLOAT_TYPE)
        return token

    def empty(self):
        print('empty')
        return NoOp()

    def compound_statement(self):
        print(self.current_token)
        print('compound_statement')
        self.check_token(MAIN)
        self.check_token(LBRAKET)
        nodes = self.statement_list()
        root = Compound()
        for node in nodes:
            root.children.append(node)
        print(root.children)
        print(self.current_token)
        self.check_token(RBRAKET)
        print(self.current_token)
        return root

    def statement_list(self):
        print('statement_list')
        node = self.statement()
        results = [node]
        print('_______________', self.current_token)
        while self.current_token.token_type == SEMI:
            self.check_token(SEMI)
            results.append(self.statement())
            print(self.current_token)
        return results

    def statement(self):
        print('statement')
        print('+++++++++++++', self.current_token)
        while True:
            if self.current_token.token_type == ID:
                node = self.assignment()
                return node
            elif self.current_token.token_type == INTEGER_TYPE:
                node = self.declarations()
                return node
            elif self.current_token.token_type == FLOAT_TYPE:
                node = self.declarations()
                return node
            else:
                node = self.empty()
                return node

    def factor(self):
        print('factor')
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
        print('term')
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
        print('expr')
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
        print('parse')
        tree = self.program()
        if self.current_token.token_type != EOF:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token, message='Program must end by EOF')
        print(tree)
        return tree
