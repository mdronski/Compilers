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
        return self.parser.parse(text, lexer=self.scanner.lexer, tracking=True)

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IF'),
        ("nonassoc", 'ELSE'),
        ("right", '=', "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN"),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", '+', '-', 'DOTADD', 'DOTSUB'),
        ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
        ("left", 'UMINUS'),
        ("right", '\'')
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

        if len(p) == 2:
            p[0] = AST.Statements()
            p[0].children.append(p[1])
        elif len(p) == 3:
            p[1].children.append(p[2])
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]
        elif len(p) == 5:
            p[1].children.extend(p[3].children)
            p[0] = p[1]

    def p_statement(self, p):
        """statement : assignment
                     | flow_control """
        p[0] = p[1]

    def p_assignment(self, p):
        """assignment : variable assignment_op expression ';'"""

        p[0] = AST.Assignment(p[1], p[2], p[3], p.lineno(1))

    def p_assignment_op(self, p):
        """assignment_op : '='
                         | ADDASSIGN
                         | SUBASSIGN
                         | MULASSIGN
                         | DIVASSIGN"""
        p[0] = p[1]

    def p_expression(self, p):
        """expression : variable
                      | constant
                      | matrix
                      | un_op
                      | bin_op
                      | logic_op
                      | '(' expression ')'"""

        if isinstance(p[1], AST.Constant):
            p[0] = p[1]
        elif p[1] == '(':
            p[0] = p[2]
        elif isinstance(p[1], str):
            p[0] = AST.Variable(p[1], p.lineno(1))
        else:
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

    def p_variable(self, p):
        """variable : ID
                    | matrix_access"""
        p[0] = AST.Variable(p[1], p.lineno(1))

    def p_value(self, p):
        """value : variable
                 | matrix
                 | constant"""
        p[0] = AST.Value(p[1])

    def p_matrix_access(self, p):
        """matrix_access : ID '[' int_sequence ']'"""
        p[0] = AST.MatrixAccess(p[1], p[3], p.lineno(1))

    def p_matrix(self, p):
        """matrix : EYE '(' int_sequence ')'
                       | ZEROS '(' int_sequence ')'
                       | ONES '(' int_sequence ')'
                       | '[' matrix_row ']' """

        if p[1] == 'eye':
            p[0] = AST.EyeMatrix(p[3], p.lineno(1))
        elif p[1] == 'zeros':
            p[0] = AST.ZerosMatrix(p[3], p.lineno(1))
        elif p[1] == 'ones':
            p[0] = AST.OnesMatrix(p[3], p.lineno(1))
        else:
            p[0] = AST.Matrix()
            p[0].rows = p[2]

    def p_int_sequence(self, p):
        """int_sequence : int_sequence ',' INTNUM
                        | INTNUM"""
        if len(p) == 2:
            p[0] = []
            p[0].append(p[1])
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_matrix_row(self, p):
        """matrix_row : matrix_row ',' value
                      | value"""
        if len(p) == 2:
            p[0] = AST.MatrixRow(p.lineno(1))
            p[0].values.append(p[1])
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

        p[0] = AST.BinOp(p[1], p[2], p[3], p.lineno(1))

    def p_logic_op(self, p):
        """logic_op : expression EQ expression
                  | expression NEQ expression
                  | expression '>' expression
                  | expression '<' expression
                  | expression LE expression
                  | expression GE expression"""

        p[0] = AST.LogicOp(p[1], p[2], p[3], p.lineno(1))

    def p_un_op(self, p):
        """un_op : expression "'"
                 | '-' expression %prec UMINUS"""
        if p[1] == '-':
            p[0] = AST.UnaryOp(p[2], p[1], p.lineno(1))
        else:
            p[0] = AST.UnaryOp(p[1], p[2], p.lineno(1))

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
        if len(p) == 6:
            p[0] = AST.CondStatement(p[3], p[5])
        else:
            p[0] = AST.CondStatement(p[3], p[5], True, p[7])

    def p_conditional_instructions(self, p):
        """conditional_instructions : statement
                                    | '{' statements '}'"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_while_loop(self, p):
        """while_loop : WHILE '(' logic_op ')' conditional_instructions"""
        p[0] = AST.WhileLoop(p[3], p[5])

    def p_for_loop(self, p):
        """for_loop : FOR ID '=' expression ':' expression conditional_instructions"""
        p[0] = AST.ForLoop(p[2], p[4], p[6], p[7])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstr(p[2], p.lineno(1))

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstr(p.lineno(1))

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstr(p.lineno(1))

    def p_print_instr(self, p):
        """print_instr : PRINT instructions_to_print ';' """
        p[0] = p[2]

    def p_instructions_to_print(self, p):
        """instructions_to_print : instructions_to_print ',' expression
                                 | expression"""
        if len(p) == 2:
            p[0] = AST.PrintInstr()
            p[0].children.append(p[1])
        else:
            p[1].children.append(p[3])
            p[0] = p[1]
