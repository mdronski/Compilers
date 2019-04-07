from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Constant)
    def printTree(self, depth):
        return depth + str(self.value) + "\n"

    @addToClass(AST.Variable)
    def printTree(self, depth):
        if hasattr(self.id, "printTree"):
            return self.id.printTree(depth)
        else:
            return depth + str(self.id) + "\n"

    @addToClass(AST.MatrixAccess)
    def printTree(self, depth):
        result = depth + "REF\n"
        result += depth + "| " + str(self.id) + "\n"
        result += depth + "| " + str(self.row) + "\n"
        result += depth + "| " + str(self.column) + "\n"
        return result

    @addToClass(AST.Statements)
    def printTree(self, depth):
        result = ""
        for block in self.statements:
            result += block.printTree(depth)
        return result

    @addToClass(AST.Assignment)
    def printTree(self, depth):
        result = depth + str(self.op) + "\n"
        result += self.left.printTree(depth + "| ")
        result += self.right.printTree(depth + "| ")
        return result

    @addToClass(AST.BinOp)
    def printTree(self, depth):
        result = depth + str(self.op) + "\n"
        result += self.left.printTree(depth + "| ")
        result += self.right.printTree(depth + "| ")
        return result

    @addToClass(AST.UnaryOp)
    def printTree(self, depth):
        name = ""
        if self.op == "'":
            name = "TRANSPOSE"
        else:
            name = "NEGATION"
        result = depth + name + "\n"
        result += self.expression.printTree(depth + "| ")
        return result

    @addToClass(AST.PrintInstr)
    def printTree(self, depth):
        result = depth + "PRINT\n"
        for instruction in self.instructions:
            result += instruction.printTree(depth + "| ")
        return result

    @addToClass(AST.CondStatement)
    def printTree(self, depth):
        result = depth + "IF\n"
        result += self.condition.printTree(depth + "| ")
        result += depth + "THEN\n"
        result += self.statements.printTree(depth + "| ")
        if self.has_else:
            result += depth + "ELSE\n"
            result += self.else_statements.printTree(depth + "| ")
        return result

    @addToClass(AST.WhileLoop)
    def printTree(self, depth):
        result = depth + "WHILE\n"
        result += depth + "| COND\n"
        result += self.condition.printTree(depth + "| ")
        result += depth + "| DO\n"
        result += self.statements.printTree(depth + "| ")
        return result

    @addToClass(AST.ForLoop)
    def printTree(self, depth):
        result = depth + "FOR\n"
        result += depth + "| " + self.id + "\n"
        result += depth + "| RANGE\n"
        result += self.start.printTree(depth + "| | ")
        result += self.end.printTree(depth + "| | ")
        result += self.statements.printTree(depth + "| ")
        return result

    @addToClass(AST.ReturnInstr)
    def printTree(self, depth):
        result = depth + "RETURN\n"
        result += self.value.printTree(depth + "| ")
        return result

    @addToClass(AST.ContinueInstr)
    def printTree(self, depth):
        return depth + "CONTINUE\n"

    @addToClass(AST.BreakInstr)
    def printTree(self, depth):
        return depth + "BREAK\n"

    @addToClass(AST.Matrix)
    def printTree(self, depth):
        result = depth + "MATRIX\n"
        for row in self.rows:
            result += row.printTree(depth + "| ")
        return result

    @addToClass(AST.MatrixRow)
    def printTree(self, depth):
        result = depth + "VECTOR\n"
        for val in self.values:
            result += depth + "| " + str(val) + "\n"
        return result

    @addToClass(AST.OnesMatrix)
    def printTree(self, depth):
        result = depth + "ONES\n"
        result += depth + "| " + str(self.n) + "\n"
        return result

    @addToClass(AST.EyeMatrix)
    def printTree(self, depth):
        result = depth + "EYE\n"
        result += depth + "| " + str(self.n) + "\n"
        return result

    @addToClass(AST.ZerosMatrix)
    def printTree(self, depth):
        result = depth + "ZEROS \n"
        result += depth + "| " + str(self.n) + "\n"
        return result