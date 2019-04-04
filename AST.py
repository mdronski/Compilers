class Node(object):
    def to_str(self):
        return self.printTree("")


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


class Matrix(Node):
    def __init__(self, value=None):
        if value is None:
            value = []
        self.rows = value


class MatrixRows(Node):
    def __init__(self):
        self.rows = []


class MatrixRow(Node):
    def __init__(self):
        self.values = []


class Assignment(Node):
    def __init__(self, id, value):
        self.id = id
        self.value = value


class MatrixAssignment(Node):
    def __init__(self, id, row, column, value):
        self.id = id
        self.row = row
        self.column = column
        self.value = value


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
        self.hasElse = has_else
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

# class InstructionToPrint(Node):
#     def __init__(self):
#         self.instructions = []


class Error(Node):
    def __init__(self):
        pass
