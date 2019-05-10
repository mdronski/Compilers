import sys
from Scanner import Scanner

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    scanner = Scanner()
    scanner.input(text)
    lexer = scanner.lexer
    lexer.input(text)

    while True:
        tok = lexer.token()
        if not tok:
            break
        column = scanner.find_column(text, tok)
        print('{0:<9}: {1:<13}{2}'.format('(' + str(tok.lineno) + ', ' + str(column) + ')', str(tok.type), ' ( ' + str(tok.value) + ' )'))
