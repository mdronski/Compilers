class Node(object):
    def __str__(self):
        return self.printTree("")

    def accept(self, visitor):
        return visitor.visit(self)
    

class Statements(Node):
    def __init__(self):
        self.statements = []


class Constant(Node):
    def __init__(self, value):
        self.value = value


class IntNum(Constant):
    pass


class FloatNum(Constant):
    pass


class String(Constant):
    pass


class Variable(Node):
    def __init__(self, id):
        self.id = id


class Value(Node):
    def __init__(self, id):
        self.id = id


class MatrixAccess(Node):
    def __init__(self, id, row, column):
        self.id = id
        self.row = row
        self.column = column


class Matrix(Node):
    def __init__(self):
        self.rows = []


class OnesMatrix(Matrix):
    def __init__(self, n):
        super().__init__()
        self.n = n
        rows = []
        for i in range(n):
            row = MatrixRow()
            row.values = [1 for x in range(n)]
            rows.append(row)
        self.rows = rows


class EyeMatrix(Matrix):
    def __init__(self, n):
        super().__init__()
        self.n = n
        rows = []
        for i in range(n):
            row = MatrixRow()
            row.values = [1 for x in range(n)]
            row.values[i] = 1
            rows.append(row)
        self.rows = rows


class ZerosMatrix(Matrix):
    def __init__(self, n):
        super().__init__()
        self.n = n
        rows = []
        for i in range(n):
            row = MatrixRow()
            row.values = [0 for x in range(n)]
            rows.append(row)
        self.rows = rows


class MatrixRow(Node):
    def __init__(self):
        self.values = []


class Assignment(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class BinOp(Node):
    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right


class LogicOp(BinOp):
    pass


class UnaryOp(Node):
    def __init__(self, expression, op):
        self.op = op
        self.expression = expression


class CondStatement(Node):
    def __init__(self, condition, statements, has_else=False, else_statements=None):
        self.condition = condition
        self.statements = statements
        self.has_else = has_else
        self.else_statements = else_statements


class WhileLoop(Node):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements


class ForLoop(Node):
    def __init__(self, id, start, end, statements):
        self.id = id
        self.start = start
        self.end = end
        self.statements = statements


class ReturnInstr(Node):
    def __init__(self, value):
        self.value = value


class ContinueInstr(Node):
    pass


class BreakInstr(Node):
    pass


class PrintInstr(Node):
    def __init__(self):
        self.instructions = []


class Error(Node):
    def __init__(self):
        pass
