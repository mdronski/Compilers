import ply.yacc as yacc
from Scanner import Scanner


class Mparser:

    def __init__(self):
        self.scanner = Scanner()
        self.parser = None

    def parse(self, text):
        self.parser = yacc.yacc(module=self)
        return self.parser.parse(text, lexer=self.scanner.lexer)

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IF'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", '+', '-', 'DOTADD', 'DOTSUB'),
        ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
        ("left", 'UMINUS')
    )

    def p_error(self, p):
        self.no_error = False
        if p:
            print("Syntax error at line {}: token({}, '{}')".format(
                p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : statements"""
        pass

    def p_statements(self, p):
        """statements : '{' statements '}'
                      | statements statement
                      | statement
                      | statements '{' statements '}'"""
        pass

    def p_statement(self, p):
        """statement : assignment
                     | flow_control """
        pass

    def p_assignment(self, p):
        """assignment : ID '=' expression ';'
                      | ID ADDASSIGN expression ';'
                      | ID SUBASSIGN expression ';'
                      | ID MULASSIGN expression ';'
                      | ID DIVASSIGN expression ';'
                      | ID '[' INTNUM ',' INTNUM ']' '=' expression ';'"""
        pass

    def p_expression(self, p):
        """expression : ID
                      | ID '[' INTNUM ',' INTNUM ']'
                      | constant
                      | matrix_decl
                      | bin_op
                      | un_op
                      | logic_op
                      | '(' expression ')'"""
        pass

    def p_constant(self, p):
        """constant : INTNUM
                    | FLOATNUM
                    | STRING"""
        pass

    def p_matrix_decl(self, p):
        """matrix_decl : EYE '(' INTNUM ')'
                       | ZEROS '(' INTNUM ')'
                       | ONES '(' INTNUM ')'
                       | '[' matrix_rows ']'"""
        pass

    def p_matrix_rows(self, p):
        """matrix_rows : matrix_rows matrix_row
                       | matrix_row"""

    def p_matrix_row(self, p):
        """matrix_row : matrix_row ',' INTNUM
                      | matrix_row ';'
                      | INTNUM"""

    def p_bin_op(self, p):
        """bin_op : expression '+' expression
                  | expression '*' expression
                  | expression '-' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""
    pass

    def p_logic_op(self, p):
        """logic_op : expression EQ expression
                  | expression NEQ expression
                  | expression '>' expression
                  | expression '<' expression
                  | expression LE expression
                  | expression GE expression"""
        pass

    def p_un_op(self, p):
        """un_op : expression "'"
                 | '-' expression %prec UMINUS"""
    pass

    def p_flow_control(self, p):
        """flow_control : conditional_statement
                        | while_loop
                        | for_loop
                        | return_instr
                        | break_instr
                        | continue_instr
                        | print_instr"""
        pass

    def p_conditional_statement(self, p):
        """conditional_statement : IF '(' logic_op ')' conditional_instructions %prec IF
                                 | IF '(' logic_op ')' conditional_instructions ELSE conditional_instructions """
        pass

    def p_conditional_instructions(self, p):
        """conditional_instructions : statement
                                    | '{' statements '}'"""
        pass

    def p_while_loop(self, p):
        """while_loop : WHILE '(' logic_op ')' conditional_instructions"""
        pass

    def p_for_loop(self, p):
        """for_loop : FOR ID '=' expression ':' expression conditional_instructions"""
        pass

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        pass

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        pass

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        pass

    def p_print_instr(self, p):
        """print_instr : PRINT instructions ';' """
        pass

    def p_instructions_to_print(self, p):
        """instructions : instructions ',' expression
                        | expression"""
