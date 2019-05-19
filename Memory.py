class Memory:

    def __init__(self, name):  # memory name
        self.name = name
        self.variables = {}

    def has_key(self, name):  # variable name
        return name in self.variables

    def get(self, name):  # gets from memory current value of variable <name>
        if self.has_key(name):
            return self.variables[name]
        else:
            return None

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value


class MemoryStack:

    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.mem_stack = []
        if memory is not None:
            self.mem_stack.append(memory)
        else:
            self.mem_stack.append(Memory("Global"))

    def get(self, name):  # gets from memory stack current value of variable <name>
        for mem in reversed(self.mem_stack):
            if mem.has_key(name):
                return mem.get(name)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.mem_stack[-1].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        self.insert(name, value)
        for mem in self.mem_stack:
            if mem.has_key(name):
                mem.put(name, value)
                break

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.mem_stack.append(memory)

    def pop(self):  # pops the top memory from the stack
        return self.mem_stack.pop()
