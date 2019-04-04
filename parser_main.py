import sys
import ply.yacc as yacc
from Mparser import Mparser
import TreePrinter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example4.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    parser = Mparser()
    ast = parser.parse(text)
    print(ast.to_str())
