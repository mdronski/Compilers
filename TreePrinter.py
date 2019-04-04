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
        return depth + str(self.id) + "\n"

    @addToClass(AST.Statements)
    def printTree(self, depth):
        result = ""
        for block in self.statements:
            result += block.printTree(depth)
        return result

    @addToClass(AST.Assignment)
    def printTree(self, depth):
        result = depth + "=\n"
        result += depth + "| " + str(self.id) + "\n"
        result += self.value.printTree(depth + "| ")
        return result

    @addToClass(AST.PrintInstr)
    def printTree(self, depth):
        result = depth + "PRINT\n"
        result += self.instructions.printTree(depth + "| ")
        return result

    @addToClass(AST.CondStatement)
    def printTree(self, depth):
        result = depth + "IF\n"
        result += self.condition.printTree(depth + "| ")
        result += self.statements.printTree(depth + "| ")
        if self.has_else is not None:
            result += depth + "ELSE\n"
            result += self.else_statements.printTree(depth + "| ")
        return result

    @addToClass(AST.WhileLoop)
    def printTree(self, depth):
        result = depth + "WHILE\n"
        result += self.condition.printTree(depth + "| ")
        result += self.statements.printTree(depth + "| ")
        return result

    @addToClass(AST.ForLoop)
    def printTree(self, depth):
        result = depth + "FOR\n"
        result += self.statements.printTree(depth + "| ")
        result = depth + "START\n"
        result += self.start.printTree(depth + "| ")
        result = depth + "END\n"
        result += self.end.printTree(depth + "| ")
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

    @addToClass(AST.BinOp)
    def printTree(self, depth):
        result = depth + str(self.op) + "\n"
        result += self.left.printTree(depth + "| ")
        result += self.right.printTree(depth + "| ")
        return result
