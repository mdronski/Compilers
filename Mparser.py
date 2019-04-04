import ply.yacc as yacc
from Scanner import Scanner
import AST
import numpy as np


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
        p[0] = p[1]

    def p_statements(self, p):
        """statements : '{' statements '}'
                      | statements statement
                      | statement
                      | statements '{' statements '}'"""

        # if p[0] is None:
        #     p[0] = AST.Statements()
        if len(p) == 2:
            p[0] = AST.Statements()
            p[0].statements.append(p[1])
        elif len(p) == 3:
            p[1].statements.append(p[2])
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]
        elif len(p) == 5:
            p[1].statements.extend(p[3])
            p[0] = p[1]

        print(p[0])

    def p_statement(self, p):
        """statement : assignment
                     | flow_control """
        p[0] = p[1]

    def p_assignment(self, p):
        """assignment : ID '=' expression ';'
                      | ID ADDASSIGN expression ';'
                      | ID SUBASSIGN expression ';'
                      | ID MULASSIGN expression ';'
                      | ID DIVASSIGN expression ';'
                      | ID '[' INTNUM ',' INTNUM ']' '=' expression ';'"""

        if p[2] == '=':
            p[0] = AST.Assignment(p[1], p[3])
        elif p[2] == '+=':
            p[0] = AST.Assignment(p[1], p[1] + p[3])
        elif p[2] == '-=':
            p[0] = AST.Assignment(p[1], p[1] - p[3])
        elif p[2] == '*=':
            p[0] = AST.Assignment(p[1], p[1] * p[3])
        elif p[2] == '/=':
            p[0] = AST.Assignment(p[1], p[1] / p[3])
        elif len(p) == 9:
            p[0] = AST.MatrixAssignment(p[1], p[3], p[5], p[8])

    def p_expression(self, p):
        """expression : ID
                      | ID '[' INTNUM ',' INTNUM ']'
                      | constant
                      | matrix_decl
                      | bin_op
                      | un_op
                      | logic_op
                      | '(' expression ')'"""
        p[0] = p[1]

    def p_constant(self, p):
        """constant : INTNUM
                    | FLOATNUM
                    | STRING"""

        if isinstance(p[1], int):
            p[0] = AST.IntNum(p[1])
        if isinstance(p[1], float):
            p[0] = AST.FloatNum(p[1])
        if isinstance(p[1], str):
            p[0] = AST.String(p[1])

    def p_matrix_decl(self, p):
        """matrix_decl : EYE '(' INTNUM ')'
                       | ZEROS '(' INTNUM ')'
                       | ONES '(' INTNUM ')'
                       | '[' matrix_rows ']'"""

        if p[1] == 'eye':
            p[0] = AST.Matrix(np.eye(p[3]))
        elif p[1] == 'zeros':
            p[0] = AST.Matrix(np.zeros(p[3]))
        elif p[1] == 'ones':
            p[0] = AST.Matrix(np.ones(p[3]))
        else:
            p[0] = AST.Matrix(np.asarray(p[2]))

    def p_matrix_rows(self, p):
        """matrix_rows : matrix_rows matrix_row
                       | matrix_row"""
        if p[0] is None:
            p[0] = AST.MatrixRows()
        elif len(p) == 2:
            p[0] = p[1]
        else:
            p[1].rows.append(p[2])
            p[0] = p[1]

    def p_matrix_row(self, p):
        """matrix_row : matrix_row ',' INTNUM
                      | matrix_row ';'
                      | INTNUM"""
        if p[0] is None:
            p[0] = AST.MatrixRow()
        elif len(p) == 2:
            p[0] = p[1]
        else:
            p[1].values.append(p[3])
            p[0] = p[1]

    def p_bin_op(self, p):
        """bin_op : expression '+' expression
                  | expression '*' expression
                  | expression '-' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""

        p[0] = AST.BinOp(p[1], p[2], p[3])

    def p_logic_op(self, p):
        """logic_op : expression EQ expression
                  | expression NEQ expression
                  | expression '>' expression
                  | expression '<' expression
                  | expression LE expression
                  | expression GE expression"""

        p[0] = AST.LogicOp(p[1], p[2], p[3])

    def p_un_op(self, p):
        """un_op : expression "'"
                 | '-' expression %prec UMINUS"""
        if p[1] == '-':
            p[0] = AST.UnaryOp(p[2], p[1])
        else:
            p[0] = AST.UnaryOp(p[1], p[2])

    def p_flow_control(self, p):
        """flow_control : conditional_statement
                        | while_loop
                        | for_loop
                        | return_instr
                        | break_instr
                        | continue_instr
                        | print_instr"""
        p[0] = p[1]

    def p_conditional_statement(self, p):
        """conditional_statement : IF '(' logic_op ')' conditional_instructions %prec IF
                                 | IF '(' logic_op ')' conditional_instructions ELSE conditional_instructions """
        if len(p) == 7:
            p[0] = AST.CondStatement(p[3], p[4])
        else:
            p[0] = AST.CondStatement(p[3], p[4], True, p[6])

    def p_conditional_instructions(self, p):
        """conditional_instructions : statement
                                    | '{' statements '}'"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_while_loop(self, p):
        """while_loop : WHILE '(' logic_op ')' conditional_instructions"""
        p[0] = AST.WhileLoop(p[4], p[6])

    def p_for_loop(self, p):
        """for_loop : FOR ID '=' expression ':' expression conditional_instructions"""
        p[0] = AST.ForLoop(p[3], p[5], p[7], p[8])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstr(p[3])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstr()

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstr()

    def p_print_instr(self, p):
        """print_instr : PRINT instructions_to_print ';' """
        p[0] = AST.PrintInstr()

    def p_instructions_to_print(self, p):
        """instructions_to_print : instructions_to_print ',' expression
                                 | expression"""
        if p[0] is None:
            p[0] = AST.PrintInstr()
        elif len(p) == 2:
            p[0] = p[1]
        else:
            p[1].instructions.append(p[3])
            p[0] = p[1]
