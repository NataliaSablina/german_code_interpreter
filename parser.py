from lexer import *
from ast_nodes import *


# l1 = Lexer('Ausfuhrung { \n int a, b, c; \n a = 3 + 4*7; float r; r = 1.2+6; \n int h; \n}.')


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, error_code, token, message):
        s = f"{error_code} {token} {message}"
        raise ParserError(s)

    def check_token(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print("check_token", self.current_token)
            self.error(
                ErrorCode.UNEXPECTED_TOKEN,
                self.current_token,
                message="Incorrect token",
            )

    def program(self):
        print("program")
        declarations = self.declarations()
        name = self.current_token.value
        self.check_token(MAIN)
        compound_statement = self.compound_statement()
        prog_node = Program(name, declarations, compound_statement)
        self.check_token(DOT)
        return prog_node

    def declarations(self):
        print("declarations")
        declarations = []
        while True:
            if self.current_token.token_type in (INTEGER_TYPE, FLOAT_TYPE):
                if self.current_token.token_type == INTEGER_TYPE:
                    node = self.variable_declaration()
                    declarations.extend(node)
                    print("declarations", declarations)
                elif self.current_token.token_type == FLOAT_TYPE:
                    node = self.variable_declaration()
                    declarations.extend(node)
                    print("FLOAT_TYPE, declarations")

                self.check_token(SEMI)
                print(self.current_token)
            elif self.current_token.token_type == ID:
                print("check Id")
                node = self.statement()
                self.check_token(SEMI)
                declarations.append(node)
            elif self.current_token.token_type == PROCEDURE:
                print("Check procedure")
                node = self.procedure_declaration()
                self.check_token(SEMI)
                declarations.append(node)
            else:
                break
        return declarations

    def procedure_declaration(self):
        self.check_token(PROCEDURE)
        proc_name = self.current_token.value
        self.check_token(ID)
        self.check_token(LPAREN)
        params = self.formal_parameters_list()
        self.check_token(RPAREN)
        self.check_token(LBRAKET)
        block = self.statement_list()
        self.check_token(RBRAKET)
        node = ProcDecl(proc_name, params, block)
        return node

    def formal_parameters_list(self):
        if self.current_token.token_type not in (INTEGER_TYPE, FLOAT_TYPE):
            return []
        param_nodes = self.formal_parameters()
        while self.current_token.token_type == SEMI:
            self.check_token(SEMI)
            if self.current_token.token_type == RPAREN:
                break
            param_nodes.extend(self.formal_parameters())
        return param_nodes

    def formal_parameters(self):
        param_nodes = []
        result = self.variable_declaration()
        return result

    def variable_declaration(self):
        print("variable_declarations")
        type_current_id = self.type_id()
        var_declarations = []
        if self.current_token.token_type == ID and self.lexer.current_char == "=":
            var_declarations.extend(
                self.variable_assignment_declaration(type_current_id)
            )
            while self.current_token.token_type == COMMA:
                self.check_token(COMMA)
                var_declarations.extend(
                    self.variable_assignment_declaration(type_current_id)
                )
            return var_declarations
        else:
            var_declarations = [VarDecl(self.variable(), type_current_id)]
            while self.current_token.token_type == COMMA:
                self.check_token(COMMA)
                if (
                    self.current_token.token_type == ID
                    and self.lexer.current_char == "="
                ):
                    var_declarations.extend(
                        self.variable_assignment_declaration(type_current_id)
                    )
                    while self.current_token.token_type == COMMA:
                        self.check_token(COMMA)
                        var_declarations.extend(
                            self.variable_assignment_declaration(type_current_id)
                        )
                    return var_declarations
                else:
                    print(self.current_token)
                    var_decl = VarDecl(self.variable(), type_current_id)
                    var_declarations.append(var_decl)
            return var_declarations

    def variable_assignment_declaration(self, type_current_id):
        print("variable_assignment_declaration")
        var_declarations = []
        token = self.current_token
        self.check_token(ID)
        self.check_token(ASSIGN)
        var_assign_decl = VarAssignDecl(token.value, type_current_id, self.expr())
        var_declarations.append(var_assign_decl)
        return var_declarations

    def proccall_statement(self):
        token = self.current_token
        proc_name = self.current_token.value
        self.check_token(ID)
        self.check_token(LPAREN)
        actual_params = []
        if self.current_token.token_type != RPAREN:
            node = self.expr()
            actual_params.append(node)

        while self.current_token.token_type == COMMA:
            self.check_token(COMMA)
            node = self.expr()
            actual_params.append(node)
        self.check_token(RPAREN)

        node = ProcedureCall(
            proc_name=proc_name,
            actual_params=actual_params,
            token=token,
        )
        return node

    def variable(self):
        print("variable")
        token = self.current_token
        self.check_token(ID)
        node = Var(token)
        return node

    def assignment(self):
        print("assignment")
        left = Var(self.current_token)
        self.check_token(ID)
        op = self.current_token
        self.check_token(ASSIGN)
        right = self.expr()
        node = Assign(left=left, op=op, right=right)
        return node

    def type_id(self):
        print("type_id")
        token = self.current_token
        if token.token_type == INTEGER_TYPE:
            self.check_token(INTEGER_TYPE)
        if token.token_type == FLOAT_TYPE:
            self.check_token(FLOAT_TYPE)
        return token

    def empty(self):
        print("empty")
        return NoOp()

    def compound_statement(self):
        print("compound_statement")
        self.check_token(LBRAKET)
        nodes = self.statement_list()
        root = Compound()
        for node in nodes:
            root.children.append(node)
        self.check_token(RBRAKET)
        return root

    def statement_list(self):
        print("statement_list")
        node = self.statement()
        results = [node]
        while (
            self.current_token.token_type == SEMI or self.current_token.token_type == ID
        ):
            self.check_token(SEMI)
            print("JJJJJJJJJJJJJJJJJJJJJJJJJ", self.current_token.token_type)
            results.append(self.statement())
        return results

    def statement(self):
        print("statement")
        print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
        print(self.current_token.token_type)
        if self.current_token.token_type == ID and self.lexer.current_char == '(':
            node = self.proccall_statement()
        elif self.current_token.token_type == ID:
            node = self.assignment()
        elif self.current_token.token_type == INTEGER_TYPE:
            node = self.variable_declaration()
        elif self.current_token.token_type == FLOAT_TYPE:
            node = self.variable_declaration()
        elif self.current_token.token_type == PROCEDURE:
            print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
            self.check_token(PROCEDURE)
            print(self.current_token)
            proc_name = self.current_token.value
            self.check_token(ID)
            self.check_token(LPAREN)
            params = self.formal_parameters_list()
            self.check_token(RPAREN)
            self.check_token(LBRAKET)
            block = self.statement_list()
            self.check_token(RBRAKET)
            node = ProcDecl(proc_name, params, block)
            print(
                "___________________________________________________________________________________________________",
                node,
            )
        else:
            node = self.empty()
        return node

    def factor(self):
        print("factor")
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
        elif token.token_type == MINUS:
            self.check_token(MINUS)
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
        print("term")
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
        print("expr")
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
        print("parse")
        tree = self.program()
        if self.current_token.token_type != EOF:
            self.error(
                ErrorCode.UNEXPECTED_TOKEN,
                self.current_token,
                message="Program must end by EOF",
            )
        return tree
