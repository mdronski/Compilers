
import AST
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator

ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv,
       "+=": operator.iadd, "-=": operator.isub, "*=": operator.imul, "/=": operator.itruediv,
       "==": operator.eq, "!=": operator.ne, ">": operator.gt, "<": operator.lt,
       "<=": operator.le, ">=": operator.ge}

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.variableStack = MemoryStack()
        self.functionStack = MemoryStack()

    @on('node')  #
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.variableStack.get(node.id)

    @when(AST.Value)
    def visit(self, node):
        return self.variableStack.get(node.id)

    @when(AST.Statements)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Assignment)
    def visit(self, node):
        expression = node.right.accept(self)
        if node.op == "=":
            self.variableStack.insert(node.left.id, expression)
        else:
            self.variableStack.insert(node.left.id, ops[node.op](self.variableStack.get(node.left.id), expression))
        return expression

    @when(AST.PrintInstr)
    def visit(self, node):
        string = ""
        for expr in [c.accept(self) for c in node.children]:
            string += str(expr)
        print(string)

    @when(AST.CondStatement)
    def visit(self, node):
        if node.condition.accept(self):
            node.statements.accept(self)
        elif node.has_else:
            node.else_statements.accept(self)

    @when(AST.WhileLoop)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.statements.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.ForLoop)
    def visit(self, node):
        self.variableStack.insert(node.id, node.start.accept(self))
        while self.variableStack.get(node.id) < node.end.accept(self):
            try:
                node.statements.accept(self)
                self.variableStack.insert(node.id, self.variableStack.get(node.id)+1)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.ReturnInstr)
    def visit(self, node):
        value = node.value.accept(self)
        raise ReturnValueException(value)

    @when(AST.ContinueInstr)
    def visit(self, node):
        raise ContinueException()

    @when(AST.BreakInstr)
    def visit(self, node):
        raise BreakException()

    # @when(AST.ExpressionList)
    # def visit(self, node):
    #     expr_list = []
    #     for child in node.children:
    #         expr_list.append(child.accept(self))
    #     return expr_list

    @when(AST.BinOp)
    def visit(self, node):
        res1 = node.left.accept(self)
        res2 = node.right.accept(self)
        return ops[node.op](res1, res2)

    @when(AST.LogicOp)
    def visit(self, node):
        res1 = node.left.accept(self)
        res2 = node.right.accept(self)
        return ops[node.op](res1, res2)
