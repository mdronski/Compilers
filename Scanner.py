import ply.lex as lex


class Scanner(object):

    def __init__(self):
        self.lexer = lex.lex(object=self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

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
                 'LE',
                 'GE',
                 'NEQ',
                 'EQ',
                 'ID',
                 'INTNUM',
                 'FLOATNUM',
                 'STRING'
             ] + list(reserved.values())

    literals = ['+', '-', '*', '/',
                '=', '<', '>', '\'',
                '(', ')', '[', ']', '{', '}',
                '\'', ',', ':', ';']

    t_DOTADD = r'\.\+'
    t_DOTSUB = r'\.\-'
    t_DOTMUL = r'\.\*'
    t_DOTDIV = r'\.\/'
    t_ADDASSIGN = r'\+='
    t_SUBASSIGN = r'-='
    t_MULASSIGN = r'\*='
    t_DIVASSIGN = r'/='
    t_LE = r'<='
    t_GE = r'>='
    t_NEQ = r'!='
    t_EQ = r'=='
    t_ignore = ' \t'

    def t_ID(self, t):
        r'[a-zA-Z_]\w*'
        t.type = Scanner.reserved.get(t.value, 'ID')
        return t

    def t_FLOATNUM(self, t):
        r'(\d*\.\d+|\d+\.\d*)(E\d+)?'
        t.value = float(t.value)
        return t

    def t_INTNUM(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        t.value = str(t.value)[1:-1]
        return t

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def t_error(self, t):
        print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
        t.lexer.skip(1)

