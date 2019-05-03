class Node(object):
    def __init__(self):
        self.children = ()

    def __str__(self):
        return self.printTree("")

    def accept(self, visitor):
        return visitor.visit(self)


class Statements(Node):
    def __init__(self):
        self.children = []


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
    def __init__(self, id, line):
        self.id = id
        self.line = line


class MatrixAccess(Node):
    def __init__(self, id, dims, line):
        self.id = id
        self.dims = dims
        self.line = line


class Matrix(Node):
    def __init__(self):
        self.rows = None # edited

    def validate(self):
        return self.rows.validate()

    def shape(self):
        return self.rows.shape()


class Value(Node):
    def __init__(self, id):
        self.id = id


class MatrixRow(Node):
    def __init__(self, line):
        self.values = []
        self.line = line

    def validate(self):
        # chceck if the same type
        t = type(self.values[0].id)
        for x in self.values:
            if type(x.id) != t:
                return False

        if isinstance(self.values[0].id, Matrix):
            for val in self.values:
                if isinstance(val.id, Matrix):
                    if not val.id.validate():
                        return False

            l = len(self.values[0].id.rows.values)
            for row in self.values:
                if l != len(row.id.rows.values):
                    return False
        return True

    def check_types(self):
        t = type(self.values[0].id)
        for n in self.values:
            if type(n.id) != t:
                print(type(n.id))
                return False
        return True

    def shape(self):
        if not isinstance(self.values[0].id, Matrix):
            return [len(self.values)]
        return [len(self.values)] + self.values[0].id.shape()


class OnesMatrix(Matrix):
    def __init__(self, dims, line):
        super().__init__()
        self.dims = dims
        self.line = line
        # self.n = n
        # rows = []
        # for i in range(n):
        #     row = MatrixRow(line)
        #     row.values = [1 for x in range(n)]
        #     rows.append(row)
        # self.rows = rows

    def shape(self):
        return self.dims


class EyeMatrix(Matrix):
    def __init__(self, dims, line):
        super().__init__()
        self.dims = dims
        self.line = line
        # self.n = n
        # rows = []
        # for i in range(n):
        #     row = MatrixRow(line)
        #     row.values = [1 for x in range(n)]
        #     row.values[i] = 1
        #     rows.append(row)
        # self.rows = rows

    def shape(self):
        return self.dims


class ZerosMatrix(Matrix):
    def __init__(self, dims, line):
        super().__init__()
        self.dims = dims
        self.line = line
        # self.n = n
        # rows = []
        # for i in range(n):
        #     row = MatrixRow(line)
        #     row.values = [0 for x in range(n)]
        #     rows.append(row)
        # self.rows = rows

    def shape(self):
        return self.dims


class Assignment(Node):
    def __init__(self, left, op, right, line):
        self.left = left
        self.op = op
        self.right = right
        self.line = line


class BinOp(Node):
    def __init__(self, left, op, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class LogicOp(BinOp):
    pass


class UnaryOp(Node):
    def __init__(self, expression, op, line):
        self.op = op
        self.expression = expression
        self.line = line


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
    def __init__(self, value, line):
        self.value = value
        self.line = line


class ContinueInstr(Node):
    def __init__(self, line):
        self.line = line


class BreakInstr(Node):
    def __init__(self, line):
        self.line = line


class PrintInstr(Node):
    def __init__(self):
        self.children = []


class Error(Node):
    def __init__(self):
        pass
