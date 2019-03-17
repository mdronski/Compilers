import sys
import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT',
}

tokens = [
        'DOTADD',
        'DOTSUB',
        'DOTMUL',
        'DOTDIV',
        'ADDASSIGN',
        'SUBASSIGN',
        'MULASSIGN',
        'DIVASSIGN',
        'LESSEQUAL',
        'GREATEREQUAL',
        'NOTEQUAL',
        'EQUAL',
        'ID',
        'INTNUM',
        'FLOATNUM',
        'STRING'
         ] + list(reserved.values())

literals = ['+', '-', '*', '/',
            '=', '<', '>',
            '(', ')', '[', ']', '{', '}',
            '\'', ',', ':', ';']

t_DOTADD        = r'\.\+'
t_DOTSUB        = r'\.\-'
t_DOTMUL        = r'\.\*'
t_DOTDIV        = r'\.\/'
t_ADDASSIGN     = r'\+='
t_SUBASSIGN     = r'-='
t_MULASSIGN     = r'\*='
t_DIVASSIGN     = r'/='
t_LESSEQUAL     = r'<='
t_GREATEREQUAL  = r'>='
t_NOTEQUAL      = r'!='
t_EQUAL         = r'=='


def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_FLOATNUM(t):
    r'(\d*\.\d+|\d+\.\d*)(E\d+)?'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = str(t.value)[1:-1]
    return t


def t_COMMENT(t):
    r'\#.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


t_ignore = ' \t'


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()

