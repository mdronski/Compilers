class Node(object):
    pass


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
    def __init__(self):
        self.rows = []


class MatrixRow(Node):
    def __init__(self):
        self.values = []


class Assignment(Node):
    def __init__(self, id, value):
        self.id = id
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


# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
