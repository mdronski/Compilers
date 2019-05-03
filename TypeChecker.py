#!/usr/bin/python
import AST
from SymbolTable import *
from collections import defaultdict

bin_ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['+', '-', '*', '/']:
    bin_ttype[op]['int']['int'] = 'int'
    bin_ttype[op]['int']['float'] = 'float'
    bin_ttype[op]['float']['int'] = 'float'
    bin_ttype[op]['float']['float'] = 'float'
    bin_ttype[op]['matrix']['matrix'] = 'matrix'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    bin_ttype[op]['int']['float'] = 'boolean'
    bin_ttype[op]['float']['int'] = 'boolean'
    bin_ttype[op]['float']['float'] = 'boolean'
    bin_ttype[op]['string']['string'] = 'boolean'

bin_ttype['+']['string']['string'] = 'string'


un_ttype = defaultdict(lambda: defaultdict(lambda: None))
un_ttype['-']['int'] = 'int'
un_ttype['-']['float'] = 'float'
un_ttype['-']['matrix'] = 'matrix'
un_ttype['\'']['matrix'] = 'matrix'


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
    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.is_in_loop = False

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Matrix(self, node):
        self.visit(node.rows)
        return 'matrix'

    def visit_Variable(self, node):
        declaration = self.table.get_from_lowest_scope(node.id)
        if declaration is None:
            print("Error: Usage of undeclared variable '{}': line {}".format(node.id, node.line))
        else:
            return declaration.type

    def visit_BinOp(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if bin_ttype[op][type1][type2] is None:
            print("Error: Type conflict, '{} {} {}': at line {}".format(type1, op, type2, node.line))
        return bin_ttype[op][type1][type2]

    def visit_LogicOp(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if bin_ttype[op][type1][type2] is None:
            print("Error: Type conflict, '{} {} {}': at line {}".format(type1, op, type2, node.line))
        return bin_ttype[op][type1][type2]

    def visit_UnaryOp(self, node):
        expr_type = self.visit(node.expression)
        op = node.op
        if un_ttype[op][expr_type] is None:
            print("Error: Type conflict, '{} {} ': at line {}".format(op, expr_type, node.line))
        return un_ttype[op][expr_type]

    def visit_CondStatement(self, node):
        self.visit(node.condition)
        self.visit(node.statements)
        if node.has_else:
            self.visit(node.else_statements)

    def visit_WhileLoop(self, node):
        self.visit(node.condition)
        self.is_in_loop = True
        self.visit(node.statements)
        self.is_in_loop = False

    def visit_ForLoop(self, node):
        self.visit(node.start)
        self.visit(node.end)
        self.is_in_loop = True
        self.visit(node.statements)
        self.is_in_loop = False

    def visit_ReturnInstr(self, node):
        self.visit(node.value)

    def visit_ContinueInstr(self, node):
        if not self.is_in_loop:
            print("Error: Continue outside the loop, at line {}".format(node.line))

    def visit_BreakInstr(self, node):
        if not self.is_in_loop:
            print("Error: Break outside the loop, at line {}".format(node.line))

    def visit_OnesMatrix(self, node):
        pass

    def visit_EyeMatrix(self, node):
        pass

    def visit_ZerosMatrix(self, node):
        pass

    def visit_MatrixRow(self, node):
        if not node.validate():
            print("Error: Wrong Matrix declaration, at line {}".format(node.line))

    def visit_Assignment(self, node):
        expr_type = self.visit(node.right)
        if node.op in ['+=', '-=', '*=', '/=']:
            if node.left.id in self.table.symbols:
                self.table.put(node.left.id, VariableSymbol(node.left, expr_type))
            else:
                print("Error: Variable {} not declared, at line {}".format(node.left.id, node.line))
        else:
            self.table.put(node.left.id, VariableSymbol(node.left, expr_type))



# class MatrixAccess(Node):
#
# class Matrix(Node):
#
# class OnesMatrix(Matrix):
#
# class EyeMatrix(Matrix):
#
# class ZerosMatrix(Matrix):
#
# class MatrixRow(Node):
#
# class Assignment(Node):
#
# class LogicOp(BinOp):
#
# class UnaryOp(Node):
#
# class CondStatement(Node):
#
# class WhileLoop(Node):
#
# class ForLoop(Node):
#
# class ReturnInstr(Node):
#
# class ContinueInstr(Node):
#
# class BreakInstr(Node):
#
# class PrintInstr(Node):
#
# class Error(Node):


