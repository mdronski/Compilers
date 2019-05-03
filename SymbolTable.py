class Symbol:
    pass


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable(object):

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name):  # get variable symbol or fundef from <name> entry
        try:
            result = self.symbols[name]
            return result
        except KeyError:
            return None

    def get_parent_scope(self):
        return self.parent

    def get_from_lowest_scope(self, name):
        if self.get(name) is None:
            if self.parent is not None:
                return self.parent.get_from_lowest_scope(name)
            else:
                return None
        else:
            return self.get(name)

    def pushScope(self, name):
        pass

    def popScope(self):
        pass
