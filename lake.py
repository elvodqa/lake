from lake_parser import Lark_StandAlone, Transformer


class Import:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __str__(self):
        return f'Import({self.name})'

class Package:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __str__(self):
        return f'Package({self.name})'

class Enum:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __str__(self):
        return f'Enum({self.name}, {self.values})'
    

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __str__(self):
        return f'Struct({self.name}, {self.fields})'
    
class FunctionDecl:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __str__(self):
        return f'FunctionDecl({self.name}, {self.args}, {self.return_type})'
    


class TreeToLake(Transformer):
    def struct_decl(self, args):
        return Struct(name=args[0], fields=args[1:])
    def enum_decl(self, args):
        return Enum(name=args[0], values=args[1:])
    def import_statement(self, args):
        return Import(name=args[0])
    def package(self, args):
        return Package(name=args[0])
    def function_decl(self, args):
        return FunctionDecl(name=args[0], args=args[1], return_type=args[2])

        

parser = Lark_StandAlone()

with open('./test.lk') as f:
    code = f.read()
    l = parser.parse(code)
    print(l.pretty())

    #transform = TreeToLake().transform(l)
    #print(transform.pretty())

