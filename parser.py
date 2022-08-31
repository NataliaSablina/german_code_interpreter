from lexer import *
from ast_nodes import *


# l1 = Lexer('Ausfuhrung { \n int a, b, c; \n a = 3 + 4*7; float r; r = 1.2+6; \n int h; \n}.')

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
        if declarations:
            self.check_token(SEMI)
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
        var_declarations = []
        if self.current_token.token_type == ID and self.lexer.current_char == '=':
            var_declarations.extend(self.variable_assignment_declaration(type_current_id))
            while self.current_token.token_type == COMMA:
                self.check_token(COMMA)
                var_declarations.extend(self.variable_assignment_declaration(type_current_id))
        else:
            var_declarations = [VarDecl(self.variable(), type_current_id)]
            while self.current_token.token_type == COMMA:
                self.check_token(COMMA)
                if self.current_token.token_type == ID and self.lexer.current_char == '=':
                    var_declarations.extend(self.variable_assignment_declaration(type_current_id))
                    while self.current_token.token_type == COMMA:
                        self.check_token(COMMA)
                        var_declarations.extend(self.variable_assignment_declaration(type_current_id))
                else:
                    print(self.current_token)
                    var_decl = VarDecl(self.variable(), type_current_id)
                    var_declarations.append(var_decl)
        return var_declarations

    def variable_assignment_declaration(self, type_current_id):
        var_declarations = []
        token = self.current_token
        print(self.current_token)
        self.check_token(ID)
        self.check_token(ASSIGN)
        var_assign_decl = VarAssignDecl(type_current_id, token.value, self.current_token.value)
        var_declarations.append(var_assign_decl)
        if self.current_token.token_type == INTEGER:
            self.check_token(INTEGER)
        elif self.current_token.token_type == FLOAT:
            self.check_token(FLOAT)
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
        left = Var(self.current_token)
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
        elif token.token_type == LPAREN:
            self.check_token(LPAREN)
            node = self.expr()
            self.check_token(RPAREN)
            return node
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
