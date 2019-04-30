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

    @addToClass(AST.Value)
    def printTree(self, indent):
        if hasattr(self.id, "printTree"):
            return self.id.printTree(indent)
        else:
            return indent + str(self.id) + "\n"

    @addToClass(AST.Constant)
    def printTree(self, indent):
        return indent + str(self.value) + "\n"

    @addToClass(AST.Variable)
    def printTree(self, indent):
        if hasattr(self.id, "printTree"):
            return self.id.printTree(indent)
        else:
            return indent + str(self.id) + "\n"

    @addToClass(AST.MatrixAccess)
    def printTree(self, indent):
        result = indent + "REF\n"
        result += indent + "| " + str(self.id) + "\n"
        result += indent + "| " + str(self.row) + "\n"
        result += indent + "| " + str(self.column) + "\n"
        return result

    @addToClass(AST.Statements)
    def printTree(self, indent):
        result = ""
        for block in self.statements:
            result += block.printTree(indent)
        return result

    @addToClass(AST.Assignment)
    def printTree(self, indent):
        result = indent + str(self.op) + "\n"
        result += self.left.printTree(indent + "| ")
        result += self.right.printTree(indent + "| ")
        return result

    @addToClass(AST.BinOp)
    def printTree(self, indent):
        result = indent + str(self.op) + "\n"
        result += self.left.printTree(indent + "| ")
        result += self.right.printTree(indent + "| ")
        return result

    @addToClass(AST.UnaryOp)
    def printTree(self, indent):
        name = ""
        if self.op == "'":
            name = "TRANSPOSE"
        else:
            name = "NEGATION"
        result = indent + name + "\n"
        result += self.expression.printTree(indent + "| ")
        return result

    @addToClass(AST.PrintInstr)
    def printTree(self, indent):
        result = indent + "PRINT\n"
        for instruction in self.instructions:
            result += instruction.printTree(indent + "| ")
        return result

    @addToClass(AST.CondStatement)
    def printTree(self, indent):
        result = indent + "IF\n"
        result += self.condition.printTree(indent + "| ")
        result += indent + "THEN\n"
        result += self.statements.printTree(indent + "| ")
        if self.has_else:
            result += indent + "ELSE\n"
            result += self.else_statements.printTree(indent + "| ")
        return result

    @addToClass(AST.WhileLoop)
    def printTree(self, indent):
        result = indent + "WHILE\n"
        result += indent + "| COND\n"
        result += self.condition.printTree(indent + "| ")
        result += indent + "| DO\n"
        result += self.statements.printTree(indent + "| ")
        return result

    @addToClass(AST.ForLoop)
    def printTree(self, indent):
        result = indent + "FOR\n"
        result += indent + "| " + self.id + "\n"
        result += indent + "| RANGE\n"
        result += self.start.printTree(indent + "| | ")
        result += self.end.printTree(indent + "| | ")
        result += self.statements.printTree(indent + "| ")
        return result

    @addToClass(AST.ReturnInstr)
    def printTree(self, indent):
        result = indent + "RETURN\n"
        result += self.value.printTree(indent + "| ")
        return result

    @addToClass(AST.ContinueInstr)
    def printTree(self, indent):
        return indent + "CONTINUE\n"

    @addToClass(AST.BreakInstr)
    def printTree(self, indent):
        return indent + "BREAK\n"

    @addToClass(AST.Matrix)
    def printTree(self, indent):
        result = self.rows.printTree(indent)
        return result

    @addToClass(AST.MatrixRow)
    def printTree(self, indent):
        result = indent + "VECTOR\n"
        for val in self.values:
            result += val.printTree(indent + "| ")
        return result

    @addToClass(AST.OnesMatrix)
    def printTree(self, indent):
        result = indent + "ONES\n"
        result += indent + "| " + str(self.n) + "\n"
        return result

    @addToClass(AST.EyeMatrix)
    def printTree(self, indent):
        result = indent + "EYE\n"
        result += indent + "| " + str(self.n) + "\n"
        return result

    @addToClass(AST.ZerosMatrix)
    def printTree(self, indent):
        result = indent + "ZEROS \n"
        result += indent + "| " + str(self.n) + "\n"
        return result