import ply.yacc as yacc
import numpy as np
from Scanner import tokens

precedence = (
    ("nonassoc", 'IF'),
    ("nonassoc", 'ELSE'),
    ("right", '='),
    ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    )


# def p_error(self, p):
#     self.no_error = False
#     if p:
#         print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
#                                                                                   self.scanner.find_tok_column(p),
#                                                                                   p.type,
#                                                                                   p.value))
#     else:
#         print("Unexpected end of input")
#
#
# def p_expression_sum(p):
#     """EXPRESSION : EXPRESSION '+' EXPRESSION
#                   | EXPRESSION '-' EXPRESSION"""
#     if p[2] == '+':
#         p[0] = p[1] + p[3]
#     elif p[2] == '-':
#         p[0] = p[1] - p[3]
#
#
# def p_expression_mul(p):
#     """EXPRESSION : EXPRESSION '*' EXPRESSION
#                   | EXPRESSION '/' EXPRESSION"""
#     if p[2] == '*':
#         p[0] = p[1] * p[3]
#     elif p[2] == '/':
#         p[0] = p[1] / p[3]
#
#
# def p_matrix_declaration(p):
#     """MATRIX : ZEROS '(' INTNUM ')'
#               | ONES '(' INTNUM ')'
#               | EYE '(' INTNUM ')'"""
#     if p[1] == 'zeros':
#         p[0] = np.zeros(p[3])
#     elif p[1] == 'ones':
#         p[0] = np.ones(p[3])
#     elif p[1] == 'eye':
#         p[0] = np.eye(p[3])
#
#
# def p_expression_matrix(p):
#     """EXPRESSION : MATRIX"""
#     p[0] = p[1]


def p_error(self, p):
    self.no_error = False
    if p:
        print("Syntax error at line {0}, column {1}: token({2}, '{3}')".format(
                        p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(self, p):
    """program : blocks"""

    p[0] = p[1]


def p_blocks(self, p):
    """blocks : blocks block
              | block """

    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_block(self, p):
    """block : instruction
             | declaration """
    p[0] = p[1]


def p_declaration(self, p):
    """declaration : ID '=' expression  ';'"""
    if len(p) > 3:
        p[0] = AST.Declaration(p[1], p[2], None)
    else:
        p[0] = AST.Declaration(None, None, p[1])
    p[0].line = self.scanner.lexer.lineno


def p_inits(self, p):
    """INITS : INITS ',' INIT
             | INIT """
    p[0] = AST.Init(p[1], p[3])


def p_instructions(self, p):
    """iNSTRUCTIONS : INSTRUCTIONS INSTRUCTION
                    | INSTRUCTION """
    if len(p) > 2:
        p[0] = AST.Instructions(p[1], p[2])
    else:
        p[0] = AST.Instructions(None, p[1])
    p[0].line = self.scanner.lexer.lineno


def p_instruction(self, p):
    """INSTRUCTION : PRINT_INSTR
                   | LABELED_INSTR
                   | ASSIGNMENT
                   | CHOICE_INSTR
                   | WHILE_INSTR
                   | REPEAT_INSTR
                   | RETURN_INSTR
                   | BREAK_INSTR
                   | CONTINUE_INSTR
                   | COMPOUND_INSTR
                   | EXPRESSION ';' """
    p[0] = p[1]
    p[0].line = self.scanner.lexer.lineno


def p_print_instr(self, p):
    """PRINT_INSTR : PRINT EXPRESSION ';'
                   | PRINT ERROR ';' """
    if isinstance(p[2], AST.Expression):
        p[0] = AST.Print(p[2], None)
    else:
        p[0] = AST.Print(None, p[2])
    p[0].line = self.scanner.lexer.lineno


def p_labeled_instr(self, p):
    """LABELED_INSTR : ID ':' INSTRUCTION """
    p[0] = AST.Labeled(p[1], p[3])
    p[0].line = self.scanner.lexer.lineno


def p_assignment(self, p):
    """ASSIGNMENT : ID '=' EXPRESSION ';' """
    p[0] = AST.Assignment(p[1], p[3])
    p[0].line = self.scanner.lexer.lineno


def p_choice_instr(self, p):
    """CHOICE_INSTR : IF '(' CONDITION ')' INSTRUCTION  %PREC IFX
                    | IF '(' CONDITION ')' INSTRUCTION ELSE INSTRUCTION
                    | IF '(' ERROR ')' INSTRUCTION  %PREC IFX
                    | IF '(' ERROR ')' INSTRUCTION ELSE INSTRUCTION """
    if isinstance(p[3], AST.Condition):
        if len(p) == 8 and p[6].lower() == "else":
            if_node = AST.If(p[3], p[5], None)
            if_node.line = self.scanner.lexer.lineno
            else_node = AST.Else(p[7])
            else_node.line = self.scanner.lexer.lineno
            p[0] = AST.Choice(if_node, else_node)
        else:
            if_node = AST.If(p[3], p[5], None)
            if_node.line = self.scanner.lexer.lineno
            p[0] = AST.Choice(if_node, None)
    else:
        if len(p) == 8 and p[6].lower() == "else":
            if_node = AST.If(None, p[5], p[3])
            if_node.line = self.scanner.lexer.lineno
            else_node = AST.Else(p[7])
            else_node.line = self.scanner.lexer.lineno
            p[0] = AST.Choice(if_node, else_node)
        else:
            if_node = AST.If(None, p[5], p[3])
            if_node.line = self.scanner.lexer.lineno
            p[0] = AST.Choice(if_node, None)
    p[0].line = self.scanner.lexer.lineno


def p_while_instr(self, p):
    """WHILE_INSTR : WHILE '(' CONDITION ')' INSTRUCTION
                   | WHILE '(' ERROR ')' INSTRUCTION """
    if isinstance(p[3], AST.Condition):
        p[0] = AST.While(p[3], p[5], None)
    else:
        p[0] = AST.While(None, p[5], p[3])
    p[0].line = self.scanner.lexer.lineno


def p_repeat_instr(self, p):
    """REPEAT_INSTR : REPEAT INSTRUCTIONS UNTIL CONDITION ';' """
    p[0] = AST.RepeatUntil(p[2], p[4])
    p[0].line = self.scanner.lexer.lineno


def p_return_instr(self, p):
    """return_instr : RETURN expression ';' """
    p[0] = AST.Return(p[2])
    p[0].line = self.scanner.lexer.lineno


def p_continue_instr(self, p):
    """continue_instr : CONTINUE ';' """
    p[0] = AST.Continue()
    p[0].line = self.scanner.lexer.lineno


def p_break_instr(self, p):
    """break_instr : BREAK ';' """
    p[0] = AST.Break()
    p[0].line = self.scanner.lexer.lineno


def p_compound_instr(self, p):
    """compound_instr : '{' blocks '}' """
    p[0] = AST.Compound(p[2])
    p[0].line = self.scanner.lexer.lineno


def p_condition(self, p):
    """condition : expression"""
    p[0] = p[1]
    p[0].line = self.scanner.lexer.lineno


def p_const(self, p):
    """const : INTEGER
             | FLOAT
             | STRING"""
    p[0] = AST.Const(p[1])
    p[0].line = self.scanner.lexer.lineno


def p_expression(self, p):
    """expression : const
                  | ID
                  | expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '%' expression
                  | expression '|' expression
                  | expression '&' expression
                  | expression '^' expression
                  | expression AND expression
                  | expression OR expression
                  | expression SHL expression
                  | expression SHR expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression '>' expression
                  | expression '<' expression
                  | expression LE expression
                  | expression GE expression
                  | '(' expression ')'
                  | '(' error ')'
                  | ID '(' expr_list_or_empty ')'
                  | ID '(' error ')' """
    if len(p) == 2:
        if isinstance(p[1], AST.Const):
            p[0] = p[1]
        else:
            p[0] = AST.Id(p[1])
    elif len(p) == 4:
        if p[1] == "(":
            if isinstance(p[2], AST.Expression):
                p[0] = AST.ExpressionInPar(p[2], None)
            else:
                p[0] = AST.ExpressionInPar(None, p[2])
        else:
            p[0] = AST.BinExpr(p[1], p[2], p[3])
    else:
        if isinstance(p[3], AST.ExpressionList):
            p[0] = AST.IdWithPar(p[1], p[3], None)
        else:
            p[0] = AST.IdWithPar(p[1], None, p[3])
    p[0].line = self.scanner.lexer.lineno


def p_expr_list_or_empty(self, p):
    """expr_list_or_empty : expr_list
                          | """
    if len(p) > 1:
        p[0] = AST.ExpressionList(p[1], None)
    else:
        p[0] = AST.ExpressionList(None, None)
    p[0].line = self.scanner.lexer.lineno


def p_expr_list(self, p):
    """expr_list : expr_list ',' expression
                 | expression """
    if len(p) > 2:
        p[0] = AST.ExpressionList(p[1], p[3])
    else:
        p[0] = AST.ExpressionList(None, p[1])
    p[0].line = self.scanner.lexer.lineno


# Build the parser
parser = yacc.yacc()
#
# while True:
#     try:
#         s = raw_input('2 + 2')
#     except EOFError:
#         break
#     if not s: continue
#     result = parser.parse(s)
#     print(result)
