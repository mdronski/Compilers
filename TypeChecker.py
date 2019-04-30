#!/usr/bin/python
import AST
from SymbolTable import *
from collections import defaultdict

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['int'] = 'int'
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'
    ttype[op]['tensor']['tensor'] = 'tensor'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['float'] = 'boolean'
    ttype[op]['float']['int'] = 'boolean'
    ttype[op]['float']['float'] = 'boolean'
    ttype[op]['string']['string'] = 'boolean'

ttype['+']['string']['string'] = 'string'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if ttype[op][type1][type2] is None:
            print("Error: Type conflict, '{} {} {}': at line {}".format(type1, op, type2, node.line))
        return ttype[op][type1][type2]

    def visit_Variable(self, node):
        pass
